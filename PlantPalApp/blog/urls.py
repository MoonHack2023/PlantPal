from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('login/', views.login, name='blog-about'),
    path('plant/', views.plant_select, name='blog-plant'),
    path('plant/charts1', views.about1, name='blog-about1'),
    path('plant/charts2', views.about2, name='blog-about2'),
    path('plant/setup', views.plant_setup, name='blog-setup'),
    path('plant/learnmore', views.learn_more, name='blog-learn'),
    # path('index/', TemplateView.as_view(template_name='index.html'),
    # name='index'),
    # path('form/',views.form, name='blog-about'),
    # path('about/distance', views.distance, name='blog-about'),
]

urlpatterns += staticfiles_urlpatterns()