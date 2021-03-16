from django.urls import path
from . import views

urlpatterns = [
    path('courier/', views.CourierCreate.as_view()),
    path('courier/list/', views.CourierList.as_view()),
    path('collection/', views.CollectionCreate.as_view()),
    path('collection/list/', views.CollectionList.as_view()),
    path('package/', views.PackageCreate.as_view()),


#    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]
