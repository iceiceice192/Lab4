
from django.contrib import admin
from django.urls import path
from records import views
urlpatterns = [
 path('admin/', admin.site.urls),
 path('', views.add_record),
 path('list/', views.list_records),
 path('ajax-search/', views.ajax_search),
 path('edit/<int:pk>/', views.edit_record),
 path('delete/<int:pk>/', views.delete_record),
]
