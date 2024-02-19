from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase



db=firestore.client()

config = {
  "apiKey": "AIzaSyDTaWnECREmBwzzN0byWQRD6-Ptsh7xLCg",
  "authDomain": "exertion-475b3.firebaseapp.com",
  "projectId": "exertion-475b3",
  "storageBucket": "exertion-475b3.appspot.com",
  "messagingSenderId": "404919533194",
  "appId": "1:404919533194:web:d2b9d03a4bc97982d27773",
  "measurementId": "G-0D08LTEK18",
  "databaseURL":"",
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()


# Create your views here.
def District(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    if request.method=="POST":
        data={"district_name":request.POST.get("district")}
        db.collection("tbl_district").add(data)
    return render(request,"Admin/District.html",{"district":dis_data})


def deldistrict(request,id):
    db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:District")


def Place(request):
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    result=[]
    place_data=db.collection("tbl_place").stream()
    for place in place_data:
        place_dict=place.to_dict()
        district=db.collection("tbl_district").document(place_dict["district_id"]).get()
        district_dict=district.to_dict()
        result.append({'districtdata':district_dict,'place_data':place_dict,'placeid':place.id})
    if request.method=="POST":
        data={"place_name":request.POST.get("place"),"district_id":request.POST.get("district")}
        db.collection("tbl_place").add(data)
        return redirect("webadmin:Place")
    else:
        return render(request,"Admin/Place.html")    


def vacancy(request):
    if request.method=="POST":
        data={"vacancy_postion":request.POST.get("postion"),"vacancy_details":request.POST.get("Details")}
        db.collection("tbl_vacancy").add(data)
    return render(request,"Admin/vacancy.html")
    
def Employe(request):
    if request.method =="POST":
      email = request.POST.get("email")
      password = request.POST.get("Password")
      try:
        Employe = firebase_admin.auth.create_user(email=email,password=password)
      except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
        return render(request,"Admin/Employe.html",{"msg":error})
      db.collection("tbl_Employereg").add({"Employe_id":Employe.uid,"Employe_name":request.POST.get("name"),"Employe_contact":request.POST.get("contact"),"user_email":request.POST.get("email"),"user_address":request.POST.get("Address"),"user_gender":request.POST.get("Gender")})
      return render(request,"Admin/Employe.html")
    else:
      return render(request,"Admin/Employe.html")          
