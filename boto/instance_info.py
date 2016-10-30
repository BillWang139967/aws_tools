#!/bin/env python


import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


conn = boto.ec2.connect_to_region(region, 
	aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
reservations = conn.get_all_instances()
for res in reservations:
    for instance in res.instances:
        if 'Name' in instance.tags:
            print "%s (%s) [%s] [%s] [%s] [%s]" % 
            	(instance.tags['Name'], instance.id, instance.state, 
            		instance.private_ip_address, instance.ip_address, instance.key_name)
        else:
            print "%s [%s] [%s] [%s] [%s]" % 
            	(instance.id, instance.state, instance.private_ip_address, 
            		instance.ip_address, instance.key_name)