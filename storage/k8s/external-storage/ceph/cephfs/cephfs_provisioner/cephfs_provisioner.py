#!/usr/bin/env python

import requests
import os
import getopt
import sys


class CephBaseDriver(object):
    base_url = os.environ["URL"]
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    create_url = base_url + "/api/cephfs"
    delete_url = base_url + "/api/cephfs"

    # noinspection PyMethodMayBeStatic
    def request_url(self, url, data):
        resp = requests.post(url, json=data)
        if resp.status_code != 200:
            raise Exception("[CephBaseDriver] request:{} failed.".format(url))
        return resp.json()

    def create_share(self, share, user, size):
        raise NotImplemented()

    def delete_share(self, share, user):
        raise NotImplemented()


class CephFsDriver(CephBaseDriver):
    def create_share(self, share, user, size):
        url = self.create_url
        data = {
            "share": share,
            "user": user,
            "size": size,
            "username": self.username,
            "password": self.password,
        }
        return self.request_url(url, data)

    def delete_share(self, share, user):
        url = self.delete_url
        data = {
            "share": share,
            "user": user,
            "username": self.username,
            "password": self.password,
        }
        return self.request_url(url, data)


def usage():
    print("Usage: " + sys.argv[0] + " --remove -n share_name -u ceph_user_id -s size")


def parse_params():
    share, user = str(), str()
    create = True
    size = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "rn:u:s:", ["remove"])
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-n':
            share = arg
        elif opt == '-u':
            user = arg
        elif opt == '-s':
            size = arg
        elif opt in ("-r", "--remove"):
            create = False
    if share == "" or user == "":
        usage()
        sys.exit(1)
    return share, user, size, create


def main():
    # 1.parse params
    share, user, size, create = parse_params()
    cephfs_driver = CephFsDriver()
    if create:
        print(cephfs_driver.create_share(share, user, size))
    else:
        cephfs_driver.delete_share(share, user)


if __name__ == "__main__":
    main()
