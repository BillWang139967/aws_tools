#!/bin/env python


import boto3

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    if instance.tags:
        print "%s (%s) [%s] [%s] [%s] [%s]" % (instance.tags[0]['Value'], instance.id, instance.state["Name"], instance.private_ip_address, instance.public_ip_address, instance.key_name)
    else:
        print "%s [%s] [%s] [%s] [%s]" % (instance.id, instance.state["Name"], instance.private_ip_address, instance.public_ip_address, instance.key_name)
