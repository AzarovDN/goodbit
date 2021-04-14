import random
import string
from pprint import pprint

import json
from django.views.generic import TemplateView

from .forms import GetParamsForm


class GeneratorCodeView(TemplateView):
    template_name = 'promocode/index.html'

    def get_context_data(self, **kwargs):
        context = super(GeneratorCodeView, self).get_context_data(**kwargs)
        form = GetParamsForm(self.request.GET or None)  # instance= None

        if form.is_valid():
            group_name = form.clean_group_name()
            amount = form.clean_amount()
            context['result'] = f'Для группы {group_name} сгенерировано {amount} кода и записаны в файл файл "ИМЯ"'
            form = GetParamsForm()

        context['form'] = form
        return context














