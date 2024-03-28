from django.urls import path
from Guest import views
app_name="webguest"

urlpatterns = [
     path('Userregistraction/',views.Userregistraction,name="Userregistraction"), 
     path('Login/',views.Login,name="Login"),
     path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
     path('',views.index,name="index"),

]