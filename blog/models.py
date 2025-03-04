from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from tinymce import HTMLField
from taggit.managers import TaggableManager

# Create your models here.

class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

  STATUS_CHOICES = ( 
      ('draft', 'Draft'), 
      ('published', 'Published'), 
  ) 
  title = models.CharField(max_length=250) 
  slug = models.SlugField(max_length=250,  
                          unique_for_date='publish') 
  author = models.ForeignKey(User, 
                             on_delete=models.CASCADE,
                             related_name='blog_posts') 
  body = HTMLField('Content')
  publish = models.DateTimeField(default=timezone.now) 
  created = models.DateTimeField(auto_now_add=True) 
  updated = models.DateTimeField(auto_now=True) 
  status = models.CharField(max_length=10,  
                            choices=STATUS_CHOICES, 
                            default='draft') 
  
  objects = models.Manager() # The default manager. 
  published = PublishedManager() # Our custom manager.
  users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)
  tags = TaggableManager()
  
  class Meta: 
      ordering = ('-publish',) 

  def __str__(self): 
      return self.title

  def get_absolute_url(self):
      return reverse('blog:post_detail',
                     args=[self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug])

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(User, 
                             on_delete=models.CASCADE,
                             related_name='post_comments', default=None) 
  body = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)
  

  class Meta:
    ordering = ('-created_at',)

  def __str__(self):
    return 'Comment by {} on {}'.format(self.author, self.post)