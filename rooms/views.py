#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
from django.views.decorators.cache import never_cache
from rooms.models import Company, Question, Answer
from rooms.models import QUESTION_CATEGORY_CHOICES
import json
import traceback
import sys


# making json response using data
def json_response(data, code=200, mimetype='application/json'):
    resp = HttpResponse(data, mimetype)
    resp.status_code = code
    return resp


# for the index page
def index(request):
    return render_to_response('index.html', {
    }, context_instance=RequestContext(request))


# for the page that shows all companies
def companylist(request):
    companies = Company.objects.filter(deleted=False)
    return render_to_response('company_list.html', {
        'companies': companies,
    }, context_instance=RequestContext(request))


# for the page that shows all questions and answers
def qalist(request):
    cs = Company.objects.filter(deleted=False)
    categories = []
    for category in QUESTION_CATEGORY_CHOICES:
        # create a chunk of answers for each category
        cat = {}
        questions = Question.objects.filter(
            category=category[0]).order_by('id')
        # if there are more than 13 questions, separate question into 2
        q2 = True if len(questions) > 13 else False
        companies_q1 = []
        companies_q2 = []
        for c in cs:
            answers = []
            ans_list = Answer.objects.filter(
                company=c, question__category=category[0]).order_by('question__id')
            ans_idx = 0
            for q in questions:
                if ans_idx < len(ans_list) and q.id == ans_list[ans_idx].question.id:
                    ans = ans_list[ans_idx]
                    ans_idx += 1
                else:
                    # if there is no answer, set 未(means 未回答) to answer
                    ans = Answer(answer=u'未')
                answers.append(ans)
            com = {
                'company_name': c.company_name,
                'company_url': c.get_absolute_url(),
                'answers': answers[:13]
            }
            companies_q1.append(com)
            if q2:
                com = {
                    'company_name': c.company_name,
                    'company_id': c.id,
                    'answers': answers[13:]
                }
                companies_q2.append(com)
        cat = {
            'display_name': category[1].split('|')[0] + (' 1' if q2 else ''),
            'id': category[0],
            'questions': questions[:13],
            'companies': companies_q1,
        }
        categories.append(cat)
        if q2:
            cat = {
                'display_name': category[1].split('|')[0] + ' 2',
                'id': category[0],
                'questions': questions[13:],
                'companies': companies_q2,
            }
            categories.append(cat)

    return render_to_response('qa_list.html', {
        'categories': categories,
    }, context_instance=RequestContext(request))


# function that get display name of categor from category_idy
def get_category_display_name(category_id):
    for category in QUESTION_CATEGORY_CHOICES:
        if category[0] == category_id:
            return category[1].split('|')[0]
    return ''


# for the page that shows statistics data
def statistics(request):
    # graph1 response rate per company
    cs = Company.objects.filter(deleted=False)
    ques_count = Question.objects.all().count()
    companies = {}
    for c in cs:
        ans_count = Answer.objects.filter(company=c).count()
        persent = '%1.2f' % (float(ans_count) / ques_count)
        companies[persent] = c
    graph1 = []
    for k in sorted(companies.keys(), reverse=True):
        graph1.append({
            'persent': k,
            'name': companies[k].company_name,
            'url': companies[k].get_absolute_url()
        })

    # graph2 response rate per answer
    qs = Question.objects.all()
    comp_count = Company.objects.filter(deleted=False).count()
    questions = {}
    for q in qs:
        ans_count = Answer.objects.filter(question=q).count()
        persent = '%1.2f' % (float(ans_count) / comp_count)
        questions[persent] = q
    graph2 = []
    for k in sorted(questions.keys(), reverse=True):
        graph2.append({
            'persent': k,
            'category': get_category_display_name(questions[k].category),
            'sentence': questions[k].question_sentence,
        })

    # generate categorised question
    question_list = {}
    for q in qs:
        if not question_list.get(q.category):
            question_list[q.category] = []
        question_list[q.category].append(q)

    return render_to_response('statistics.html', {
        'graph1': graph1[:10],
        'graph2': graph2[:10],
        'question_list': question_list,
    }, context_instance=RequestContext(request))


# for ajax request of obtaining data to make pie chart
@never_cache
def piedata(request, question_id):
    try:
        q = Question.objects.get(pk=question_id)
        result = Answer.objects.filter(
            question=q).values("answer").annotate(Count("id")).order_by()
        data = []
        for r in result:
            data.append({'answer': r['answer'], 'id': r['id__count']})
        return json_response(json.dumps(data))
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print repr(traceback.format_exception(
            exc_type, exc_value, exc_traceback))
        return HttpResponseServerError(mimetype='application/json')


# for GET request that searches companies by keyword
@never_cache
def search(request):
    keyword = request.GET.get('keyword', '')
    companies = Company.objects.filter(
        (Q(company_name__contains=keyword) | Q(company_url__contains=keyword)
        | Q(company_description__contains=keyword)) & Q(deleted=False))
    return render_to_response('search_result.html', {
        'keyword': keyword,
        'companies': companies,
    }, context_instance=RequestContext(request))


# for the page to add new company
def addcompany(request):
    return render_to_response('add_company.html', {
    }, context_instance=RequestContext(request))


# for the page to edit company's information
def editcompany(request, company_id):
    try:
        company = Company.objects.get(pk=company_id, deleted=False)
    except Company.DoesNotExist:
        raise Http404

    return render_to_response('edit_company.html', {
        'company': company,
    }, context_instance=RequestContext(request))


# for the page that shows company's information
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


# for ajax request of editing answers
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
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print repr(traceback.format_exception(
            exc_type, exc_value, exc_traceback))
        return HttpResponseServerError(mimetype='application/json')


# for ajax request of adding new question
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
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print repr(traceback.format_exception(
            exc_type, exc_value, exc_traceback))
        return HttpResponseServerError(mimetype='application/json')


# for ajax request of adding new company
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
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print repr(traceback.format_exception(
            exc_type, exc_value, exc_traceback))
        return HttpResponseServerError(minetype='application/json')


# for ajax request of editing company information
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
        company.company_name = company_name
        company.company_url = company_url
        company.company_image_url = company_image_url
        company.company_description = company_description
        company.save()
        data = json.dumps({})
        return json_response(data)
    except Company.DoesNotExist:
        return HttpResponseBadRequest(minetype='application/json')
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print repr(traceback.format_exception(
            exc_type, exc_value, exc_traceback))
        return HttpResponseServerError(minetype='application/json')
