from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from qa.models import Question
from qa.models import Answer
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import AskForm, AnswerForm
from django.http import HttpResponse, HttpResponseRedirect

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
    one_question = get_object_or_404(Question, pk=pk)
    answers=one_question.answer_for_question.all()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save()
            url = one_question.get_url()
            return HttpResponseRedirect(url)

    else:
        form = AnswerForm(initial={'question': one_question.id})
        form = AnswerForm(initial={'question': one_question.id})
    return render(request, 'question_details.html', {
	    'question': one_question,
	    "form":form,
	    "answers":answers
    })


@login_required
def question_add(request):
    if request.method == "POST":
        form_2 = AskForm(request.POST)
        if form_2.is_valid():
            new_question = form_2.save()
            url = new_question.get_url()
            return HttpResponseRedirect(url)
    else:
        form_2 = AskForm()
    return render (request,'ask.html', {
     'form':form_2
    })



