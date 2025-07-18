#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode LKE node pools."""

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_node_pool as docs
import linode_api4
import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
    jsonify_node_pool,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import LKECluster, LKENodePool

linode_lke_pool_autoscaler = {
    "enabled": SpecField(
        type=FieldType.bool,
        editable=True,
        description=[
            "Whether autoscaling is enabled for this Node Pool.",
            "NOTE: Subsequent playbook runs will override nodes created by the cluster autoscaler.",
        ],
    ),
    "max": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The maximum number of nodes to autoscale to. "
            "Defaults to the value provided by the count field."
        ],
    ),
    "min": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The minimum number of nodes to autoscale to. "
            "Defaults to the Node Pool’s count."
        ],
    ),
}

linode_lke_pool_disks = {
    "type": SpecField(
        type=FieldType.string,
        required=True,
        description=["This custom disk partition’s filesystem type."],
        choices=["raw", "ext4"],
    ),
    "size": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The size of this custom disk partition in MB."],
    ),
}

linode_lke_pool_taint = {
    "key": SpecField(
        type=FieldType.string,
        description=["The Kubernetes taint key."],
        required=True,
        editable=True,
    ),
    "value": SpecField(
        type=FieldType.string,
        description=["The Kubernetes taint value."],
        required=True,
        editable=True,
    ),
    "effect": SpecField(
        type=FieldType.string,
        description=["The Kubernetes taint effect."],
        required=True,
        editable=True,
        choices=["NoSchedule", "PreferNoSchedule", "NoExecute"],
    ),
}

MODULE_SPEC = {
    "cluster_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The ID of the LKE cluster that contains this node pool."],
    ),
    "autoscaler": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "When enabled, the number of nodes autoscales within the "
            "defined minimum and maximum values."
        ],
        suboptions=linode_lke_pool_autoscaler,
    ),
    "count": SpecField(
        type=FieldType.integer,
        editable=True,
        description=["The number of nodes in the Node Pool."],
    ),
    "disks": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        description=[
            "This Node Pool’s custom disk layout. "
            "Each item in this array will create a "
            "new disk partition for each node in this "
            "Node Pool."
        ],
        suboptions=linode_lke_pool_disks,
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        required=True,
        description=[
            "An array of tags applied to this object.",
            "Tags must be unique as they are used by the "
            "`lke_node_pool` module to uniquely identify node pools.",
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=[
            "The Linode Type for all of the nodes in the Node Pool.",
            "Required if `state` == `present`.",
        ],
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "skip_polling": SpecField(
        type=FieldType.bool,
        description=[
            "If true, the module will not wait for all "
            "nodes in the node pool to be ready."
        ],
        default=False,
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The period to wait for the node pool to be ready in seconds."
        ],
        default=600,
    ),
    "labels": SpecField(
        type=FieldType.dict,
        editable=True,
        description=[
            "Key-value pairs added as labels to nodes in the node pool. "
            "Labels help classify your nodes and to easily select subsets of objects."
        ],
    ),
    "taints": SpecField(
        type=FieldType.list,
        editable=True,
        description=[
            "Kubernetes taints to add to node pool nodes. Taints help control "
            "how pods are scheduled onto nodes, specifically allowing them to repel certain pods."
        ],
        suboptions=linode_lke_pool_taint,
    ),
    "k8s_version": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The desired Kubernetes version for this Kubernetes ",
            "Node Pool in the format of <major>.<minor>, and the ",
            "latest supported patch version.",
            "NOTE: Only available for LKE Enterprise to support node pool upgrades. ",
            "This field may not currently be available to all users and is under v4beta.",
        ],
    ),
    "update_strategy": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "Upgrade strategy describes the available upgrade strategies.",
            "NOTE: Only available for LKE Enterprise to support node pool upgrades. ",
            "This field may not currently be available to all users and is under v4beta.",
        ],
        choices=["rolling_update", "on_recycle"],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode LKE cluster node pools."],
    requirements=global_requirements,
    author=global_authors,
    options=MODULE_SPEC,
    examples=docs.examples,
    return_values={
        "node_pool": SpecReturnValue(
            description="The Node Pool in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-node-pool",
            type=FieldType.dict,
            sample=docs.result_node_pool,
        )
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
- Manage Linode LKE cluster node pools.
module: lke_node_pool
notes: []
options:
  autoscaler:
    description:
    - When enabled, the number of nodes autoscales within the defined minimum and
      maximum values.
    required: false
    suboptions:
      enabled:
        description:
        - Whether autoscaling is enabled for this Node Pool.
        - 'NOTE: Subsequent playbook runs will override nodes created by the cluster
          autoscaler.'
        required: false
        type: bool
      max:
        description:
        - The maximum number of nodes to autoscale to. Defaults to the value provided
          by the count field.
        required: false
        type: int
      min:
        description:
        - "The minimum number of nodes to autoscale to. Defaults to the Node Pool\u2019\
          s count."
        required: false
        type: int
    type: dict
  cluster_id:
    description:
    - The ID of the LKE cluster that contains this node pool.
    required: true
    type: int
  count:
    description:
    - The number of nodes in the Node Pool.
    required: false
    type: int
  disks:
    description:
    - "This Node Pool\u2019s custom disk layout. Each item in this array will create\
      \ a new disk partition for each node in this Node Pool."
    elements: dict
    required: false
    suboptions:
      size:
        description:
        - The size of this custom disk partition in MB.
        required: true
        type: int
      type:
        choices:
        - raw
        - ext4
        description:
        - "This custom disk partition\u2019s filesystem type."
        required: true
        type: str
    type: list
  k8s_version:
    description:
    - 'The desired Kubernetes version for this Kubernetes '
    - 'Node Pool in the format of <major>.<minor>, and the '
    - latest supported patch version.
    - 'NOTE: Only available for LKE Enterprise to support node pool upgrades. '
    - This field may not currently be available to all users and is under v4beta.
    required: false
    type: str
  labels:
    description:
    - Key-value pairs added as labels to nodes in the node pool. Labels help classify
      your nodes and to easily select subsets of objects.
    required: false
    type: dict
  skip_polling:
    default: false
    description:
    - If true, the module will not wait for all nodes in the node pool to be ready.
    required: false
    type: bool
  state:
    choices:
    - present
    - absent
    description:
    - The desired state of the target.
    required: true
    type: str
  tags:
    description:
    - An array of tags applied to this object.
    - Tags must be unique as they are used by the `lke_node_pool` module to uniquely
      identify node pools.
    elements: str
    required: true
    type: list
  taints:
    description:
    - Kubernetes taints to add to node pool nodes. Taints help control how pods are
      scheduled onto nodes, specifically allowing them to repel certain pods.
    required: false
    suboptions:
      effect:
        choices:
        - NoSchedule
        - PreferNoSchedule
        - NoExecute
        description:
        - The Kubernetes taint effect.
        required: true
        type: str
      key:
        description:
        - The Kubernetes taint key.
        required: true
        type: str
      value:
        description:
        - The Kubernetes taint value.
        required: true
        type: str
    type: list
  type:
    description:
    - The Linode Type for all of the nodes in the Node Pool.
    - Required if `state` == `present`.
    required: false
    type: str
  update_strategy:
    choices:
    - rolling_update
    - on_recycle
    description:
    - Upgrade strategy describes the available upgrade strategies.
    - 'NOTE: Only available for LKE Enterprise to support node pool upgrades. '
    - This field may not currently be available to all users and is under v4beta.
    required: false
    type: str
  wait_timeout:
    default: 600
    description:
    - The period to wait for the node pool to be ready in seconds.
    required: false
    type: int
requirements:
- python >= 3
short_description: Manage Linode LKE cluster node pools.
"""
EXAMPLES = r"""
- name: Create a Linode LKE node pool
  linode.cloud.lke_node_pool:
    cluster_id: 12345
    tags:
    - my-pool
    count: 3
    type: g6-standard-2
    state: present
- name: Create a Linode LKE node pool with autoscaler
  linode.cloud.lke_node_pool:
    cluster_id: 12345
    tags:
    - my-pool
    count: 3
    type: g6-standard-2
    autoscaler:
      enabled: true
      min: 1
      max: 3
    state: present
- name: Delete a Linode LKE node pool
  linode.cloud.lke_node_pool:
    cluster_id: 12345
    tags:
    - my-pool
    state: absent
"""
RETURN = r"""
node_pool:
  description: The Node Pool in JSON serialized form.
  returned: always
  sample:
  - autoscaler:
      enabled: true
      max: 12
      min: 3
    count: 6
    disk_encryption: enabled
    disks:
    - size: 1024
      type: ext-4
    id: 456
    nodes:
    - id: '123456'
      instance_id: 123458
      status: ready
    tags:
    - example tag
    - another example
    type: g6-standard-4
  type: dict
"""


class LinodeLKENodePool(LinodeModuleBase):
    """Module for managing Linode Firewall devices"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "node_pool": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_node_pool(self) -> Optional[linode_api4.LKENodePool]:
        try:
            params = self.module.params
            cluster_id = params["cluster_id"]
            tags = params["tags"]

            cluster = linode_api4.LKECluster(self.client, cluster_id)
            for pool in cluster.pools:
                if set(pool._raw_json["tags"]) == set(tags):
                    return pool

            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get node pool for cluster {0}: {1}".format(
                    cluster_id, exception
                )
            )

    def _wait_for_all_nodes_ready(
        self, pool: LKENodePool, timeout: int
    ) -> None:
        def _check_pool_nodes_ready() -> bool:
            # Enterprise node pools take longer than usual to provision nodes, so the API
            # initially returns an empty list of nodes. This is never possible, so we can
            # wait for the nodes list to no longer be empty before proceeding to checking on
            # the nodes' statuses.
            if len(pool.nodes) == 0:
                return False

            for node in pool.nodes:
                if node.status != "ready":
                    return False
            return True

        try:
            polling.poll(
                _check_pool_nodes_ready,
                step=4,
                timeout=timeout,
            )
        except polling.TimeoutException:
            self.fail(
                "failed to wait for lke node pool nodes: timeout period expired"
            )

    def _create_pool(self) -> LKENodePool:
        try:
            params = filter_null_values(self.module.params)

            cluster_id = params.pop("cluster_id")
            for key in ["api_token", "api_version"]:
                params.pop(key)

            pool = LKECluster(self.client, cluster_id).node_pool_create(
                params.pop("type"), params.pop("count"), **params
            )
            self.register_action("Created node pool {}".format(pool.id))

            return pool
        except Exception as exception:
            self.fail(
                msg="failed to create lke cluster node pool for cluster {0}: {1}".format(
                    self.module.params.get("cluster_id"), exception
                )
            )

    def _update_pool(self, pool: LKENodePool) -> LKENodePool:
        params = filter_null_values(self.module.params)

        cluster_id = params.pop("cluster_id")
        new_autoscaler = (
            params.pop("autoscaler") if "autoscaler" in params else None
        )
        new_count = params.pop("count")
        new_taints = params.pop("taints") if "taints" in params else None
        new_labels = params.pop("labels") if "labels" in params else None
        new_k8s_version = (
            params.pop("k8s_version") if "k8s_version" in params else None
        )
        new_update_strategy = (
            params.pop("update_strategy")
            if "update_strategy" in params
            else None
        )

        try:
            handle_updates(pool, params, set(), self.register_action)
        except Exception as exception:
            self.fail(
                msg="failed to update lke cluster node pool for cluster {0}: {1}".format(
                    cluster_id, exception
                )
            )

        should_update = False

        if pool.count != new_count:
            self.register_action(
                "Resized pool from {} -> {}".format(pool.count, new_count)
            )

            pool.count = new_count
            should_update = True

        if new_autoscaler is not None and pool.autoscaler != new_autoscaler:
            self.register_action("Updated autoscaler for Node Pool")
            pool.autoscaler = new_autoscaler
            should_update = True

        if new_taints is not None and pool.taints != new_taints:
            self.register_action("Updated taints for Node Pool")
            pool.taints = new_taints
            should_update = True

        if new_labels is not None and pool.labels != new_labels:
            self.register_action("Updated labels for Node Pool")
            pool.labels = new_labels
            should_update = True

        if new_k8s_version is not None and pool.k8s_version != new_k8s_version:
            self.register_action("Updated k8s version for Node Pool")
            pool.k8s_version = new_k8s_version
            should_update = True

        if (
            new_update_strategy is not None
            and pool.update_strategy != new_update_strategy
        ):
            self.register_action("Updated update strategy for Node Pool")
            pool.update_strategy = new_update_strategy
            should_update = True

        if should_update:
            try:
                pool.save()
            except Exception as exception:
                return self.fail(
                    msg="failed to update node pool for cluster {0}: {1}".format(
                        cluster_id, exception
                    )
                )

        pool._api_get()

        return pool

    def _handle_present(self) -> None:
        pool = self._get_node_pool()

        # Create the device if it does not already exist
        if pool is None:
            pool = self._create_pool()

        pool = self._update_pool(pool)

        if not self.module.params.get("skip_polling"):
            self._wait_for_all_nodes_ready(
                pool, self._timeout_ctx.seconds_remaining
            )

        self.results["node_pool"] = jsonify_node_pool(pool)

    def _handle_absent(self) -> None:
        pool = self._get_node_pool()

        if pool is not None:
            self.results["node_pool"] = jsonify_node_pool(pool)

            self.register_action(
                "Deleted pool {0} from cluster {1}".format(
                    pool.id, self.module.params["cluster_id"]
                )
            )
            pool.delete()

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for lke_node_pool module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode LKE Node Pool module"""
    LinodeLKENodePool()


if __name__ == "__main__":
    main()
