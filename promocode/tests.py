import json
import os
from pprint import pprint
from django.test import Client

from django.test import TestCase

from .views import generating_codes


class GeneratorCodeViewTest(TestCase):

    def test_create_promocode(self):

        # очищаю файл
        with open('test_promocode.json', 'w', encoding='utf8') as promo_code_file:
            json_dict = {}
            json.dump(json_dict, promo_code_file, indent=4)

        checking_list = [(10, 'агенства'), (1, 'агенства'), (42, 'автостоп'), (5, 1)]
        for i in checking_list:
            generating_codes(i[1], i[0], 'test_promocode.json')

        with open('test_promocode.json') as promo_code_file:
            json_dict = json.load(promo_code_file)
            keys = json_dict.keys()
            values = json_dict.values()
            counter = 0
            for value in values:
                counter += len(value)

        self.assertIs(list(keys) == ['агенства', 'автостоп', '1'], True)
        self.assertIs(counter == 58, True)


class CheckingViewTest(TestCase):

    def test_checking_non_existent_promocode(self):
        client = Client()
        response = client.get('/checking/', {'promocode': 'johwn'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'код не существует')

    def test_checking_existent_promocode(self):
        client = Client()
        promocode = ''

        if os.path.isfile('promocode.json'):
            if os.path.getsize('promocode.json') != 0:
                with open('promocode.json') as promo_code_file:
                    json_dict = json.load(promo_code_file)
                    values = list(json_dict.values())
                    promocode = values[0]
                    response = client.get('/checking/', {'promocode': promocode})
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, 'код существует группа =')
        else:
            self.assertIs(False, True, msg='Для работы теста нужен файл promocode.json с сгенерированными кодами')





