from django.urls import path
from . import views

app_name="meetup"
urlpatterns = [
    path('', views.meetup_list, name='meetup_list'),
    path('cadastro/', views.meetup_create, name='meetup_create'),
    path('detalhes/<int:id>/', views.meetup_detail, name='detail'),
    path('inscricao/<int:id>/', views.inscricao_create, name='inscricao'),
    path('reunioes_inscritas/', views.inscricao_list, name='inscricao_list'),
    path('reunioes_criadas/', views.reuniao_list_user, name='reuniao_list_user'),
    path('proximas_reunioes/', views.proximas_reunioes, name='proximas_reunioes'),
    path('editar_reuniao/<int:id>/', views.meetup_edit, name='meetup_edit'),
]
