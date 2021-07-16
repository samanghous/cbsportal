from django.contrib import admin
from django.urls import path
from cbs_portal import views

urlpatterns = [
    path('', views.index,name="cbs_portal"),
    path('securitykeygenerate', views.securitykeygenerate,name="cbs_portal"),
    path('afterlogin', views.afterlogin,name="cbs_portal"),
    path('afterloginComplaintForm', views.afterloginComplaintForm,name="cbs_portal"),
    path('afterloginMessFeedForm', views.afterloginMessFeedForm,name="cbs_portal"),
    path('logout', views.logoutuser,name="cbs_portal")
     
]
