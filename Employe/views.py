from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from datetime import date,datetime


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

def homepage(request):
    return render(request,"Employee/Homepage.html")


def Myprofile (request):
    Employee = db.collection("tbl_Employereg").document(request.session["eid"]).get().to_dict()
    
    return render(request,"Employee/Myprofile.html",{"Employee":Employee})
   
  
def Editprofile(request):
  Employee = db.collection("tbl_Employereg").document(request.session["uid"]).get().to_dict()
  if request.method=="POST":
    data={"Employee_name":request.POST.get("name"),"Employee_contact":request.POST.get("contact"),"Employee_address":request.POST.get("address")}
    db.collection("tbl_Employereg").document(request.session["eid"]).update(data)
    return redirect("webemploye:Myprofile")
  else:
    return render(request,"Employee/EditProfile.html",{"Employee":Employee})  

def changepassword(request):
  Employee = db.collection("tbl_Employereg").document(request.session["uid"]).get().to_dict()
  email = Employee["Employe_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET Employee.",#body
    settings.EMAIL_HOST_USER,
    [email],
  )
  return render(request,"Employee/Homepage.html",{"msg":email})  

def work(request):
    if request.method=="POST":
        data={"Description_name":request.POST.get("description"),"work_name":request.POST.get("work")}
        db.collection("tbl_workdetails").add(data)
    return render(request,"Employee/Work.html")

def attendence(request):
  datedata=date.today()  
  time = datetime.now()
  data = db.collection("tbl_attendence").where("employee","==",request.session["uid"]).where("date","==",str(datedata)).stream()
  count = 0
  for i in data:
    count = count + 1
  if count > 0:
    return render(request,"Employee/Homepage.html",{"msg":"Attendence is already added"})
  else:
    data={"date":str(datedata),"employee":request.session["uid"],"time":str(time)} 
    db.collection("tbl_attendence").add(data)
    return render(request,"Employee/Homepage.html",{"msg":"Attendence added"})