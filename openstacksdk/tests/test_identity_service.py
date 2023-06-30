from django.test import TestCase

import openstack

openstack.enable_logging(debug=False)
conn = openstack.connect(cloud='oidev')


class TestClass(TestCase):
    def test01_유저_리스트조회(self):
        print("List Users:")

        for user in conn.identity.users():
            print(user)

    def test02_자격증명_리스트_조회(self):
        print("List Credentials:")

        for credential in conn.identity.credentials():
            print(credential)

    def test03_프로젝트_리스트_조회(self):
        print("List Projects:")

        for project in conn.identity.projects():
            print(project)

    def list_domains(conn):
        print("List Domains:")

        for domain in conn.identity.domains():
            print(domain)

    def list_groups(conn):
        print("List Groups:")

        for group in conn.identity.groups():
            print(group)

    def list_services(conn):
        print("List Services:")

        for service in conn.identity.services():
            print(service)

    def list_endpoints(conn):
        print("List Endpoints:")

        for endpoint in conn.identity.endpoints():
            print(endpoint)

    def list_regions(conn):
        print("List Regions:")

        for region in conn.identity.regions():
            print(region)

    def list_roles(conn):
        print("List Roles:")

        for role in conn.identity.roles():
            print(role)

    def list_role_domain_group_assignments(conn):
        print("List Roles assignments for a group on domain:")

        for role in conn.identity.role_domain_group_assignments():
            print(role)

    def list_role_domain_user_assignments(conn):
        print("List Roles assignments for a user on domain:")

        for role in conn.identity.role_project_user_assignments():
            print(role)

    def list_role_project_group_assignments(conn):
        print("List Roles assignments for a group on project:")

        for role in conn.identity.role_project_group_assignments():
            print(role)

    def list_role_project_user_assignments(conn):
        print("List Roles assignments for a user on project:")

        for role in conn.identity.role_project_user_assignments():
            print(role)
