#!/bin/env python


import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


volume_info =  [{'device': u'/dev/sdc', 'volume_id': u'vol-93796f9c'}]
instance_id = "i-5435d299"

conn = boto.ec2.connect_to_region(region, 
	aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
reservations = conn.get_all_instances()

for i in volume_info:
    volume_id = i["volume_id"]
    device = i["device"]
    if 'sda' in device:
        continue

    curr_vol = conn.get_all_volumes([volume_id])[0]
    if curr_vol.status == 'available':
        conn.attach_volume(volume_id, instance_id, device)