#!/bin/env python
#
# Create a volume and attach it to a instance.
#


import time

import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


def create_volume(zone, size):
    conn = boto.ec2.connect_to_region(region, 
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    volume_info = conn.create_volume(size, zone) 
    volume_id = volume_info.id

    time_init = 0
    time_total = 30
    time_interval = 1
    while time_init < time_total:
        volume_info.update()
        status = volume_info.status
        # print status
        if status == 'available':
            return volume_id
        else:
            time.sleep(time_interval)
            time_init += time_interval

    return False
    

def attach_volume(instance_id, volume_id, device):
    conn = boto.ec2.connect_to_region(region, 
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    result = conn.attach_volume(volume_id, instance_id, device)
    return True if result == "attaching" else False


if __name__ == "__main__":
    zone = "ap-southeast-1b"
    instance_ids = ["i-c0cb2f0d"]
    devices = ['/dev/sdx', '/dev/sdy', '/dev/sdz'] 
    size = "512"

    for instance_id in instance_ids:
        for device in devices:
            volume_id = create_volume(zone, size)
            if volume_id:
                print attach_volume(instance_id, volume_id, device)
            else:
                print "Create volume failed."