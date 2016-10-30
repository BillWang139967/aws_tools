#!/bin/env python


import time
import sys
import copy

import boto.ec2


region = ""
aws_access_key_id = ""
aws_secret_access_key = ""


def stop_instance(instance_list):
    conn = boto.ec2.connect_to_region(region,
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    if instance_list == []:
        return True

    conn.stop_instances(instance_ids=instance_list)

    _dict = {}
    reservations = conn.get_all_instances()
    for res in reservations:
        for instance in res.instances:
            if instance.id in instance_list:
                _dict[instance.id] = instance

    time_init = 0
    time_total = 60
    time_interval = 1
    tmp_list = copy.deepcopy(instance_list)
    while time_init < time_total:
        if tmp_list == []:
            break

        for _id in instance_list:
            _instance = _dict.get(_id)
            status = _instance.update()
            if status == 'stopped':
                tmp_list.remove(_id)

        time.sleep(time_interval)
        time_init += time_interval
        # print time_init

    if tmp_list == []:
        return True
    else:
        return tmp_list


def modify_instance_type(instance_list, instance_type):
    conn = boto.ec2.connect_to_region(region,
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    if instance_list == []:
        return True

    _dict = {}
    for _id in instance_list:
        ret = conn.modify_instance_attribute(_id, "instanceType", instance_type)
        _dict[_id] = ret

        if not ret:
            status = False

    if "status" in dir():
        return _dict
    else:
        return True


def start_instance(instance_list):
    conn = boto.ec2.connect_to_region(region,
        aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    if instance_list == []:
        return True

    conn.start_instances(instance_ids=instance_list)

    _dict = {}
    reservations = conn.get_all_instances()
    for res in reservations:
        for instance in res.instances:
            if instance.id in instance_list:
                _dict[instance.id] = instance

    time_init = 0
    time_total = 60
    time_interval = 1
    tmp_list = copy.deepcopy(instance_list)
    while time_init < time_total:
        if tmp_list == []:
            break

        for _id in instance_list:
            _instance = _dict.get(_id)
            status = _instance.update()
            if status == 'running':
                tmp_list.remove(_id)

        time.sleep(time_interval)
        time_init += time_interval

    if tmp_list == []:
        return True
    else:
        return tmp_list


def main():
    # print sys.argv[1]
    instance_list = ["%s" % sys.argv[1] ]
    print instance_list
    instance_type = "c3.2xlarge"

    stop_status = stop_instance(instance_list)
    print "stop status: {0}".format(stop_status)
    if stop_status:
        modify_status = modify_instance_type(instance_list, instance_type)
        print "modify status: {0}".format(modify_status)
        if modify_status:
            start_status = start_instance(instance_list)
            if start_status:
                print "start status: {0}".format(start_status)


if __name__ == '__main__':
    main()