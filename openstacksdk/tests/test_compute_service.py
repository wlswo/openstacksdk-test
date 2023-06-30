import errno
import time

import openstack
import os
from django.test import TestCase

# Initialize and turn on debug logging
openstack.enable_logging(debug=False)

# Initialize connection
conn = openstack.connect(cloud='oidev')
PRIVATE_KEYPAIR_FILE = 'mykey2.pem'
SERVER_NAME = 'test2'


def is_Exist_Server(Server_Name):
    server = conn.compute.find_server(Server_Name)
    if server is None:
        return False
    else:
        return True


def create_keypair():
    keypair = conn.compute.find_keypair('mykey2')

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name='mykey3')

        print(keypair)

        try:
            os.mkdir('/Users/byun/Downloads')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(PRIVATE_KEYPAIR_FILE, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(PRIVATE_KEYPAIR_FILE, 0o400)

    return keypair


def wait_for_server_deletion(conn, server_id):
    time_out = 10
    cnt = 0
    while cnt <= 10:
        cnt += 1
        try:
            server = conn.compute.get_server(server_id)
        except Exception:
            break

        if server.status == 'DELETED':
            break

        time.sleep(1)  # 1초마다 상태 확인

    return server.status == 'DELETED'


class TestClass(TestCase):

    @classmethod  # 최초 실행
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

    # 각 Method 실행될 때마다 실행
    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")

    def test01_서버_개수_확인(self):
        # List the servers
        # for server in conn.compute.servers():
        #     json_formatted_str = json.dumps(server.to_dict()['instance_name'], indent=2)
        #     print(json_formatted_str)
        count = 0
        for _ in conn.compute.servers():
            count += 1
        print("VM Count : ", count)
        pass

    def test02_VM_생성(self):
        print("Create Server...")
        image = conn.image.find_image('cirros')
        flavor = conn.compute.find_flavor('m1.small')
        network = conn.network.find_network('private')
        keypair = create_keypair()

        server = conn.compute.create_server(
            name=SERVER_NAME,
            image_id=image.id,
            flavor_id=flavor.id,
            networks=[{"uuid": network.id}],
            key_name=keypair.name,
        )

        server = conn.compute.wait_for_server(server)

        print(
            "ssh -i {key} root@{ip}".format(
                key=PRIVATE_KEYPAIR_FILE, ip=server.access_ipv4
            )
        )
        self.assertEquals(True, is_Exist_Server(SERVER_NAME))

    def test03_VM_삭제(self):
        print("Delete Server:")

        server = conn.compute.find_server(SERVER_NAME)
        conn.compute.delete_server(server)

        self.assertEquals(False, wait_for_server_deletion(conn, server.id))

