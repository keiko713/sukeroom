from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rooms.models import Company, Question, Answer
from rooms.models import QUESTION_CATEGORY_CHOICES
import json


def json_response(data, code=200, mimetype='application/json'):
    resp = HttpResponse(data, mimetype)
    resp.code = code
    return resp

def company(request):
    company_name = 'Twitter Japan'
    company = Company.objects.filter(company_name=company_name)
    if not company:
        raise Http404
    else:
        company = company[0]
    result = {}
    result['company'] = company

    categories = []
    for category in QUESTION_CATEGORY_CHOICES:
        questions = Question.objects.filter(category=category[0])
        qas = []
        for question in questions:
            answer = Answer.objects.filter(company=company, question=question)
            if answer:
                answer = answer[0]
            qa = {
                'answer_type': question.answer_type,
                'question_sentence': question.question_sentence,
                'answer': answer.answer if answer else '-',
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

    return render_to_response('company.html', {'result': result}, context_instance=RequestContext(request))

@csrf_exempt
def company_edit(request):
    change_nodes = request.POST.get('change_nodes', False)
    cid = request.POST.get('company_id', False)
    if not change_nodes or not cid:
        data = json.dumps({'msg': 'Error!'})
        return json_response(data)
    change_nodes = json.loads(change_nodes)
    nodes = change_nodes['nodes']
    for node in nodes:
        ai = False
        qid = node['qid']
        value = node['value']
        if node['qid'].startswith('ai'):
            qid = qid[2:]
            ai = True
        question = Question.objects.get(id=int(qid))
        company = Company.objects.get(id=int(cid))
        try:
            answer = Answer.objects.get(company=company, question=question)
            if ai:
                answer.additional_info = value
            else:
                answer.answer = value
        except Answer.DoesNotExist:
            if not ai:
                answer = Answer(company=company, question=question, answer=value)
            else:
                answer = Answer(company=company, question=question, answer='-', additional_info=value)

        answer.save()
    data = json.dumps({'msg': 'Success!'})
    return json_response(data)


@csrf_exempt
def question_add(request):
    category = request.POST.get('category', False)
    answer_type = request.POST.get('answer_type', False)
    question_sentence = request.POST.get('question_sentence', False)
    if not category or not answer_type or not question_sentence:
        data = json.dumps({'msg': 'Error!'})
        return json_response(data)

    question = Question(category=int(category), answer_type=int(answer_type), question_sentence=question_sentence)
    question.save()
    data = json.dumps({'msg': 'Success!'})
    return json_response(data)
