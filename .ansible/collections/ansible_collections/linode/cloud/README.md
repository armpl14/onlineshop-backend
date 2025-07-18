# Linode Ansible Collection
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-linode.cloud-660198.svg?style=flat)](https://galaxy.ansible.com/linode/cloud/) 
![Tests](https://img.shields.io/github/actions/workflow/status/linode/ansible_linode/integration-tests.yml?branch=main)

The Ansible Linode Collection contains various plugins for managing Linode services.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

<!--start collection content-->
### Modules

Modules for managing Linode infrastructure.

Name | Description |
--- | ------------ |
[linode.cloud.api_request](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/api_request.md)|Make an arbitrary Linode API request.|
[linode.cloud.database_mysql](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_mysql.md)|Manage a Linode MySQL database.|
[linode.cloud.database_mysql_v2](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_mysql_v2.md)|Create, read, and update a Linode MySQL database.|
[linode.cloud.database_postgresql](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_postgresql.md)|Manage a Linode PostgreSQL database.|
[linode.cloud.database_postgresql_v2](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_postgresql_v2.md)|Create, read, and update a Linode PostgreSQL database.|
[linode.cloud.domain](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/domain.md)|Manage Linode Domains.|
[linode.cloud.domain_record](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/domain_record.md)|Manage Linode Domain Records.|
[linode.cloud.firewall](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/firewall.md)|Manage Linode Firewalls.|
[linode.cloud.firewall_device](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/firewall_device.md)|Manage Linode Firewall Devices.|
[linode.cloud.image](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/image.md)|Manage a Linode Image.|
[linode.cloud.instance](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/instance.md)|Manage Linode Instances, Configs, and Disks.|
[linode.cloud.ip](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ip.md)|Allocates a new IPv4 Address on your Account. The Linode must be configured to support additional addresses - please Open a support ticket requesting additional addresses before attempting allocation.|
[linode.cloud.ip_assign](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ip_assign.md)|Assign IPs to Linodes in a given Region.|
[linode.cloud.ip_rdns](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ip_rdns.md)|Manage a Linode IP address's rDNS.|
[linode.cloud.ip_share](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ip_share.md)|Manage the Linode shared IPs.|
[linode.cloud.lke_cluster](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/lke_cluster.md)|Manage Linode LKE clusters.|
[linode.cloud.lke_node_pool](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/lke_node_pool.md)|Manage Linode LKE cluster node pools.|
[linode.cloud.nodebalancer](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/nodebalancer.md)|Manage a Linode NodeBalancer.|
[linode.cloud.nodebalancer_node](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/nodebalancer_node.md)|Manage Linode NodeBalancer Nodes.|
[linode.cloud.nodebalancer_stats](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/nodebalancer_stats.md)|Get info about a Linode Node Balancer Stats.|
[linode.cloud.object_keys](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/object_keys.md)|Manage Linode Object Storage Keys.|
[linode.cloud.placement_group](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/placement_group.md)|Manage a Linode Placement Group.|
[linode.cloud.placement_group_assign](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/placement_group_assign.md)|Manages a single assignment between a Linode and a Placement Group.|
[linode.cloud.ssh_key](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ssh_key.md)|Manage a Linode SSH key.|
[linode.cloud.stackscript](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/stackscript.md)|Manage a Linode StackScript.|
[linode.cloud.token](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/token.md)|Manage a Linode Token.|
[linode.cloud.user](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/user.md)|Manage a Linode User.|
[linode.cloud.volume](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/volume.md)|Manage a Linode Volume.|
[linode.cloud.vpc](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc.md)|Create, read, and update a Linode VPC.|
[linode.cloud.vpc_subnet](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc_subnet.md)|Create, read, and update a Linode VPC Subnet.|


### Info Modules

Modules for retrieving information about existing Linode infrastructure.

Name | Description |
--- | ------------ |
[linode.cloud.account_availability_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/account_availability_info.md)|Get info about a Linode Account Availability.|
[linode.cloud.account_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/account_info.md)|Get info about a Linode Account.|
[linode.cloud.child_account_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/child_account_info.md)|Get info about a Linode Child Account.|
[linode.cloud.database_mysql_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_mysql_info.md)|Get info about a Linode MySQL Managed Database.|
[linode.cloud.database_postgresql_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_postgresql_info.md)|Get info about a Linode PostgreSQL Managed Database.|
[linode.cloud.domain_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/domain_info.md)|Get info about a Linode Domain.|
[linode.cloud.domain_record_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/domain_record_info.md)|Get info about a Linode Domain Records.|
[linode.cloud.firewall_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/firewall_info.md)|Get info about a Linode Firewall.|
[linode.cloud.image_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/image_info.md)|Get info about a Linode Image.|
[linode.cloud.instance_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/instance_info.md)|Get info about a Linode Instance.|
[linode.cloud.ip_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ip_info.md)|Get info about a Linode IP.|
[linode.cloud.ipv6_range_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ipv6_range_info.md)|Get info about a Linode IPv6 range.|
[linode.cloud.lke_cluster_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/lke_cluster_info.md)|Get info about a Linode LKE cluster.|
[linode.cloud.lke_version_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/lke_version_info.md)|Get info about a Linode LKE Version.|
[linode.cloud.nodebalancer_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/nodebalancer_info.md)|Get info about a Linode Node Balancer.|
[linode.cloud.object_cluster_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/object_cluster_info.md)|**NOTE: This module has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**|
[linode.cloud.placement_group_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/placement_group_info.md)|Get info about a Linode Placement Group.|
[linode.cloud.profile_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/profile_info.md)|Get info about a Linode Profile.|
[linode.cloud.region_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/region_info.md)|Get info about a Linode Region.|
[linode.cloud.ssh_key_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ssh_key_info.md)|Get info about a Linode SSH Key.|
[linode.cloud.stackscript_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/stackscript_info.md)|Get info about a Linode StackScript.|
[linode.cloud.token_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/token_info.md)|Get info about a Linode Personal Access Token.|
[linode.cloud.type_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/type_info.md)|Get info about a Linode Type.|
[linode.cloud.user_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/user_info.md)|Get info about a Linode User.|
[linode.cloud.vlan_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vlan_info.md)|Get info about a Linode VLAN.|
[linode.cloud.volume_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/volume_info.md)|Get info about a Linode Volume.|
[linode.cloud.vpc_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc_info.md)|Get info about a Linode VPC.|
[linode.cloud.vpc_subnet_info](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc_subnet_info.md)|Get info about a Linode VPC Subnet.|


### List Modules

Modules for retrieving and filtering on multiple Linode resources.

Name | Description |
--- | ------------ |
[linode.cloud.account_availability_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/account_availability_list.md)|List and filter on Account Availabilities.|
[linode.cloud.child_account_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/child_account_list.md)|List and filter on Child Account.|
[linode.cloud.database_engine_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_engine_list.md)|List and filter on Managed Database engine types.|
[linode.cloud.database_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/database_list.md)|List and filter on Linode Managed Databases.|
[linode.cloud.domain_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/domain_list.md)|List and filter on Domains.|
[linode.cloud.event_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/event_list.md)|List and filter on Events.|
[linode.cloud.firewall_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/firewall_list.md)|List and filter on Firewalls.|
[linode.cloud.image_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/image_list.md)|List and filter on Images.|
[linode.cloud.instance_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/instance_list.md)|List and filter on Instances.|
[linode.cloud.instance_type_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/instance_type_list.md)|**NOTE: This module has been deprecated in favor of `type_list`.**|
[linode.cloud.lke_type_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/lke_type_list.md)|List and filter on LKE Types.|
[linode.cloud.lke_version_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/lke_version_list.md)|List and filter on LKE Versions.|
[linode.cloud.network_transfer_prices_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/network_transfer_prices_list.md)|List and filter on Network Transfer Prices.|
[linode.cloud.nodebalancer_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/nodebalancer_list.md)|List and filter on Node Balancers.|
[linode.cloud.nodebalancer_type_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/nodebalancer_type_list.md)|List and filter on Node Balancer Types.|
[linode.cloud.object_cluster_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/object_cluster_list.md)|**NOTE: This module has been deprecated because it relies on deprecated API endpoints. Going forward, `region` will be the preferred way to designate where Object Storage resources should be created.**|
[linode.cloud.object_storage_endpoint_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/object_storage_endpoint_list.md)|List and filter on Object Storage Endpoints.|
[linode.cloud.placement_group_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/placement_group_list.md)|List and filter on Placement Groups.|
[linode.cloud.region_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/region_list.md)|List and filter on Regions.|
[linode.cloud.ssh_key_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/ssh_key_list.md)|List and filter on SSH Keys.|
[linode.cloud.stackscript_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/stackscript_list.md)|List and filter on StackScripts.|
[linode.cloud.token_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/token_list.md)|List and filter on Tokens.|
[linode.cloud.type_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/type_list.md)|List and filter on Types.|
[linode.cloud.user_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/user_list.md)|List and filter on Users.|
[linode.cloud.vlan_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vlan_list.md)|List and filter on VLANs.|
[linode.cloud.volume_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/volume_list.md)|List and filter on Linode Volumes.|
[linode.cloud.volume_type_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/volume_type_list.md)|List and filter on Volume Types.|
[linode.cloud.vpc_ip_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc_ip_list.md)|List and filter on VPC IP Addresses.|
[linode.cloud.vpc_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc_list.md)|List and filter on VPCs.|
[linode.cloud.vpc_subnet_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpc_subnet_list.md)|List and filter on VPC Subnets.|
[linode.cloud.vpcs_ip_list](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/modules/vpcs_ip_list.md)|List and filter on all VPC IP Addresses.|


### Inventory Plugins

Dynamically add Linode infrastructure to an Ansible inventory.

Name |
--- |
[linode.cloud.instance](https://github.com/linode/ansible_linode/blob/v0.37.1/docs/inventory/instance.md)|


<!--end collection content-->

## Installation

You can install the Linode collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install linode.cloud
```

The Python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```shell
pip install --upgrade -r https://raw.githubusercontent.com/linode/ansible_linode/v0.37.1/requirements.txt
```

> :warning: **NOTE:** Python dependencies should always be reinstalled when upgrading collection versions

## Usage
Once the Linode Ansible collection is installed, it can be referenced by its [Fully Qualified Collection Namespace (FQCN)](https://github.com/ansible-collections/overview#terminology): `linode.cloud.module_name`.

In order to use this collection, the `LINODE_API_TOKEN` environment variable must be set to a valid Linode API v4 token. 
Alternatively, you can pass your Linode API v4 token into the `api_token` option for each Linode module you reference.

The `LINODE_UA_PREFIX` environment variable or the `ua_prefix` module option can be used to specify a custom User-Agent prefix.

The `LINODE_API_URL` environment variable pr the `api_url` module option can be used to specify a custom API base url.

#### Example Playbook
```yaml
---
- name: create linode instance
  hosts: localhost
  tasks:
    - name: Create a Linode instance    
      linode.cloud.instance:
        label: my-linode
        type: g6-nanode-1
        region: us-east
        image: linode/ubuntu22.04
        root_pass: verysecurepassword!!!
        state: present
```

For more information on Ansible collection usage, see [Ansible's official usage guide](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html).

## Examples

Use-case examples for this collection can be found [here](./examples/README.md).

## Development

The following section outlines various information relating to the development of this collection.

### Attaching a Debugger

To quickly and easily attach a debugger to a running module in this collection, 
you can use the [madbg](https://pypi.org/project/madbg/) package:

1. Install `madbg` in your local Python environment:

```shell
pip install madbg
```

2. Call `madbg.set_trace(...)` at the location you would like to create a breakpoint at:

```shell
import madbg; madbg.set_trace()
```

3. Run the module in either a playbook or a test.
4. In a separate shell, run `madbg connect`.
5. You should now be able to remotely debug the module as soon as the breakpoint is triggered.

## Licensing

GNU General Public License v3.0.

See [COPYING](COPYING) to see the full text.