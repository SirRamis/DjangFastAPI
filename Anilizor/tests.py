from django.test import TestCase


def oper(2, 3, '+'):
    pass


class TestAnilizor(TestCase):
    # def setUp(self):
    #     super().self.response = self.client.get("/base1/")

    # def test_base(self):
    #     response = self.client.get("/base1/")
    #     self.assertEqual(response.status_code, 200)
    def test_1(self):
        r = oper(2,5,'+')
        self.assertEqual(7,r)