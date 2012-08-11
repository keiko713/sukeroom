#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.cache import cache

QUESTION_CATEGORY_CHOICES = (
    (1, 'メール・通信|MailNetwork'),
    (3, '社内システム|CorpSystem'),
    (2, 'Web閲覧・ソフトウェア規制|WebSoftware'),
    (4, '働く環境|Environment'),
)

ANSWER_TYPE_CHOICES = (
    (1, 'インプットボックス'),
    (2, '可/制限付可/不可セレクトボックス'),
    (3, '有/無セレクトボックス'),
    (4, '必須/推奨/不要セレクトボックス'),
)


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_url = models.CharField(max_length=200)
    company_image_url = models.CharField(max_length=300, blank=True)
    company_description = models.CharField(max_length=300, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Companies"

    def __unicode__(self):
        if self.deleted:
            return u'%s (deleted)' % (self.company_name)
        else:
            return self.company_name

    def get_absolute_url(self):
        return '/company/%i/' % self.id

    def save(self):
        # set 'updated' key and the urls that need to update
        updated = cache.get('updated')
        if not updated:
            updated = {}
        updated['/companylist/'] = True
        updated[self.get_absolute_url()] = True
        updated['/editcompany/%i/' % self.id] = True
        updated['/qalist/'] = True
        updated['/statistics/'] = True
        cache.set('updated', updated)
        super(Company, self).save()


class Question(models.Model):
    category = models.IntegerField(choices=QUESTION_CATEGORY_CHOICES)
    answer_type = models.IntegerField(choices=ANSWER_TYPE_CHOICES)
    question_sentence = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % (self.question_sentence)

    def save(self):
        updated = cache.get('updated')
        if not updated:
            updated = {}
        updated['/qalist/'] = True
        updated['/statistics/'] = True
        cache.set('updated', updated)
        super(Question, self).save()


class Answer(models.Model):
    company = models.ForeignKey(Company)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=100)
    additional_info = models.CharField(max_length=200, blank=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s, %s, %s' % (self.answer, self.company, self.question)

    def save(self):
        updated = cache.get('updated')
        if not updated:
            updated = {}
        updated[self.company.get_absolute_url()] = True
        updated['/qalist/'] = True
        updated['/statistics/'] = True
        cache.set('updated', updated)
        super(Answer, self).save()
