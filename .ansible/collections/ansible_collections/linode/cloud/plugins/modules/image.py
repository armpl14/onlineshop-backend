#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Images."""

from __future__ import absolute_import, division, print_function

import os
from typing import Any, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs
import polling
import requests
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
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Image

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This Image's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this Image."],
    ),
    "cloud_init": SpecField(
        type=FieldType.bool,
        description=["Whether this image supports cloud-init."],
        default=False,
    ),
    "description": SpecField(
        type=FieldType.string,
        editable=True,
        description=["A description for the Image."],
    ),
    "disk_id": SpecField(
        type=FieldType.integer,
        conflicts_with=["source_file"],
        description=["The ID of the disk to clone this image from."],
    ),
    "recreate": SpecField(
        type=FieldType.bool,
        default=False,
        description=[
            "If true, the image with the given label will be deleted and recreated"
        ],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The Linode region to upload this image to."],
        default="us-east",
    ),
    "source_file": SpecField(
        type=FieldType.string,
        conflicts_with=["disk_id"],
        description=["An image file to create this image with."],
    ),
    "wait": SpecField(
        type=FieldType.bool,
        default=True,
        description=[
            "Wait for the image to have status `available` before returning."
        ],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        default=600,
        description=[
            "The amount of time, in seconds, to wait for an image to "
            "have status `available`."
        ],
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=["A list of customized tags of this new Image."],
    ),
    # `regions` send to API for image replication
    "replica_regions": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "A list of regions that customer wants to replicate this image in. "
            "At least one available region must be provided and only core regions allowed. "
            "Existing images in the regions not passed will be removed. ",
        ],
    ),
    "wait_for_replications": SpecField(
        type=FieldType.bool,
        default=False,
        description=[
            "Wait for the all the replications `available` before returning."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode Image."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "image": SpecReturnValue(
            description="The Image in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-image",
            type=FieldType.dict,
            sample=docs.result_image_samples,
        )
    },
)

MUTABLE_FIELDS = {"description", "tags"}

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
- Manage a Linode Image.
module: image
notes: []
options:
  cloud_init:
    default: false
    description:
    - Whether this image supports cloud-init.
    required: false
    type: bool
  description:
    description:
    - A description for the Image.
    required: false
    type: str
  disk_id:
    description:
    - The ID of the disk to clone this image from.
    required: false
    type: int
  label:
    description:
    - This Image's unique label.
    required: true
    type: str
  recreate:
    default: false
    description:
    - If true, the image with the given label will be deleted and recreated
    required: false
    type: bool
  region:
    default: us-east
    description:
    - The Linode region to upload this image to.
    required: false
    type: str
  replica_regions:
    description:
    - 'A list of regions that customer wants to replicate this image in. At least
      one available region must be provided and only core regions allowed. Existing
      images in the regions not passed will be removed. '
    elements: str
    required: false
    type: list
  source_file:
    description:
    - An image file to create this image with.
    required: false
    type: str
  state:
    choices:
    - present
    - absent
    description:
    - The state of this Image.
    required: true
    type: str
  tags:
    description:
    - A list of customized tags of this new Image.
    elements: str
    required: false
    type: list
  wait:
    default: true
    description:
    - Wait for the image to have status `available` before returning.
    required: false
    type: bool
  wait_for_replications:
    default: false
    description:
    - Wait for the all the replications `available` before returning.
    required: false
    type: bool
  wait_timeout:
    default: 600
    description:
    - The amount of time, in seconds, to wait for an image to have status `available`.
    required: false
    type: int
requirements:
- python >= 3
short_description: Manage a Linode Image.
"""
EXAMPLES = r"""
- name: Create a basic image from an existing disk
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    tags:
    - test
    state: present
- name: Create a basic image from a file
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    source_file: myimage.img.gz
    tags:
    - test
    state: present
- name: Replicate an image
  linode.cloud.image:
    label: my-image
    description: Created using Ansible!
    disk_id: 12345
    tags:
    - test
    replica_regions:
    - us-east
    - us-central
    state: present
- name: Delete an image
  linode.cloud.image:
    label: my-image
    state: absent
"""
RETURN = r"""
image:
  description: The Image in JSON serialized form.
  returned: always
  sample:
  - capabilities: []
    created: '2021-08-14T22:44:02'
    created_by: my-account
    deprecated: false
    description: Example Image description.
    eol: '2026-07-01T04:00:00'
    expiry: null
    id: private/123
    is_public: true
    label: my-image
    regions:
    - region: us-east
      status: available
    - region: us-central
      status: pending
    size: 2500
    status: null
    tags:
    - test
    total_size: 5000
    type: manual
    updated: '2021-08-14T22:44:02'
    vendor: Debian
  type: dict
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Images"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "image": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("state", "label")],
            mutually_exclusive=[("disk_id", "source_file")],
            required_if=[
                ("state", "present", ["disk_id", "source_file"], True)
            ],
        )

    def _get_image_by_label(self, label: str) -> Optional[Image]:
        try:
            return self.client.images(Image.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get image {0}: {1}".format(label, exception)
            )

    def _wait_for_image_status(self, image: Image, status: Set[str]) -> None:
        def poll_func() -> bool:
            image._api_get()
            return image.status in status

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=self._timeout_ctx.seconds_remaining,
            )
        except polling.TimeoutException:
            self.fail("failed to wait for image status: timeout period expired")

    def _wait_for_image_replication_status(
        self, image: Image, status: Set[str]
    ) -> None:
        def poll_func() -> bool:
            image._api_get()
            for region in image.regions:
                if region.status not in status:
                    return False

            return True

        # Initial attempt
        if poll_func():
            return

        try:
            polling.poll(
                poll_func,
                step=10,
                timeout=self._timeout_ctx.seconds_remaining,
            )
        except polling.TimeoutException:
            self.fail(
                "failed to wait for image replication status: timeout period expired"
            )

    def _create_image_from_disk(self) -> Optional[Image]:
        disk_id = self.module.params.get("disk_id")
        label = self.module.params.get("label")
        description = self.module.params.get("description")
        cloud_init = self.module.params.get("cloud_init")
        tags = self.module.params.get("tags")

        try:
            return self.client.images.create(
                disk_id,
                label=label,
                description=description,
                cloud_init=cloud_init,
                tags=tags,
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create image: {0}".format(exception)
            )

    def _create_image_from_file(self) -> Optional[Image]:
        label = self.module.params.get("label")
        description = self.module.params.get("description")
        region = self.module.params.get("region")
        source_file = self.module.params.get("source_file")
        cloud_init = self.module.params.get("cloud_init")
        tags = self.module.params.get("tags")

        if not os.path.exists(source_file):
            return self.fail(
                msg="source file {0} does not exist".format(source_file)
            )

        # Create an image upload
        try:
            image, upload_to = self.client.images.create_upload(
                label,
                region,
                description=description,
                cloud_init=cloud_init,
                tags=tags,
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create image upload: {0}".format(exception)
            )

        try:
            with open(source_file, "rb") as file:
                # We want to stream the image
                requests.put(
                    upload_to,
                    headers={"Content-Type": "application/octet-stream"},
                    data=file,
                )

        except Exception as exception:
            return self.fail(
                msg="failed to upload image: {0}".format(exception)
            )

        image = Image(self.client, image.id, json=image._raw_json)
        return image

    def _create_image(self) -> Optional[Image]:
        if self.module.params.get("disk_id") is not None:
            return self._create_image_from_disk()

        if self.module.params.get("source_file") is not None:
            return self._create_image_from_file()

        return self.fail(msg="no handler found for image")

    def _update_image(self, image: Image) -> None:
        image._api_get()

        params = filter_null_values(self.module.params)

        handle_updates(image, params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get("label")

        image = self._get_image_by_label(label)

        if params.get("recreate") and image is not None:
            image.delete()
            self.register_action("Deleted image {0}".format(label))
            image = None

        # Create the image if it does not already exist
        if image is None:
            image = self._create_image()
            self.register_action("Created image {0}".format(label))

            if self.module.params.get("wait"):
                self._wait_for_image_status(image, {"available"})

        self._update_image(image)

        replica_regions = params.get("replica_regions")
        new_regions: list = [] if replica_regions is None else replica_regions
        old_regions = [r.region for r in image.regions]

        # Replicate image in new regions
        if replica_regions is not None and new_regions != old_regions:
            if len(new_regions) == 0 or (
                not set(new_regions) & set(old_regions)
            ):
                return self.fail(
                    msg="failed to replicate image {0}: replica_regions value {1} is invalid. "
                    "At least one available region must be provided.".format(
                        label, new_regions
                    )
                )

            image.replicate(new_regions)
            self.register_action(
                "Replicated image {0} in regions {1}".format(label, new_regions)
            )

            if params.get("wait_for_replications"):
                self._wait_for_image_replication_status(image, {"available"})

        # Force lazy-loading
        image._api_get()

        self.results["image"] = image._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        image = self._get_image_by_label(label)

        if image is not None:
            self.results["image"] = image._raw_json
            image.delete()
            self.register_action("Deleted image {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Image module"""

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Image module"""
    Module()


if __name__ == "__main__":
    main()
