from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='comp')
router.register(r'workers', views.WorkerViewSet)

app_name = 'work'

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += format_suffix_patterns([
    path(
        'hire/',
        views.HireAPI.as_view()
    ),
    path(
        'workplaces/<int:pk>/',
        views.WorkPlaceDetailAPI.as_view(),
        name='wp-detail'
    ),
    path(
        'workplaces/<int:pk>/worktimes',
        views.WorkTimeListAPI.as_view(),
        name='wt-list'
    ),
    path(
        'companies/<int:pk>/works',
        views.WorkListAPI.as_view(),
        name='work-list'
    ),
])


# Using templates

# urlpatterns = [
#     path(
#         'companies/',
#         views.CompList.as_view(),
#         name='comp_list'
#     ),
#     path(
#         'companies/<int:pk>/',
#         views.CompDetail.as_view(),
#         name='comp_detail'
#     ),
#     path(
#         'companies/<int:pk>/managers/',
#         views.ManagList.as_view(),
#         name='manag_list'
#     ),
#     path(
#         'workers/',
#         views.WorkerList.as_view(),
#         name='worker_list'
#     ),
#     path(
#         'workers/<int:pk>/',
#         views.WorkerDetail.as_view(),
#         name='worker_detail'
#     ),
#     path(
#         'workers/<int:pk>/create_worktime',
#         views.CreateWorkTime.as_view(),
#         name='create_worktime'
#     ),
#     path(
#         'create_work/',
#         views.CreateWork.as_view(),
#         name='create_work'
#     ),
#     path(
#         'hire',
#         views.Hire.as_view(),
#         name='hire'
#     ),
#     path(
#         'workplace/<int:pk>/',
#         views.update_wp,
#         name='update_wp'
#     ),
# ]
