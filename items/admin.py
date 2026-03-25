from django.contrib import admin
from .models import Item, ItemImage, Message

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 0

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'category', 'location', 'status', 'user', 'is_approved', 'created_at']
    list_filter = ['type', 'category', 'status', 'is_approved']
    search_fields = ['title', 'description', 'location']
    inlines = [ItemImageInline]
    actions = ['approve_items', 'close_items']

    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
    approve_items.short_description = '审核通过'

    def close_items(self, request, queryset):
        queryset.update(status='closed')
    close_items.short_description = '关闭物品'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'item', 'content', 'is_read', 'created_at']
    list_filter = ['is_read']
