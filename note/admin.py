from django.contrib import admin
from django.contrib.auth import get_user_model
from note.models import Class, Diary, NotePrecise, UserProfile

# Register your models here.
class NotePreciseInline(admin.StackedInline):
    model = NotePrecise
    extra = 1
    verbose_name = "Note for each Student"

class ClassAdmin(admin.ModelAdmin):
    verbose_name = "Classroom"

class DiaryAdmin(admin.ModelAdmin):
    inlines = [NotePreciseInline,]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        return super(DiaryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields + ('author',)
        return self.readonly_fields

    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data['author'] = request.user
        request.GET = data
        return super(DiaryAdmin, self).add_view(request, form_url="", extra_context=extra_context)

admin.site.register(Class, ClassAdmin)
admin.site.register(Diary, DiaryAdmin)
admin.site.register(NotePrecise)
admin.site.register(UserProfile)
