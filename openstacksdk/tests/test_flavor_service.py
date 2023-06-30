import time

from django.test import TestCase

import openstack

openstack.enable_logging(debug=False)
conn = openstack.connect(cloud='oidev')

FLAVOR_NAME = 'example_test_flavor'


class TestClass(TestCase):

    def test01_flavor_리스트_조회(self):
        print("Find Flavor:")

        for flavor in conn.compute.flavors():
            print(flavor)

    def test02_flavor_생성(self):
        print("Create Flavor:")

        conn.compute.create_flavor(
            name=FLAVOR_NAME,
            ram=1024,
            disk=10,
            vcpus=1
        )

        time.sleep(1)

        flavor = conn.compute.find_flavor(FLAVOR_NAME)
        self.assertNotEquals(None, flavor)

    def test03_flavor_삭제(self):
        print("Delete Flavor")

        example_flavor = conn.compute.find_flavor(FLAVOR_NAME)

        conn.compute.delete_flavor(example_flavor, ignore_missing=False)

        time.sleep(1)
        self.assertEquals(None, conn.compute.find_flavor(FLAVOR_NAME))
