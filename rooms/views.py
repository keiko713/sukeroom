#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rooms.models import Company, Question, Answer
from rooms.models import QUESTION_CATEGORY_CHOICES
import json


def json_response(data, code=200, mimetype='application/json'):
    resp = HttpResponse(data, mimetype)
    resp.status_code = code
    return resp

def index(request):
    return render_to_response('index.html', {
    }, context_instance=RequestContext(request))

def companylist(request):
    companies = Company.objects.filter(deleted=False)
    return render_to_response('company_list.html', {
        'companies': companies,
    }, context_instance=RequestContext(request))

def search(request):
    keyword = request.GET.get('keyword', '')
    companies = Company.objects.filter(
        (Q(company_name__contains=keyword)|Q(company_url__contains=keyword)
        |Q(company_description__contains=keyword))&Q(deleted=False))
    return render_to_response('search_result.html', {
        'keyword': keyword,
        'companies': companies,
    }, context_instance=RequestContext(request))

def addcompany(request):
    return render_to_response('add_company.html', {
    }, context_instance=RequestContext(request))

def editcompany(request, company_id):
    try:
        company = Company.objects.get(pk=company_id, deleted=False)
    except Company.DoesNotExist:
        raise Http404

    return render_to_response('edit_company.html', {
        'company': company,
    }, context_instance=RequestContext(request))

def company(request, company_id):
    try:
        company = Company.objects.get(pk=company_id, deleted=False)
    except Company.DoesNotExist:
        raise Http404

    result = {}
    # if there is no image registered, use default one
    if not company.company_image_url:
        company.company_image_url = '/static/img/company_default.png'
    result['company'] = company

    # get questions and answers of each category
    categories = []
    for category in QUESTION_CATEGORY_CHOICES:
        questions = Question.objects.filter(category=category[0])
        qas = []
        for question in questions:
            answer = Answer.objects.filter(
                company=company, question=question)
            if answer:
                answer = answer[0]
            qa = {
                'answer_type': question.answer_type,
                'question_sentence': question.question_sentence,
                'answer': answer.answer if answer else '',
                'additional_info': answer.additional_info if answer else '',
                'question_id': question.id,
            }
            qas.append(qa)
        cat = {
            'category_id': category[0],
            'display_name': category[1].split('|')[0],
            'id_name': category[1].split('|')[1],
            'qas': qas,
        }
        categories.append(cat)
    result['categories'] = categories

    # count how many questions the company hasn't answered
    count_q = Question.objects.count()
    count_a = Answer.objects.filter(company=company).count()
    result['not_answer_yet'] = count_q - count_a

    # get the recently answered questions up to 4
    r_answers = Answer.objects.filter(
        company=company).order_by('updated').reverse()[:4]
    r_questions = []
    for ans in r_answers:
        r_questions.append(ans.question.question_sentence)
    result['recent_ans_questions'] = r_questions

    return render_to_response('company.html', {
        'result': result
    }, context_instance=RequestContext(request))

@csrf_exempt
def answer_edit(request):
    change_nodes = request.POST.get('change_nodes', False)
    cid = request.POST.get('company_id', False)
    if not change_nodes or not cid:
        return HttpResponseBadRequest(mimetype='application/json')
    try:
        # get nodes from change_nodes json object
        change_nodes = json.loads(change_nodes)
        nodes = change_nodes['nodes']
        # each node is for the change of
        # either answer or additional info
        for node in nodes:
            ai = False
            qid = node['qid']
            value = node['value']
            # if the node is for additional info,
            # qid starts with ai
            if node['qid'].startswith('ai'):
                qid = qid[2:]
                ai = True
            question = Question.objects.get(id=qid)
            company = Company.objects.get(id=cid)
            try:
                # get the answer object based on company and question
                answer = Answer.objects.get(
                    company=company, question=question)
                # change the value of the answer object
                if ai:
                    answer.additional_info = value
                else:
                    answer.answer = value
            except Answer.DoesNotExist:
                if not ai:
                    # if there is no answer object,
                    # and this node is not for additional info,
                    # create the new answer object with answer=value
                    answer = Answer(
                        company=company, question=question, answer=value)
                else:
                    # if there is no answer object,
                    # and this node is for additional info,
                    # create the new answer object without answer(-),
                    # and with additional_info=value
                    answer = Answer(
                        company=company, question=question,
                        answer='-', additional_info=value)

            answer.save()
        data = json.dumps({})
        return json_response(data)
    except Exception:
        return HttpResponseServerError(mimetype='application/json')


@csrf_exempt
def question_add(request):
    category = request.POST.get('category', False)
    answer_type = request.POST.get('answer_type', False)
    question_sentence = request.POST.get('question_sentence', False)
    if not category or not answer_type or not question_sentence:
        return HttpResponseBadRequest(mimetype='application/json')

    try:
        question = Question(
            category=int(category), answer_type=int(answer_type),
            question_sentence=question_sentence)
        question.save()
        data = json.dumps({})
        return json_response(data)
    except Exception:
        return HttpResponseServerError(mimetype='application/json')

@csrf_exempt
def company_add(request):
    company_name = request.POST.get('company_name', False)
    company_url = request.POST.get('company_url', False)
    company_image_url = request.POST.get('company_image_url', '')
    company_description = request.POST.get('company_description', '')
    if not company_name or not company_url:
        return HttpResponseBadRequest(minetype='application/json')

    try:
        company = Company(
            company_name=company_name, company_url=company_url,
            company_image_url=company_image_url,
            company_description=company_description)
        company.save()
        data = json.dumps({})
        return json_response(data)
    except Exception:
        return HttpResponseServerError(minetype='application/json')

@csrf_exempt
def company_edit(request):
    company_id = request.POST.get('company_id', False)
    company_name = request.POST.get('company_name', False)
    company_url = request.POST.get('company_url', False)
    company_image_url = request.POST.get('company_image_url', '')
    company_description = request.POST.get('company_description', '')
    if not company_id or not company_name or not company_url:
        return HttpResponseBadRequest(minetype='application/json')
    try:
        company = Company.objects.get(pk=company_id, deleted=False)
        company.company_name=company_name
        company.company_url=company_url
        company.company_image_url=company_image_url
        company.company_description=company_description
        company.save()
        data = json.dumps({})
        return json_response(data)
    except Company.DoesNotExist:
        return HttpResponseBadRequest(minetype='application/json')
    except Exception:
        return HttpResponseServerError(minetype='application/json')
