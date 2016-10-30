#!/bin/env python


import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


volume_info =  [{'device': u'/dev/sdc', 'volume_id': u'vol-a47f96aa'}]
instance_id = "i-2fbd3a07"


conn = boto.ec2.connect_to_region(region, 
    aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

for i in volume_info:
    volume_id = i["volume_id"]
    device = i["device"] 

    curr_vol = conn.get_all_volumes([volume_id])[0]
    if curr_vol.status == 'in-use':
        print volume_id, device
        if 'sda' in device:
            continue
        try:
            print conn.detach_volume(volume_id, instance_id, device)
        except Exception, e:
            print e