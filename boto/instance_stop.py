#!/bin/env python


import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


conn = boto.ec2.connect_to_region(region, 
	aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

instance_list = ["i-a485228"]

conn.stop_instances(instance_ids=instance_list)