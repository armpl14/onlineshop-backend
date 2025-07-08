#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation for the linode.cloud.database_mysql_v2 module."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_mysql_v2 as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    SPEC_FORK,
    SPEC_UPDATE_WINDOW_V2,
    call_protected_provisioning,
    wait_for_database_status,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
    mapping_to_dict,
    poll_condition,
    safe_find,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import MySQLDatabase

SPEC = {
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The desired state of the Managed Database."],
    ),
    "allow_list": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of IP addresses and CIDR ranges that can access the Managed Database."
        ],
        editable=True,
    ),
    "cluster_size": SpecField(
        type=FieldType.integer,
        description=[
            "The number of Linode instance nodes deployed to the Managed Database."
        ],
        editable=True,
    ),
    "engine": SpecField(
        type=FieldType.string,
        description=["The Managed Database engine in engine/version format."],
        editable=True,
    ),
    "label": SpecField(
        type=FieldType.string,
        description=["The label of the Managed Database."],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The region of the Managed Database."],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=[
            "The Linode Instance type used by the Managed Database for its nodes."
        ],
        editable=True,
    ),
    "fork": SpecField(
        type=FieldType.dict,
        description=["Information about a database to fork from."],
        suboptions=SPEC_FORK,
    ),
    "updates": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_UPDATE_WINDOW_V2,
        description=[
            "Configuration settings for automated patch "
            "update maintenance for the Managed Database."
        ],
        editable=True,
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The maximum number of seconds a poll operation can take before "
            "raising an error."
        ],
        default=45 * 60,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create, read, and update a Linode MySQL database.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "database": SpecReturnValue(
            description="The database in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance",
            type=FieldType.dict,
            sample=docs.result_database_samples,
        ),
        "ssl_cert": SpecReturnValue(
            description="The SSL CA certificate for an accessible Managed MySQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance-ssl",
            type=FieldType.dict,
            sample=docs.result_ssl_cert_samples,
        ),
        "credentials": SpecReturnValue(
            description="The root username and password for an accessible Managed MySQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance-credentials",
            type=FieldType.dict,
            sample=docs.result_credentials_samples,
        ),
    },
)


DOCUMENTATION = r"""
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
- Zhiwei Liang (@zliang)
- Ye Chen (@yechen)
- Youjung Kim (@ykim)
- Vinay Shanthegowda (@vshanthe)
- Erik Zilber (@ezilber)
description:
- Create, read, and update a Linode MySQL database.
module: database_mysql_v2
notes: []
options:
  allow_list:
    description:
    - A list of IP addresses and CIDR ranges that can access the Managed Database.
    elements: str
    required: false
    type: list
  cluster_size:
    description:
    - The number of Linode instance nodes deployed to the Managed Database.
    required: false
    type: int
  engine:
    description:
    - The Managed Database engine in engine/version format.
    required: false
    type: str
  fork:
    description:
    - Information about a database to fork from.
    required: false
    suboptions:
      restore_time:
        description:
        - The database timestamp from which it was restored.
        required: false
        type: str
      source:
        description:
        - The instance id of the database that was forked from.
        required: false
        type: int
    type: dict
  label:
    description:
    - The label of the Managed Database.
    required: false
    type: str
  region:
    description:
    - The region of the Managed Database.
    required: false
    type: str
  state:
    choices:
    - present
    - absent
    description:
    - The desired state of the Managed Database.
    required: true
    type: str
  type:
    description:
    - The Linode Instance type used by the Managed Database for its nodes.
    required: false
    type: str
  updates:
    description:
    - Configuration settings for automated patch update maintenance for the Managed
      Database.
    required: false
    suboptions:
      day_of_week:
        choices:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        description:
        - The day to perform maintenance. 1=Monday, 2=Tuesday, etc.
        required: true
        type: int
      duration:
        description:
        - The maximum maintenance window time in hours.
        required: true
        type: int
      frequency:
        choices:
        - weekly
        default: weekly
        description:
        - The frequency at which maintenance occurs.
        required: false
        type: str
      hour_of_day:
        description:
        - The hour to begin maintenance based in UTC time.
        required: true
        type: int
    type: dict
  wait_timeout:
    default: 2700
    description:
    - The maximum number of seconds a poll operation can take before raising an error.
    required: false
    type: int
requirements:
- python >= 3
short_description: Create, read, and update a Linode MySQL database.
"""
EXAMPLES = r"""
- name: Create a basic MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    allow_list:
    - 0.0.0.0/0
    state: present
- name: Create a MySQL database with three nodes
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-standard-1
    cluster_size: 3
    allow_list:
    - 0.0.0.0/0
    state: present
- name: Create a MySQL database with an explicit maintenance schedule
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    updates:
      duration: 4
      frequency: weekly
      hour_of_day: 16
      day_of_week: 4
    state: present
- name: Create a MySQL database forked from another database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    fork:
      source: 12345
    state: present
- name: Delete a MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    state: absent
"""
RETURN = r"""
credentials:
  description: The root username and password for an accessible Managed MySQL Database.
  returned: always
  sample:
  - password: s3cur3P@ssw0rd
    username: akmadmin
  type: dict
database:
  description: The database in JSON serialized form.
  returned: always
  sample:
  - allow_list:
    - 10.0.0.3/32
    cluster_size: 3
    created: '2025-02-10T20:10:20'
    encrypted: true
    engine: mysql
    hosts:
      primary: a225891-akamai-prod-1798333-default.g2a.akamaidb.net
      standby: replica-a225891-akamai-prod-1798333-default.g2a.akamaidb.net
    id: 12345
    label: my-db
    members:
      172.104.207.136: primary
      194.195.112.177: failover
      45.79.126.72: failover
    oldest_restore_time: '2025-02-10T20:15:07'
    platform: rdbms-default
    port: 11876
    region: ap-west
    ssl_connection: true
    status: active
    total_disk_size_gb: 30
    type: g6-standard-1
    updated: '2025-02-10T20:25:55'
    updates:
      day_of_week: 4
      duration: 4
      frequency: weekly
      hour_of_day: 16
      pending: []
    used_disk_size_gb: 0
    version: 8.0.35
  type: dict
ssl_cert:
  description: The SSL CA certificate for an accessible Managed MySQL Database.
  returned: always
  sample:
  - ca_certificate: LS0tLS1CRUdJ...==
  type: dict
"""


class Module(LinodeModuleBase):
    """Module implementation for database_mysql_v2."""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "database": None,
            "ssl_cert": None,
            "credentials": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def _create(self) -> MySQLDatabase:
        params = filter_null_values_recursive(
            {
                k: v
                for k, v in self.module.params.items()
                if k
                in [
                    "allow_list",
                    "cluster_size",
                    "engine",
                    "fork",
                    "label",
                    "region",
                    "type",
                ]
            }
        )

        # This is necessary because `type` is a Python-reserved keyword
        if "type" in params:
            params["ltype"] = params.pop("type")

        create_poller = self.client.polling.event_poller_create(
            "database", "database_create"
        )

        database = self.client.database.mysql_create(**params)

        create_poller.set_entity_id(database.id)
        create_poller.wait_for_next_event_finished(
            timeout=self._timeout_ctx.seconds_remaining
        )

        wait_for_database_status(
            self.client,
            database,
            "active",
            timeout=self._timeout_ctx.seconds_remaining,
        )

        # The `updates` field is not currently supported in the POST
        # request body.
        updates = params.get("updates")
        if updates is not None:
            database.updates = params.get("updates")
            database.save()

            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        return database

    def _update(self, database: MySQLDatabase) -> None:
        database._api_get()

        params = copy.deepcopy(self.module.params)

        # The database PUT endpoint accepts `version` rather than `engine`
        engine = params.pop("engine", None)
        if engine is not None:
            engine_components = engine.split("/")

            if len(engine_components) < 2:
                raise ValueError(f"Invalid engine: {engine}")

            major_version = int(engine_components[1])

            # Evil hack to correct for the API returning a three-part value for the
            # `version` field while the user specifies the major version, while still
            # using handle_updates.
            #
            # If anyone can think of a better way to do this, please correct it :)
            if int(database.version.split(".")[0]) != major_version:
                params["version"] = major_version

        # The `updates` field is returned with an additional `pending` key that isn't
        # defined by the user, so we need to inject the actual value here.
        if "updates" in params and params["updates"] is not None:
            params["updates"]["pending"] = database.updates.pending

        # Apply updates
        updated_fields = handle_updates(
            database,
            params,
            {
                "label",
                "allow_list",
                "cluster_size",
                "updates",
                "type",
                "version",
            },
            self.register_action,
        )

        # NOTE: We don't poll for the database_update event here because it is not
        # triggered under all conditions.
        if len(updated_fields) > 0:
            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        # Sometimes the cluster_size attribute doesn't update until shortly after
        # a resize operation
        if "cluster_size" in updated_fields:

            def __poll_condition() -> bool:
                database._api_get()
                return database.cluster_size == params["cluster_size"]

            poll_condition(
                __poll_condition,
                timeout=self._timeout_ctx.seconds_remaining,
                step=1,
            )

    def _populate_results(self, database: MySQLDatabase) -> None:
        database._api_get()

        self.results["database"] = database._raw_json
        self.results["credentials"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials)
        )
        self.results["ssl_cert"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl)
        )

    def _handle_present(self) -> None:
        params = self.module.params

        result = safe_find(
            self.client.database.mysql_instances,
            MySQLDatabase.label == params.get("label"),
        )
        if result is None:
            result = self._create()
            self.register_action("Created MySQL database {0}".format(result.id))

        self._update(result)

        self._populate_results(result)

    def _handle_absent(self) -> None:
        params = self.module.params

        database = safe_find(
            self.client.database.mysql_instances,
            MySQLDatabase.label == params.get("label"),
        )

        if database is not None:
            self._populate_results(database)

            database.delete()

            self.register_action(f"Deleted MySQL database {database.id}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
        else:
            self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode MySQL database module"""
    Module()


if __name__ == "__main__":
    main()
