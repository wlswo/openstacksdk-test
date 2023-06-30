import time

from django.test import TestCase

import openstack

openstack.enable_logging(debug=False)
conn = openstack.connect(cloud='oidev')

NETWORK_NAME = 'openstacksdk-example-project-subnet'


class TestClass(TestCase):

    def test01_네트워크_리스트_조회(self):
        print("List Networks:")

        for network in conn.network.networks():
            print(network)

    def test02_서브넷_리스트_조회(self):
        print("List Subnets:")

        for subnet in conn.network.subnets():
            print(subnet)

    def test03_포트_리스트_조회(self):
        print("List Ports:")

        for port in conn.network.ports():
            print(port)

    def test04_보안그룹_리스트_조회(self):
        print("List Security Groups:")

        for port in conn.network.security_groups():
            print(port)

    def test05_라우터_리스트_조회(self):
        print("List Routers:")

        for router in conn.network.routers():
            print(router)

    def test06_네트워크에이전트_리스트_조회(self):
        print("List Network Agents:")

        for agent in conn.network.agents():
            print(agent)

    def test07_네트워크_생성(self):
        print("Create Network:")

        example_network = conn.network.create_network(name=NETWORK_NAME)

        example_subnet = conn.network.create_subnet(
            name=NETWORK_NAME,
            network_id=example_network.id,
            ip_version='4',
            cidr='10.0.2.0/24',
            gateway_ip='10.0.2.1',
        )

        time.sleep(1)

        network = conn.network.find_network(NETWORK_NAME)
        self.assertNotEquals(None, network)

    def test08_네트워크_삭제(self):
        print("Delete Network:")

        example_network = conn.network.find_network(NETWORK_NAME)

        for example_subnet in example_network.subnet_ids:
            conn.network.delete_subnet(example_subnet, ignore_missing=False)

        conn.network.delete_network(example_network, ignore_missing=False)

        time.sleep(1)

        self.assertEquals(None, conn.network.find_network(NETWORK_NAME))
