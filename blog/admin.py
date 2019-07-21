from django.contrib import admin
from .models import Post

# Register your models here.

# 增加Post项
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ('title', 'body')
    # 域填充
    prepopulated_fields = {'slug':('title',)}

    # 排序
    ordering = ('status', 'publish')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'