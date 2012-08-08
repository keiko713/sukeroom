#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.inclusion_tag('value.html')
def print_value(qa):
    if qa['answer_type'] == 1:
        # インプットボックス
        return {'qa': qa}

    choices = []
    cs = []
    if qa['answer_type'] == 2:
        # 可/不可/-
        cs = [u'可', u'不可', u'-']
    elif qa['answer_type'] == 3:
        # 有/無/-
        cs = [u'有', u'無', u'-']
    elif qa['answer_type'] == 4:
        # 必須/推奨/不要/-
        cs = [u'必須', u'推奨', u'不要', u'-']
    for c in cs:
        selected = False
        if qa['answer'] == c:
            selected = True
        else:
            if not qa['answer'] and c == u'-':
                selected = True
        choices.append({'value': c, 'selected': selected})

    return {'qa': qa, 'choices': choices}
