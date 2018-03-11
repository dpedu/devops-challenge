# BONUS.md

*you can't see me*

## Cloudformation

This repository offers an AWS Cloudformation template, capable of creating a single-region vpc-based EC2 Container
Service installation of the app!

## Parameters

The parameters required for the Cloudformation template are simple:

- `KeyName` - An existing keypair to authorize access into the ECS instances
- `VpcId` - An existing VPC ID the ECS instances will be launched into
- `SubnetId` - 2 subnet IDs within the above VPC the ECS instances will be attached to
- `Region` - Region for the deployment
- `DesiredCapacity` - How many app instances to run
- `MaxSize` - Maximum number of app instances to run
- `InstanceType` - Size of ECS instances such as `m3.medium`

## Setup

Simply create a new Cloudformation stack from `cloudformation.template` at the root of the repo. After the stack is
built, the output `ECSALB` will contain the URL of an Elastic Load Balancer sitting in front of the containers.
