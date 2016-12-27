from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from qa.models import Question
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from django.http import HttpResponse 
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
    return render(request, 'question_details.html', {
	'question': question,
    })

