#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module allows users to allocate a new IPv4 Address on their accounts."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
from ansible_specdoc.objects import FieldType, SpecDocMeta, SpecField

spec: dict = {
    "linode_id": SpecField(
        type=FieldType.integer,
        description=[
            "The ID of a Linode you have access to "
            "that this address will be allocated to."
        ],
    ),
    "public": SpecField(
        type=FieldType.bool,
        description=["Whether to create a public or private IPv4 address."],
    ),
    "type": SpecField(
        type=FieldType.string,
        choices=["ipv4"],
        description=[
            "The type of address you are requesting. "
            "Only IPv4 addresses may be allocated through this operation."
        ],
    ),
    "address": SpecField(
        type=FieldType.string,
        description=["The IP address to delete."],
        conflicts_with=["linode_id", "public", "type"],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this IP."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Allocates a new IPv4 Address on your Account. "
        "The Linode must be configured to support "
        "additional addresses - "
        "please Open a support ticket "
        "requesting additional addresses before attempting allocation.",
    ],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={},
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
- Allocates a new IPv4 Address on your Account. The Linode must be configured to support
  additional addresses - please Open a support ticket requesting additional addresses
  before attempting allocation.
module: ip
notes: []
options:
  address:
    description:
    - The IP address to delete.
    required: false
    type: str
  linode_id:
    description:
    - The ID of a Linode you have access to that this address will be allocated to.
    required: false
    type: int
  public:
    description:
    - Whether to create a public or private IPv4 address.
    required: false
    type: bool
  state:
    choices:
    - present
    - absent
    description:
    - The state of this IP.
    required: true
    type: str
  type:
    choices:
    - ipv4
    description:
    - The type of address you are requesting. Only IPv4 addresses may be allocated
      through this operation.
    required: false
    type: str
requirements:
- python >= 3
short_description: Allocates a new IPv4 Address on your Account. The Linode must be
  configured to support additional addresses - please Open a support ticket requesting
  additional addresses before attempting allocation.
"""
EXAMPLES = r"""
- name: Allocate IP to Linode
  linode.cloud.ip:
    linode_id: 123
    public: true
    type: ipv4
    state: present
"""
RETURN = r"""
{}
"""


class Module(LinodeModuleBase):
    """Module for allocating a new IP"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "ip": None,
        }
        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_together=[
                ("linode_id", "public", "type"),
            ],
        )

    def _handle_present(self) -> None:
        params = filter_null_values(self.module.params)
        linode_id = params.get("linode_id")
        public = params.get("public")

        try:
            ip = self.client.networking.ip_allocate(linode_id, public)
            self.register_action(
                f"IP allocation to Linode {linode_id} completed."
            )
        except Exception as exc:
            self.fail(msg=f"failed to allocate IP to Linode {linode_id}: {exc}")

        self.results["ip"] = ip._raw_json

    def _handle_absent(self) -> None:
        # TODO: Implement deleting IP once it's available in python-sdk.
        #  Raise an error for now when user reaches deleting IP.
        self.fail(
            msg="failed to delete IP: IP deleting is currently not supported."
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for IP module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
