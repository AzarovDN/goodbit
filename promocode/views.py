import os

import random
import string

import json
from django.views.generic import TemplateView

from .forms import GetParamsForm, CheckingForm


class GeneratorCodeView(TemplateView):
    template_name = 'promocode/index.html'

    def get_context_data(self, **kwargs):
        context = super(GeneratorCodeView, self).get_context_data(**kwargs)
        form = GetParamsForm(self.request.GET or None)  # instance= None

        if form.is_valid():
            group_name = form.clean_group_name()
            amount = form.clean_amount()
            context['result'] = f'Для группы {group_name} сгенерировано {amount} кода'
            form = GetParamsForm()
            generating_codes(group_name, amount)

        context['form'] = form
        return context


class CheckingView(TemplateView):

    template_name = 'promocode/checking.html'

    def get_context_data(self, **kwargs):
        context = super(CheckingView, self).get_context_data(**kwargs)
        form = CheckingForm(self.request.GET or None)  # instance= None

        if form.is_valid():
            promocode = form.clean_promocode()
            result = 'код не существует'
            if os.path.isfile('promocode.json'):
                if os.path.getsize('promocode.json') != 0:
                    with open('promocode.json') as promo_code_file:
                        json_dict = json.load(promo_code_file)
                        for key, value in json_dict.items():
                            if promocode in value:
                                result = f'код существует группа = {key}'

            context['result'] = result
            form = CheckingForm()

        context['form'] = form
        return context


def generating_codes(group_name, amount, file_name='promocode.json'):
    promocode_list = []
    current_list = []
    letters_and_digits = string.ascii_letters + string.digits

    # создаю список всех промокодов для проверки на повторный промокод
    if os.path.isfile(file_name):
        if os.path.getsize(file_name) != 0:
            with open(file_name) as promo_code_file:
                json_dict = json.load(promo_code_file)
                for _, value in json_dict.items():
                    current_list += value

    for i in range(amount):
        flag = True
        promo_code = ''
        # Проверяю промокод нет ли повторяющихся промокодов
        while flag:
            promo_code = ''.join(random.sample(letters_and_digits, 5))
            flag = promo_code in current_list
        promocode_list.append(promo_code)
    get_json(str(group_name), promocode_list, file_name)


def get_json(group_name, promocode_list, file_name):
    flag = True
    json_dict = {}

    # Беру данные из файла, если они есть
    if os.path.isfile(file_name):
        if os.path.getsize(file_name) != 0:
            flag = False
            with open(file_name) as promo_code_file:
                json_dict = json.load(promo_code_file)

    with open(file_name, 'w', encoding='utf8') as promo_code_file:
        if flag:
            json_dict = {group_name: promocode_list}
            json.dump(json_dict, promo_code_file, indent=4)
        else:
            if json_dict.get(group_name):
                json_dict[group_name] = json_dict[group_name] + promocode_list
                json.dump(json_dict, promo_code_file, indent=4)
            else:
                json_dict[group_name] = promocode_list
                json.dump(json_dict, promo_code_file, indent=4)



