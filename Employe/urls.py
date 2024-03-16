from django.urls import path
from Employe import views
app_name="webemploye"

urlpatterns = [

    path('homepage/',views.homepage,name="homepage"),
    path("Myprofile/",views.Myprofile,name="Myprofile"),
    path("Editprofile/",views.Editprofile,name="Editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path('work/',views.work,name="work"),
    path('Attendence/',views.attendence,name="attendence"),
    path('complaint/',views.complaint,name="complaint"),
    path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
    path('logout/',views.logout,name="logout"),

]
