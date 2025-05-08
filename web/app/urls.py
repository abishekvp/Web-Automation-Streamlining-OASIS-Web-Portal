from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('mark_entry',views.mark_entry,name="mark_entry"),
    path('data_feed',views.data_feed,name="data_feed"),
    path('delete',views.delete,name="delete"),
]

