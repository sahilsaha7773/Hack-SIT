from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from blog.models import Post
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

# Create your views here.

def user_login(request):
	if request.method=='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])

			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('home')
				else:
					return HttpResponse("Disabled account")
			else:
				return HttpResponse("Invalid login")
	else:
		form = LoginForm()
	return render(request, 'account/login.html', {'form': form})

def home(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])

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
	return render(request, 'account/home.html', {'section': 'home','posts':posts, 'page':page, 'tag':tag})

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			
			return render(request, 'account/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form': user_form})