from django.urls import path
from . import views

urlpatterns = [
    path('courier/', views.CourierCreate.as_view()),
    path('courier/list/', views.CourierList.as_view()),
    path('collection/', views.CollectionCreate.as_view()),
    path('collection/list/', views.CollectionList.as_view()),
    path('package/<slug:slug>/cancel/', views.PackageCancel.as_view()), 
    path('package/<slug:slug>/accept/', views.PackageAccept.as_view()), 
    path('package/<slug:slug>/receive/', views.PackageReceived.as_view()), 
    path('package/<slug:slug>/on-way/', views.PackageOnWay.as_view()), 
    path('package/<slug:slug>/delivered/', views.PackageDelivered.as_view()), 
    path('package/list/', views.PackageList.as_view()),
    path('package/', views.PackageCreate.as_view()),
    


#    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]
