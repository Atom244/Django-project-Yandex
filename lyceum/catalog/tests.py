from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_page_endpoint(self):

        normal_catalog_check = Client().get("/catalog/")
        self.assertEqual(normal_catalog_check.status_code, 200,
                         "normal_catalog_check down")

        wrong_catalog_check = Client().get("/catalogE/")
        self.assertEqual(wrong_catalog_check.status_code, 404,
                         "wrong_catalog_check down")

    def test_catalog_page_detail_endpoint(self):

        normal_num_check = Client().get("/catalog/1/")
        self.assertEqual(normal_num_check.status_code, 200,
                         "normal_num_check down")

        negative_num_check = Client().get("/catalog/-1/")
        self.assertEqual(negative_num_check.status_code, 404,
                         "negative_num_check down")

        float_num_check = Client().get("/catalog/1.5/")
        self.assertEqual(float_num_check .status_code, 404,
                         "float_num_check down")

    def test_catalog_reg_path(self):

        normal_num_check = Client().get("/catalog/re/1/")
        self.assertEqual(normal_num_check.status_code, 200,
                         "normal_num_check down")

        negative_num_check = Client().get("/catalog/re/-1/")
        self.assertEqual(negative_num_check.status_code, 404,
                         "negative_num_check down")

        float_num_check = Client().get("/catalog/re/1.5/")
        self.assertEqual(float_num_check .status_code, 404,
                         "float_num_check down")

    def test_catalog_converter_path(self):

        normal_num_check = Client().get("/catalog/converter/1/")
        self.assertEqual(normal_num_check.status_code, 200,
                         "normal_num_check down")

        negative_num_check = Client().get("/catalog/converter/-1/")
        self.assertEqual(negative_num_check.status_code, 404,
                         "negative_num_check down")

        float_num_check = Client().get("/catalog/converter/1.5/")
        self.assertEqual(float_num_check .status_code, 404,
                         "float_num_check down")
