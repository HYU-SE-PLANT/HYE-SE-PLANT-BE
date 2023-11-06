from django.contrib import admin
from community.models import Community


# Register your models here.
class CommunityCheck(admin.ModelAdmin):
    list_display = ('id', 'user' , 'question_title', 'created_at')
    search_fields = ('user', 'question_title')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('question_detail', {'fields': ('question_title', 'question_content')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('question_title', 'question_content')
        }),
    )

admin.site.register(Community, CommunityCheck)