#!/bin/env python
#
# Create a image from a instance, and create some new instances from the image.
#


import time
import requests
from multiprocessing.dummy import Pool as ThreadPool


import boto.ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType
from boto.ec2.networkinterface import NetworkInterfaceSpecification, NetworkInterfaceCollection


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


def create_ami(instance_id, name):
    conn = boto.ec2.connect_to_region(region, 
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    image_id= conn.create_image(instance_id, name, no_reboot=True, block_device_mapping=None)
    # print image_id
    image_ids = [image_id]
    # print image_ids

    time.sleep(3)
    image_object = conn.get_all_images(image_ids=image_ids)[0]
    # print image_object.__dict__

    time_init = 0
    time_total = 300
    time_interval = 3
    while time_init < time_total:
        image_object.update()
        print image_object.state
        if image_object.state == 'available':
            return image_id
        else:
            time.sleep(time_interval)
            time_init += time_interval
    return False


def instance_info(instance_id):
    conn = boto.ec2.connect_to_region(region, 
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    instance_ids = [instance_id]
    reservations = conn.get_all_instances(instance_ids=instance_ids)
    for res in reservations:
        for instance in res.instances:
            subnet_id = instance.subnet_id
            key_name = instance.key_name
            instance_type = instance.instance_type
            sg_id = instance.interfaces[0].groups[0].id

            _dict = {'subnet_id': subnet_id,
                'key_name': key_name,
                'instance_type': instance_type,
                'sg_id': sg_id
            }
            return _dict


def create_instance(create_list):
    region = create_list["region"]
    subnet_id = create_list["subnet_id"]
    ami_id = create_list["ami_id"]
    key_name = create_list["key_name"]
    instance_type = create_list["instance_type"]
    sg_id = create_list["sg_id"]
    user_data = create_list["user_data"]
    usage = create_list["usage"]
 
    #############################
    # some user_data oper here
    #############################
 
    network_interface = NetworkInterfaceSpecification(subnet_id=subnet_id,groups=[sg_id])
    network_interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(network_interface)
 
    conn = boto.ec2.connect_to_region(region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
        reservation = conn.run_instances(ami_id,
        key_name=key_name,
        network_interfaces=network_interfaces,
        instance_type=instance_type,
        min_count=1,
        max_count=1,
        user_data=user_data
    )   
 
    instance = reservation.instances[0]
 
    time_init = 0
    time_total = 300
    time_interval = 5
    while time_init < time_total:
        status = instance.update()
        if status == 'running':
            instance.add_tag("Name",hostname)
            break
        else:
            time.sleep(time_interval)
            time_init += time_interval
 
    create_list["instance_id"] = str(instance).split(":")[-1]
    create_list["placement"] = instance.placement
    create_list["status"] = instance.update()
    create_list["hostname"] = hostname
 
    return create_list



def create_instances(region, instance_id, num, usage):
    ret = requests.get(clone_install_script)
    user_data = ret.text
 
    _time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    name = "{0}-{1}".format(instance_id, _time)
    ami_id = create_ami(region, instance_id, name)
    if not ami_id:
       return False
 
    _instance_info = instance_info(region, instance_id)
    create_list = {
        "region": region,
        "subnet_id": _instance_info["subnet_id"],
        "instance_type": _instance_info["instance_type"],
        "key_name": _instance_info["key_name"],
        "sg_id": _instance_info["sg_id"],
        "ami_id": ami_id,
        "user_data": user_data,
        "usage": usage
    }
 
    create_lists = list()
    for i in xrange(num):
        create_lists.append(create_list)
 
    pool = ThreadPool(100)
 
    create_results = pool.map(create_instances, create_lists)
 
    pool.close()
    pool.join()
 
    return create_results


def main():
    print create_instances("ap-southeast-1", "i-22sdf234", 10, "test")


if __name__ == '__main__':
    main()