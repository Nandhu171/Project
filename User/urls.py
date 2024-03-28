from django.urls import path
from User import views
app_name="webuser"

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('Myprofile/',views.Myprofile,name="Myprofile"),
    path('Editprofile/',views.Editprofile,name="Editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('viewvacancy/',views.viewvacancy,name="viewvacancy"),
    path('sendreq/<str:id>',views.sendreq,name="sendreq"),
<<<<<<< HEAD
    path('logout',views.logout,name="logout"),
    path('complaint/',views.complaint,name="complaint"),
    path('delcomplaint/<str:id>',views.delcomplaint,name="delcomplaint"),
=======
    path('logout/',views.logout,name="logout"),

>>>>>>> 6747d5d6cace1e7dff62efc55c1e8b7e82695daa
]