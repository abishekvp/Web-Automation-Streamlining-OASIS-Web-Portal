from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('username',views.username,name="username"),
    path('email',views.email,name="email"),
    path('profile',views.profile,name="profile"),
    path('edit_profile',views.edit_profile,name="edit_profile"),
    path('contacts',views.contacts,name="contacts"),
    path('mark_entry',views.mark_entry,name="mark_entry"),
    path('data_feed',views.data_feed,name="data_feed"),
    path('student_list',views.student_list,name="student_list"),
    path('text_recognition',views.text_recognition,name="text_recognition"),
]

