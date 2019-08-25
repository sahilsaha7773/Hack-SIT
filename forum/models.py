from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from tinymce import HTMLField
from slugify import slugify
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset()

class Question(models.Model):
	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions_created', on_delete=models.CASCADE)
	question = models.CharField(max_length=1000)
	slug = models.SlugField(max_length=200, blank=True)
	url = models.URLField()
	content = HTMLField('Content')
	created = models.DateField(auto_now_add=True, db_index=True)
	users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='questions_liked', blank=True)
	published = PublishedManager()
	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return self.question

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.question)
		super(Question, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('forum:detail', args=[self.id, self.slug])

class Answer(models.Model):
  post = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Answers')
  author = models.ForeignKey(User, 
                             on_delete=models.CASCADE,
                             related_name='post_Answers', default=None) 
  content = HTMLField('Content')
  ratings = GenericRelation(Rating, related_query_name='foos')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)
  

  class Meta:
    ordering = ('-created_at',)

  def __str__(self):
    return 'Answer by {} on {}'.format(self.author, self.post)

