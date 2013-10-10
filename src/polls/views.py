# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from polls.models import Poll

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.template import RequestContext, loader
# def index(request):
#     latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = RequestContext(request, {
#         'latest_poll_list' : latest_poll_list
#     })        
#     return HttpResponse(template.render(context));

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]    
    context = {
        'latest_poll_list' : latest_poll_list
    }
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
#     try:
#         poll = Poll.objects.get(pk=poll_id)
#     except Poll.DoesNotExist:
#         raise Http404

    poll = get_object_or_404(Poll, pk=poll_id)             
    return render(request, 'polls/detail.html', {'poll':poll})
    

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)           
    data = serializers.serialize("json", [poll])
    #data = json.dumps(poll, cls=DjangoJSONEncoder)
    
    return HttpResponse(data)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)