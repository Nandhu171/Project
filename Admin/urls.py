from django.urls import path
from Admin import views
app_name="webadmin"

urlpatterns = [
    path('District/',views.District,name="District"),
    path('Place/',views.Place,name="Place"),
    path('vacancy/',views.vacancy,name="vacancy"),
    path('Employe/',views.Employe,name="Employe"),
    path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
    path('viewreq/',views.viewreq,name="viewreq")

]