from django.contrib import admin
from note.models import Class, Diary, NotePrecise

# Register your models here.
class NotePreciseInline(admin.StackedInline):
    model = NotePrecise
    extra = 1

class DiaryAdmin(admin.ModelAdmin):
    inlines = [NotePreciseInline,]


admin.site.register(Class)
admin.site.register(Diary, DiaryAdmin)
admin.site.register(NotePrecise)