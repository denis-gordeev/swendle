from django.contrib import admin
from .forms import AdminUserChangeForm, AdminUserAddForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from .models import Story, Source, Party, Article, Cluster, Fact, Comment, Citation, CitationComment, MyUser



# Указываем наши форма для создания и редактирования пользователя.
# Добавляем новые поля в fieldsets, и поле email в add_fieldsets.
class UserAdmin(UserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'avatar',
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

admin.site.register(Story)
admin.site.register(Source)
admin.site.register(Party)
admin.site.register(Article)
admin.site.register(Cluster)
admin.site.register(Fact)
admin.site.register(Comment)
admin.site.register(Citation)
admin.site.register(CitationComment)
admin.site.register(MyUser, UserAdmin)
