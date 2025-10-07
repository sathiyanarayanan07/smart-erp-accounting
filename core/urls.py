
from django.urls import path
from .import views

urlpatterns = [
    path("register/",views.register,name="register"),
    path("login_user/",views.login_user,name="login_user"),
    path("logout/",views.logout,name="logout"),
    path("verify_otp/",views.verify_otp,name="verify_otp"),
    path("logout_view/",views.logout_view,name="logout_view"),
    path("user_profile/",views.user_profile,name="user_profile"),
    path("user_update/<str:email>/",views.user_update,name="user_profile_update"),
    path("user_list/",views.user_details,name="user_list"),
    path("user_delete/<str:email>/",views.user_delete,name="user_delete"),


    
]