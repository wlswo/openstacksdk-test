import time

from django.test import TestCase

import openstack
openstack.enable_logging(debug=False)
conn = openstack.connect(cloud='oidev')

EXAMPLE_IMAGE_NAME = 'FakeImage'


class TestClass(TestCase):
    def test01_images_조회(self):
        print("List Images:")

        for image in conn.image.images():
            print(image)

    def test02_images_생성(self):
        print("Upload Image...")

        # Load fake image data for the example.
        data = 'This is fake image data.'

        # Build the image attributes and upload the image.
        image_attrs = {
            'name': EXAMPLE_IMAGE_NAME,
            'data': data,
            'disk_format': 'raw',
            'container_format': 'bare',
            'visibility': 'public',
        }
        conn.image.upload_image(**image_attrs)
        time.sleep(1.5)
        self.assertNotEquals(None, conn.image.find_image(EXAMPLE_IMAGE_NAME))

    def test03_image_삭제(self):
        print("Delete Image...")

        example_image = conn.image.find_image(EXAMPLE_IMAGE_NAME)
        conn.image.delete_image(example_image, ignore_missing=False)

        time.sleep(1.5)
        self.assertEquals(None, conn.image.find_image(EXAMPLE_IMAGE_NAME))
