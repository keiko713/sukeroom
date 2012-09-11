#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sukeroom.settings
import csv
import re
os.environ['DJANGO_SETTINGS_MODULE'] = 'sukeroom.settings'
from rooms.models import Company, Question, Answer

def sub_comma(arg):
    if arg.find(',') != -1:
        return re.sub(',', '', arg)
    return arg

def create_csv():
    data_writer = csv.writer(open('eggs.csv', 'wb'),
            quotechar='|', quoting=csv.QUOTE_NONE)
    data_writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    companies = Company.objects.all()
    questions = Question.objects.all().order_by('id')

    # first line, questions
    qs = [u'会社名']
    for question in questions:
        qs.append(sub_comma(question.question_sentence))
    data_writer.writerow([s.encode("utf-8") for s in qs])

    # after second line, answers
    for company in companies:
        answers = [sub_comma(company.company_name)]
        ans_list = Answer.objects.filter(
                    company=company).order_by('question__id')
        ans_idx = 0
        for q in questions:
            if ans_idx < len(ans_list) and q.id == ans_list[ans_idx].question.id:
                ans = ans_list[ans_idx]
                ans_idx += 1
            else:
                ans = Answer(answer=u'未回答')
            answers.append(sub_comma(ans.answer))

        data_writer.writerow([s.encode("utf-8") for s in answers])


if __name__ == '__main__':
    create_csv()
