from django.urls import path
from . import views
urlpatterns=[
  path("",views.home,name="home"),
  path("about/",views.about,name="about_path"),
  path("login/",views.login_function,name="login"),
  path("logout/",views.logout_function,name="logout"),
  path("register/",views.register,name="register"),
  path("product/<int:product_id>",views.product,name="product"),
  path("category/<str:cat_name>",views.category,name="category"),
  path("all_categories/",views.all_categories,name="categories"),
  path("updateuser/",views.update_user,name="update_user"),
  path("updatepassword/",views.update_password,name="update_password"),
  path("updateprofile/",views.update_profile,name="update_profile")
  
]