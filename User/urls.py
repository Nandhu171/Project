from django.urls import path
from User import views
app_name="webuser"

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
     path("Myprofile/",views.Myprofile,name="Myprofile"),
    path("Editprofile/",views.Editprofile,name="Editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path('viewvacancy/',views.viewvacancy,name="viewvacancy"),
    path('sendreq/<str:id>',views.sendreq,name="sendreq")
]