from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase



db=firestore.client()

config = {
  "apiKey": "AIzaSyAypXmHlJ5uXI6N3z9hICj3-mAGy9em3T8",
  "authDomain": "exertion-b2ee3.firebaseapp.com",
  "projectId": "exertion-b2ee3",
  "storageBucket": "exertion-b2ee3.appspot.com",
  "messagingSenderId": "1074924172707",
  "appId": "1:1074924172707:web:62328a7a069ca273fd5616",
  "measurementId": "G-YMBJCPKLRV",
  "databaseURL" : ""
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
st = firebase.storage()

# Create your views here.
def Userregistraction(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
      dis_data.append({"dis":d.to_dict(),"id":d.id})
    if request.method =="POST":
      email = request.POST.get("uemail")
      password = request.POST.get("password")
      try:
        
        user = firebase_admin.auth.create_user(email=email,password=password)
      except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
        return render(request,"Guest/Userregistration.html",{"msg":error})
      image = request.FILES.get("photo")
      if image:
        path = "UserPhoto/" + image.name
        st.child(path).put(image)
        u_url = st.child(path).get_url(None)
      db.collection("tbl_userreg").add({"user_id":user.uid,"user_name":request.POST.get("uname"),"user_contact":request.POST.get("ucontact"),"user_email":request.POST.get("uemail"),"user_address":request.POST.get("address"),"user_gender":request.POST.get("Gender"),"place_id":request.POST.get("sel_place"),"user_photo":u_url})
      return render(request,"Guest/Userregistration.html")
    else:
      return render(request,"Guest/Userregistration.html",{"district":dis_data})

def Login(request):
  Employeid=""
  userid=""
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
      data = authe.sign_in_with_email_and_password(email,password)
    except:
      return render(request,"Guest/Login.html",{"msg":"Error in Email Or Password"})
    print(data["localId"])
    user=db.collection("tbl_userreg").where("user_id","==",data["localId"]).stream()    
    for u in user:
      userid=u.id 
    Employee=db.collection("tbl_Employereg").where("Employe_id","==",data["localId"]).stream()  
    for e in Employee:
      Employeid=e.id  
    if userid:
      request.session["uid"]=userid
      return redirect("webuser:homepage")
    elif Employeid:
      request.session["eid"]=Employeid
      return redirect("webemploye:homepage")
    else:
      return render(request,"Guest/Login.html",{"msg":"error"})    
  else:
    return render(request,"Guest/Login.html")       

def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id", "==", request.GET.get("did")).stream()
    place_data = []
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})
  

def index(request):
  return render(request,"Guest/index.html")
