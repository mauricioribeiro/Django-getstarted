from django.shortcuts import get_object_or_404,render
# my imports
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question


# Create your views here.
'''
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'firstapp/index.html', context)

def detail(request, question_id):
	q = get_object_or_404(Question,pk=question_id)
	return render(request, 'firstapp/detail.html', { 'question': q })

def results(request, question_id):
	q = get_object_or_404(Question,pk=question_id)
	return render(request, 'firstapp/results.html', { 'question': q })
'''

class IndexView(generic.ListView):
	template_name = 'firstapp/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'firstapp/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'firstapp/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'firstapp/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('firstapp:results', args=(question.id,)))

def notfound(request):
	return HttpResponse("Make sure the requested page exists..")