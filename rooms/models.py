#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models

QUESTION_CATEGORY_CHOICES = (
    (1, 'メール・通信|MailNetwork'),
    (2, 'Web閲覧・ソフトウェア規制|WebSoftware'),
    (3, '社内システム|CorpSystem'),
    (4, '働く環境|Environment'),
)

ANSWER_TYPE_CHOICES = (
    (1, 'インプットボックス'),
    (2, '可/不可セレクトボックス'),
    (3, '有/無セレクトボックス'),
    (4, '必須/推奨/不要セレクトボックス'),
)

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_url = models.CharField(max_length=200)
    company_image_url = models.CharField(max_length=300, blank=True)
    company_description = models.CharField(max_length=300, blank=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        if self.deleted:
            return u'%s (deleted)' % (self.company_name)
        else:
            return self.company_name

"""
class QuestionCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=300)

A type of answer:
    id: answer_type_name
    1: インプットボックス
    2: 可/不可セレクトボックス
    3: 有/無セレクトボックス
    4: 必須/推奨/不要セレクトボックス
class AnswerType(models.Model):
    answer_type_name = models.CharField(max_length=50)

A relationship between specific answer's key and value:
    e.g. for answer type 2
        answer_key: answer_value
        1: 可
        2: 不可
        3: -
class AnswerTypeValue(models.Model):
    answer_type = models.ForeignKey(AnswerType)
    answer_key = models.IntegerField()
    answer_value = models.CharField(max_length=10)
"""

class Question(models.Model):
    category = models.IntegerField(choices=QUESTION_CATEGORY_CHOICES)
    answer_type = models.IntegerField(choices=ANSWER_TYPE_CHOICES)
    question_sentence = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % (self.question_sentence)

class Answer(models.Model):
    company = models.ForeignKey(Company)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=100)
    additional_info = models.CharField(max_length=200, blank=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s, %s, %s' % (self.answer, self.company, self.question)
