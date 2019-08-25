from django import forms
from .models import Question, Answer
from tinymce import TinyMCE
from django.contrib.auth.models import User

class QuestionCreateForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCE(mce_attrs={'width': 800}))
	class Meta:
		model = Question
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['content'].widget.attrs.update(TinyMCE(mce_attrs={'width': 800}))
		fields = ('question', 'content')

class AnswerForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCE(mce_attrs={'width': 800}))
	class Meta:
		model = Answer
		fields = ('content',)