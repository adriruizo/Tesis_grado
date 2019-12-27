from django.shortcuts import render
from . import functions
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request, template_name="chatApp/home.html"):
    #respuesta=get_response(request)
    context = {'title': 'Chatbot Version 1.0'}
    return render_to_response(template_name, context)

@csrf_exempt
def get_response(request):
    response = {'status': None}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data['message']
        print(message)
        chat_response = functions.chat_bot(message)
        response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
        response['status'] = 'ok'
        
    else:
        response['error'] = 'no post data found'
        print("no")
    print(response)
    return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)

