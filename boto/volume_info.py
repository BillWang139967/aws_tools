#!/bin/env python
#
# Get volume info of instances.
#


import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


instance_list = ['muce-hdc1']

conn = boto.ec2.connect_to_region(region, 
    aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
reservations = conn.get_all_instances()

for res in reservations:
    for instance in res.instances:
        if 'Name' in instance.tags:
            if instance.tags['Name'] in instance_list:
                volume_list = []
                for i in instance.block_device_mapping:
                    volume_dict = {}
                    volume_dict["device"] = i
                    volume_dict["volume_id"] = instance.block_device_mapping.get(i).volume_id
                    volume_list.append(volume_dict)

                print "%s (%s) [%s]:\n %s" % (instance.tags['Name'], instance.id, instance.state, volume_list)
                print 