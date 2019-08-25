from django.shortcuts import render
from . import admin
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.
@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    comments = post.comments.filter(active=True)
    
    new_comment = None
    if request.method == 'POST':
      comment_form = CommentForm(data=request.POST)
      
      if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.author = request.user
        new_comment.save()
    else:
      comment_form = CommentForm()

    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,'blog/post/detail.html',{'post': post, 'new_comment':new_comment, 'comment_form':comment_form, 'comments':comments})

@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_liked.add(request.user)
            else:
                post.users_liked.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
