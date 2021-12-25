from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# def index(request):
#     #return HttpResponse("Hello, world. Yor're at the polls index")
#     #output = ', '.join([q.question_text for q in latest_question_list])

#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
    
#     context = {
#         'latest_question_list': latest_question_list
#     }
    
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)
    

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#     # response = "Yor're looking at the results of question %s."
#     question = get_object_or_404(Question, pk=question_id)
#     # return HttpResponse(response % question_id)
#     return render(request, 'polls/results.html', { 'question': question})



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5] # 최근 다섯개의 질문을 가져옴

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id): # question_id를 넘겨받음
    question = get_object_or_404(Question, pk=question_id) # id에 해당하는 question 조회
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) # 해당 question에 대해 외래키를 갖는 선택지를 가져옴
    except (KeyError, Choice.DoesNotExist): # 선택된 데이터가 없을 경우
        return render(request, 'polls/detail.html', {
            'question':question, # 다시 질문과 에러메세지를 보냄
            'error_merrage' : "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1 
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,))) # POST와 한 세트로 생각하면 됨
    # reverse; 하드코딩