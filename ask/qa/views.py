from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from qa.models import Question
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import AskForm, AnswerForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit >100:
        limit = 10
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page, paginator

def home(request):
    questions = Question.objects.all()
    questions = questions.order_by('-id')
    page, paginator=paginate(request, questions)
    paginator.baseurl = reverse('home') + '?page='
    return render(request, 'home.html', {
	'questions': page.object_list,
	'paginator': paginator, 'page': page,
    })
def popular(request):
    questions=Question.objects.all()
    questions=questions.order_by('-rating')
    page, paginator=paginate(request, questions)
    paginator.baseurl = reverse('popular') + '?page='
    return render(request, 'popular.html', {
	'questions': page.object_list,
	'paginator': paginator, 'page': page,
    })

def question_details(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers=question.ok.all()
    
    form = AnswerForm({"question": question.id})
	
    return render(request, 'question_details.html', {
	'question': question,
	"form":form,
	"answers":answers
    })


@login_required
def question_add(request):
    if request.method == "POST":
	form = AskForm(request.POST)
	if form.is_valid():
    	    question = form.save()
            url = question.get_url()
	    return HttpResponseRedirect(url)
    else:
	form = AskForm()
    return render (request,'ask.html', {
	'form':form    
})
@require_POST
def answer_add(request):
    if request.method == "POST":
	form = AnswerForm(request.POST)
	if form.is_valid():
    	    answer = form.save()
            url = answer.get_url()
	    return HttpResponseRedirect(url)
    return HttpResponseRedirect('/')
     

