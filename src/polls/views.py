# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from polls.models import Poll, Choice

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse

from django.views import generic
from django.utils import timezone

from django.template import RequestContext, loader
# def index(request):
#     latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = RequestContext(request, {
#         'latest_poll_list' : latest_poll_list
#     })        
#     return HttpResponse(template.render(context));

def index(request):
    latest_poll_list = Poll.objects.filter(
        pub_date___lte=timezone.now()        
    ).order_by('-pub_date')[:5]
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
    #data = serializers.serialize("json", [poll])    
    
    return render(request, 'polls/results.html', {'poll':poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the poll voting for,
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name = 'latest_poll_list'
    
    def get_queryset(self):
        """
        Return the last five published polls (not including those set to be
        published in the future).
        """
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    
class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'
    

    
    
    
    
    
    
    
    
    
    
    