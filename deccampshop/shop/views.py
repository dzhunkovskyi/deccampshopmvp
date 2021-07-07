from django.shortcuts import render

# Create your views here.

import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import requests

from shop import models


telegram_url = 'https://api.telegram.org/bot1711627262:AAGB7zbJFmtNK5aCkzs9jAbI3djdgdxHrNA/{method}'


@csrf_exempt
def shop(request):
    print('*'*110)
    body_str = request.body.decode('utf-8')
    print(body_str)
    print(type(body_str))
    body_dict = json.loads(body_str)
    print(type(body_dict))

    if 'callback_query' in body_dict:
        chat_id = body_dict['callback_query']['message']['chat']['id']
    else:
        chat_id = body_dict['message']['chat']['id']

    person = models.Person.objects.filter(chat_id=chat_id).first()
    if person is None and 'message' in body_dict:
        person = models.Person.objects.create(
            first_name=body_dict['message']['from']['first_name'],
            last_name=body_dict['message']['from']['last_name'],
            chat_id=chat_id,
        )

    print('chat_id: ', chat_id)
    print('*'*110)

    question = 'Ти вже пройшов свій сюжет?'
    answers = []

    # if 'message' in body_dict:
    #     print(body_dict['message']['text'])
    #     if 'photo' in body_dict['message']['text']:
    #         url = telegram_url.format(method='sendPhoto')
    #         answer = {
    #             'chat_id': chat_id,
    #             'photo': 'AgACAgIAAxkDAAPNYIVWE4kBMHqqXllE8aIOmq4q3rEAAlGzMRuDvShIqzFfEw_bv1q7ipChLgADAQADAgADbQADzXkBAAEfBA',
    #         }
    #         requests.post(url, json=answer)


    if 'message' in body_dict and person.last_q_asked is None:
        if '/start' in body_dict['message']['text']:
            question_obj = models.Question.objects.filter(
                request_data='start',
            ).values(
                'id',
                'request_data',
                'q',
            ).first()
            print('question_obj: ', question_obj)

            question = question_obj['q']
            answers = make_answers(question_obj['id'])
            person.last_q_asked_id = question_obj['id']
            person.q_plus_a = question
            person.save()
    elif 'message' in body_dict and person.last_q_asked is not None:

        if '/start' in body_dict['message']['text']:
            question_obj = models.Question.objects.filter(
                id=person.last_q_asked_id,
            ).values(
                'id',
                'request_data',
                'q',
            ).first()

            if question_obj is not None:
                question = question_obj['q']
                answers = make_answers(question_obj['id'])
                print('question_obj: ', question_obj)

    elif 'callback_query' in body_dict:
        callback_data = body_dict['callback_query']['data']

        answer = models.Answer.objects.filter(
            a_data=callback_data,
        ).values_list(
            'a',
            flat=True,
        ).first()

        if answer is not None:
            print('#'*100)
            print(person.q_plus_a)
            print(type(person.q_plus_a))
            print(answer)
            person.q_plus_a = person.q_plus_a + '---' + answer

        question_obj = models.Question.objects.filter(
            request_data=callback_data,
        ).values(
            'id',
            'request_data',
            'q',
        ).first()

        if question_obj is not None:
            question = question_obj['q']
            answers = make_answers(question_obj['id'])
            print('question_obj: ', question_obj)

            person.q_plus_a = person.q_plus_a + ' | ' + question
            person.last_q_asked_id = question_obj['id']

        person.save()




    # now = datetime.datetime.now()
    # date_info = "<html><body>It is now %s.</body></html>" % now
    # question = date_info
    # answers = [
    #     {'text': '1', 'callback_data': '123'},
    #     {'text': '3', 'callback_data': '444'},
    # ]

    url = telegram_url.format(method='sendMessage')
    answer = {
        'chat_id': chat_id,
        'text': question,
        'reply_markup': {
            'inline_keyboard': [
                answers
            ]
        }
    }
    requests.post(url, json=answer)

    return HttpResponse(json.dumps({'date': 'today'}), content_type="application/json")
