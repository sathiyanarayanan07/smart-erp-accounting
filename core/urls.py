

from django.urls import path
from . import views

urlpatterns = [
    path("single_login/",views.single_login,name="role1_login"),
    path("get_user_data/",views.get_user_data,name="get_user_data"),
    path("single_signup/",views.admin_single_signup,name="single_signup"),
    path("logout/",views.logout,name="logout"),
    path("add_product_details/",views.add_product_details,name="add_product_details"),
    path("update_product_status/<int:id>/",views.update_product_status,name="update_product_status"),
    path("delete_product/<int:id>/",views.delete_product,name="delete_product"),
    path("qa_view/",views.qa_view,name="qa_view"),
    path("plan_product/",views.add_plan_product,name="plan_product"),
    path("get_plan_product/",views.get_plan_products,name="get_plan_product"),
    path("add_product_material/",views.add_product_material,name="add_product_material"),
    path("get_product_material/",views.get_product_materials,name="get_product_material"),
    path("add_product_options/",views.add_product_options,name="add_product_options"),
    path("get_product_options/",views.get_product_options,name="get_product_options"),
    path("Schedule_add/",views.Schedule_add,name="Schedule_add"),
    path("Schedule_view/",views.Schedule_view,name="Schedule_view"),
    path("product_qa_view/",views.product_qa_view,name="product_qa_view"),
    path("add_account/",views.add_account,name="create_account"),
    path("account_view/",views.account_view,name="account_view"),
    path("get_role_count/",views.get_role_count,name="get_role_count"),
    path("total_product/",views.total_product,name="total_product"),
    path("Schedule_process/",views.Schedule_process,name="Schedule_process"),
    path("over_all_details/",views.over_all_details,name="over_all_details")
   

  
]
