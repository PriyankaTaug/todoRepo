from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from todoapp.views import *
from.import views

app_name="todoapp"

urlpatterns = [
    path('login/',views.login,name='login'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_applogin/',views.LoginPage.as_view(),name='user_applogin'),
    path('user_todo/',views.ToDo.as_view(),name='user_todo'),
    path('todo_insert/',views.TaskInsert.as_view(),name='user_todo'),
    path('user_logout/',views.Logout.as_view(),name='user_logout'),
    path('todoinsert/',views.todoinsert,name='todoinsert'),
    path('viewtodo/',views.viewtodo,name='viewtodo'),
    path('todo_delete/',views.todo_delete,name='todo_delete'),
    path('todo_logout/',views.todo_logout,name='todo_logout'),
    path('todo_view/',views.todo_view,name='todo_view'),
    path('todo_update/',views.todo_update,name='todo_update'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)