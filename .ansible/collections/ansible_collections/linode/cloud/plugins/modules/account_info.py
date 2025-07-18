#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about the current Linode account."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.account_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Account",
        field_name="account",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-account",
        samples=docs.result_account_samples,
        get=lambda client, params: client.account()._raw_json,
    ),
)

SPECDOC_META = module.spec

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
- Get info about a Linode Account.
module: account_info
notes: []
options: {}
requirements:
- python >= 3
short_description: Get info about a Linode Account.
"""
EXAMPLES = r"""
- name: Get info about the current Linode account
  linode.cloud.account_info: {}
"""
RETURN = r"""
account:
  description: The returned Account.
  returned: always
  sample:
  - active_promotions:
    - credit_monthly_cap: '10.00'
      credit_remaining: '50.00'
      description: Receive up to $10 off your services every month for 6 months! Unused
        credits will expire once this promotion period ends.
      expire_dt: '2018-01-31T23:59:59'
      image_url: https://linode.com/10_a_month_promotion.svg
      service_type: all
      summary: $10 off your Linode a month!
      this_month_credit_remaining: '10.00'
    active_since: '2018-01-01T00:01:01'
    address_1: 123 Main Street
    address_2: Suite A
    balance: 200
    balance_uninvoiced: 145
    billing_source: akamai
    capabilities:
    - Linodes
    - NodeBalancers
    - Block Storage
    - Object Storage
    city: Philadelphia
    company: Linode LLC
    country: US
    credit_card:
      expiry: 11/2022
      last_four: 1111
    email: john.smith@linode.com
    euuid: E1AF5EEC-526F-487D-B317EBEB34C87D71
    first_name: John
    last_name: Smith
    phone: 215-555-1212
    state: PA
    tax_id: ATU99999999
    zip: 19102-1234
  type: dict
"""

if __name__ == "__main__":
    module.run()
