from django.conf.urls import url
from . import views #(imports views.py of the current folder)

urlpatterns = [ 
    url(r'^$', views.index), 
    url(r'^register', views.register),
    url(r'login', views.login),
    url(r'success', views.success),
    url(r'^user_create', views.user_create), # POST data from ADD to the DB
    url(r'^user/(?P<id>\d+)', views.show_user), #display the particular book 
    url(r'^like_btn', views.like_btn),
    url(r'^drop_btn', views.drop_btn),
    url(r'logout', views.logout)
    ]