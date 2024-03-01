from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



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
    w=db.collection("tbl_vacancy").stream()
    w_data=[]
    for i in w:
        data=i.to_dict()
        w_data.append({"w":data,"id":i.id})
    if request.method=="POST":
        data={"CompanyName":request.POST.get("CompanyName"),"vacancy_postion":request.POST.get("postion"),"vacancy_details":request.POST.get("Details")}
        db.collection("tbl_vacancy").add(data)
    return render(request,"Admin/vacancy.html",{"vacancy":w_data})
    
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


def viewreq(request):
    req=db.collection("tbl_request").where("request_status","==",0).stream()
    req_data=[]
    for i in req:
        data=i.to_dict()
        user=db.collection("tbl_userreg").document(data["user_id"]).get().to_dict()
        vacancy=db.collection("tbl_vacancy").document(data["vacancy_id"]).get().to_dict()
        req_data.append({"view":data,"id":i.id,"user":user,"vacancy":vacancy})
        # print(req_data)
    return render(request,"Admin/Viewrequest.html",{"view":req_data}) 
    
def accept(request,id):
    request = db.collection("tbl_request").document(id).get().to_dict()
    user = db.collection("tbl_userreg").document(request["user_id"]).get().to_dict()
    empid = user["user_id"]
    email = user["user_email"]
    send_mail(
        'Welcome To Our Company', 
        "\rHello \r\n Your request is accepted by our HR team. Now ur our employee.\n Thank you for ur corperation \r\n Thank you. \r\n By Exertion.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    db.collection("tbl_Employereg").add({"Employe_id":empid,"Employe_name":user["user_name"],"Emplpoye_contact":user["user_contact"],"Employe_email":user["user_email"],"Employe_address":user["user_address"],"Employe_gender":user["user_gender"],"Employe_photo":user["user_photo"],"place_id":user["place_id"]})
    db.collection("tbl_userreg").document(request["user_id"]).delete()
    db.collection("tbl_request").document(id).delete()
    return redirect("webadmin:viewreq")
    

def reject(request,id):
    req=db.collection("tbl_request").document(id).update({"request_status":2})
     
    return redirect("webuser:viewreq")
   