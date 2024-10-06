from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_page_endpoint(self):

        response = Client().get("/catalog/")

        self.assertEqual(response.status_code, 200, "ERROR-WRONG RESPONSE!")

    def test_catalog_page_detail_endpoint(self):

        response = Client().get("/catalog/1")

        self.assertEqual(response.status_code, 200, "ERROR-WRONG RESPONSE!")
