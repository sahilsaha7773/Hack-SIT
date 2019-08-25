from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',   
                       'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'post', 'created_at', 'active')
	list_filter = ('active', 'created_at', 'updated_at')
	search_fields = ('author', 'body')

	def save_model(self, request, obj, form, change):
		obj.author = request.user
		super().save_model(request, obj, form, change)