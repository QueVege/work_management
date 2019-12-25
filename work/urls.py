from django.urls import path
from . import views

app_name = 'work'

urlpatterns = [
    path(
        'companies/',
        views.CompList.as_view(),
        name='comp_list'
    ),
    path(
        'companies/<int:pk>/',
        views.CompDetail.as_view(),
        name='comp_detail'
    ),
    path(
        'companies/<int:pk>/managers/',
        views.ManagList.as_view(),
        name='manag_list'
    ),
    path(
        'workers/',
        views.WorkerList.as_view(),
        name='worker_list'
    ),
    path(
        'workers/<int:pk>/',
        views.WorkerDetail.as_view(),
        name='worker_detail'
    ),
    path(
        'workers/<int:pk>/create_worktime',
        views.CreateWorkTime.as_view(),
        name='create_worktime'
    ),
    path(
        'create_work/',
        views.CreateWork.as_view(),
        name='create_work'
    ),
    path(
        'hire',
        views.Hire.as_view(),
        name='hire'
    ),
    path(
        'workplace/<int:pk>/',
        views.update_wp,
        name='update_wp'
    ),
]
