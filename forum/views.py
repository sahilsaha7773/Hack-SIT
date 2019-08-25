from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionCreateForm, AnswerForm
from django.contrib import messages
from django.shortcuts import redirect
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required
def  question_create(request):
	if request.method == 'POST':
		form = QuestionCreateForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			new = form.save(commit=False)
			new.user = request.user
			new.save()
			return redirect(new.get_absolute_url())
			messages.success(request, 'Question uploaded successfully')
		else:
			messages.success(request, 'Error uploading Question')
	else:
		form = QuestionCreateForm()
	return render(request, 'forum/create.html', {'form': form})

@login_required
def question_detail(request, id, slug):
	question = get_object_or_404(Question, id=id, slug=slug)

	answers = Answer.objects.filter( post=question).order_by('-ratings__average')

	new_answer = None
	if request.method == 'POST':
		answer_form = AnswerForm(data=request.POST)
		if answer_form.is_valid():
			new_answer = answer_form.save(commit=False)
			new_answer.post = question
			new_answer.author = request.user
			new_answer.save()
	else:
		answer_form = AnswerForm()

	return render(request, 'forum/detail.html', {'question':question, 'AnswerForm':AnswerForm, 'new_answer':new_answer, 'answers':answers})

@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = get_object_or_404(Question, id=post_id)
            if action == 'like':
                post.users_liked.add(request.user)
            else:
                post.users_liked.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko', 'post_id':post_id, 'action':action})

def post_list(request):
	object_list = Question.published.all()
	# tag = None

	# if tag_slug:
	# 	tag = get_object_or_404(Tag, slug=tag_slug)
		#object_list = object_list.filter(tags__in=[tag])

	paginator = Paginator(object_list, 3) # 3 posts in each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer deliver the first page
	    posts = paginator.page(1)	
	except EmptyPage:
	    # If page is out of range deliver last page of results
	    posts = paginator.page(paginator.num_pages)
	return render(request, 'forum/list.html', {'section': 'home','posts':posts, 'page':page})

@login_required
def post_delete(request, id, slug):
    post= get_object_or_404(Question, id=id, slug=slug) 
    if post.user == request.user:   
    	if request.method=='POST':
    		post.delete()
    		return redirect(post_list)
    else:
    	return HttpResponse('You are not authorized to delete this post')
        
    return render(request, 'forum/del_conf.html', {'object':post})

@login_required
def delete_done():
	return render(request, 'forum/del_done.html')