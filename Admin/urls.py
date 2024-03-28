from django.urls import path
from Admin import views
app_name="webadmin"

urlpatterns = [
    path('district/',views.district,name="district"),
    path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
    path('editdistrict/<str:id>',views.editdistrict,name="editdistrict"),
    path('Place/',views.Place,name="Place"),
    path('delPlace/<str:id>',views.delPlace,name="delPlace"),
    path('editPlace/<str:id>',views.editPlace,name="editPlace"),
    path('vacancy/',views.vacancy,name="vacancy"),
    path('Employe/',views.Employe,name="Employe"),
    path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
    path('viewreq/',views.viewreq,name="viewreq"),
    path('accept/<str:id>',views.accept,name="accept"),
    path('reject/<str:id>',views.reject,name="reject"),
    path('homepage/',views.homepage,name="homepage"),
    path('viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
    path('Reply/<str:id>',views.reply,name="reply"),
    path('logout/',views.logout,name="logout"),
    path('viewattendance/<str:id>',views.viewattendance,name="viewattendance"),
    path('viewemployee/',views.viewemployee,name="viewemployee"),
    path('Admin/',views.admin,name="admin"),

    
]