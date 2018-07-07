from django.contrib import admin
from django.contrib.auth import get_user_model
from note.models import Class, Diary, NotePrecise, UserProfile
from itertools import chain
from django.db.models import Q

# Register your models here.
class NotePreciseInline(admin.StackedInline):
    model = NotePrecise
    extra = 1
    verbose_name = "Note for each Student"

class NotePreciseAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == 'diary':

            if request.user.userprofile.headline == "Manager" or request.user.is_superuser:
                kwargs['queryset'] = Diary.objects.all()
            
            elif request.user.userprofile.headline == "Supporter":
                kwargs['queryset'] = Diary.objects.filter(author = request.user)
            
            elif request.user.userprofile.headline == "Teacher":
                user = request.user.userprofile
                classes = user.teacher.all()
                qs = user.teacher.none()
                for classroom in classes:
                    query = classroom.diary.all()
                    qs = qs | query
                kwargs['queryset'] = qs

        return super(NotePreciseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(NotePreciseAdmin, self).get_queryset(request)

        if request.user.is_superuser or request.user.userprofile.headline == "Manager":
            return qs
        
        if request.user.userprofile.headline == "Teacher":
            user = request.user.userprofile
            classes = user.teacher.all()
            qs = user.teacher.none()
            for classroom in classes:
                diaries = classroom.diary.all()
                for diary in diaries:
                    query = diary.note_precise.all() 
                    qs = qs | query
            return qs
        
        elif request.user.userprofile.headline == "Supporter":
            return qs.filter(diary__author = request.user)

class ClassAdmin(admin.ModelAdmin):
    verbose_name = "Classroom"

class DiaryAdmin(admin.ModelAdmin):
    inlines = [NotePreciseInline,]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == 'author':
            if request.user.is_superuser or request.user.userprofile.headline == "Manager":
                kwargs['queryset'] = get_user_model().objects.all()
            else:
                kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
        
        if db_field.name == 'classroom':
            if request.user.is_superuser or request.user.userprofile.headline == "Manager":
                kwargs['queryset'] = Class.objects.all()
            else:
                kwargs['queryset'] = Class.objects.filter(Q(teacher = request.user.userprofile) | Q(support=request.user.userprofile))
        
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

    def get_queryset(self, request):
        qs = super(DiaryAdmin, self).get_queryset(request)
        
        if request.user.is_superuser or request.user.userprofile.headline == "Manager":
            return qs
        
        elif request.user.userprofile.headline == "Teacher":
            user = request.user.userprofile
            classes = user.teacher.all()
            qs = user.teacher.none()
            for classroom in classes:
                query = classroom.diary.all()
                qs = qs | query
            return qs
        
        elif request.user.userprofile.headline == "Supporter":
            return qs.filter(author=request.user)

admin.site.register(Class, ClassAdmin)
admin.site.register(Diary, DiaryAdmin)
admin.site.register(NotePrecise, NotePreciseAdmin)
admin.site.register(UserProfile)
