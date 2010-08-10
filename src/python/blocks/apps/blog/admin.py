from django.contrib import admin

from blocks.apps.core.admin import BaseContentAdmin, MultiLanguageInline
from blocks.apps.comments.moderation import CommentModerator, moderator

from blocks.apps.blog.models import BlogEntry, BlogEntryTranslation

class BlogEntryInline(MultiLanguageInline):
	model = BlogEntryTranslation

class BlogEntryAdmin(BaseContentAdmin):
	inlines = [BlogEntryInline]
	fieldsets = (
	   (None,					{'fields': ('name', 'comments_enabled', 'tag_list', )}),
	   BaseContentAdmin.PUBLISHING_OPTIONS,
	)
	list_filter = ('comments_enabled', 'status', 'promoted',)
	list_display = ('name', 'comments_enabled', 'creation_user', 'lastchange_date', 'status', 'promoted', )

admin.site.register(BlogEntry, BlogEntryAdmin)


class BlogEntryModerator(CommentModerator):
	email_notification = True
	enable_field = 'comments_enabled'

moderator.register(BlogEntry, BlogEntryModerator)