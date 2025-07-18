#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode rDNS."""

from __future__ import absolute_import, division, print_function

from ipaddress import IPv6Address, ip_address
from typing import Any, Optional, Union

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_info as ip_docs
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_rdns as ip_rdns_docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ExplicitNullValue, IPAddress

ip_rdns_spec = {
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        description=["The state of this rDNS of the IP address."],
    ),
    "address": SpecField(
        type=FieldType.string,
        description=["The IP address."],
        required=True,
    ),
    "rdns": SpecField(
        type=FieldType.string,
        editable=True,
        description=["The desired RDNS value."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode IP address's rDNS."],
    requirements=global_requirements,
    author=global_authors,
    options=ip_rdns_spec,
    examples=ip_rdns_docs.specdoc_examples,
    return_values={
        "ip": SpecReturnValue(
            description=(
                "The updated IP address with the new "
                "reverse DNS in JSON serialized form."
            ),
            docs_url=(
                "https://techdocs.akamai.com/linode-api/reference/get-ipv6-range"
            ),
            type=FieldType.dict,
            sample=ip_docs.result_ip_samples,
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
- Manage a Linode IP address's rDNS.
module: ip_rdns
notes: []
options:
  address:
    description:
    - The IP address.
    required: true
    type: str
  rdns:
    description:
    - The desired RDNS value.
    required: false
    type: str
  state:
    choices:
    - present
    - absent
    description:
    - The state of this rDNS of the IP address.
    required: false
    type: str
requirements:
- python >= 3
short_description: Manage a Linode IP address's rDNS.
"""
EXAMPLES = r"""
- name: Update reverse DNS
  linode.cloud.ip_rdns:
    state: present
    address: 97.107.143.141
    rdns: 97.107.143.141.nip.io
- name: Remove the reverse DNS
  linode.cloud.ip_rdns:
    state: absent
    address: 97.107.143.141
"""
RETURN = r"""
ip:
  description: The updated IP address with the new reverse DNS in JSON serialized
    form.
  returned: always
  sample:
  - address: 97.107.143.141
    gateway: 97.107.143.1
    linode_id: 123
    prefix: 24
    public: true
    rdns: test.example.org
    region: us-east
    subnet_mask: 255.255.255.0
    type: ipv4
    vpc_nat_1_1:
      address: 139.144.244.36
      subnet_id: 194
      vpc_id: 242
  type: dict
"""


class ReverseDNSModule(LinodeModuleBase):
    """Module for updating Linode IP address's reverse DNS value"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "rdns"]
        self.results = {
            "changed": False,
            "actions": [],
            "ip": None,
        }
        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[["state", "present", ["rdns"]]],
        )

    @staticmethod
    def _build_default_rdns(
        address: str,
    ) -> Optional[str]:
        """
        Builds the default RDNS address for the given IPv4/IPv6 address.
        This is only used for local diffing purposes.
        """
        parsed_address = ip_address(address)

        # IPv6 addresses have no default RDNS
        if isinstance(parsed_address, IPv6Address):
            return None

        return f"{address.replace('.', '-')}.ip.linodeusercontent.com"

    def _should_update_rdns(
        self, old_rdns: str, new_rdns: Union[str, ExplicitNullValue]
    ) -> bool:
        """
        Returns whether the old RDNS value and the proposed new RDNS for the
        IP address differ.
        """

        # If the RDNS address is being reset, compare the old RDNS against
        # the Linode API default
        if isinstance(new_rdns, ExplicitNullValue):
            new_rdns = self._build_default_rdns(
                self.module.params.get("address")
            )

        return new_rdns != old_rdns

    def _attempt_update_rdns(self, rdns: Union[str, ExplicitNullValue]) -> None:
        """
        Update the reverse DNS of the IP address.
        """
        ip_str = self.module.params.get("address")
        ip_obj = self._get_resource_by_id(IPAddress, ip_str)

        old_rdns = ip_obj.rdns

        if self._should_update_rdns(old_rdns, rdns):
            ip_obj.rdns = rdns

            ip_obj.save()
            ip_obj._api_get()
            self.register_action(
                f"Updated reverse DNS of the IP address {ip_str} from {old_rdns} to {ip_obj.rdns}"
            )
        self.results["ip"] = ip_obj._raw_json

    def _handle_present(self) -> None:
        rdns = self.module.params.get("rdns")

        if not rdns:
            self.fail("`rdns` attribute is required to update the IP address")

        self._attempt_update_rdns(rdns)

    def _handle_absent(self) -> None:
        self._attempt_update_rdns(ExplicitNullValue())

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for reverse DNS module"""
        state = kwargs.get("state", "present")

        if state == "absent":
            self._handle_absent()
        else:
            self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the reverse DNS module"""
    ReverseDNSModule()


if __name__ == "__main__":
    main()
