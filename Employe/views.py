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
  data = db.collection("tbl_attendence").where("employee","==",request.session["eid"]).where("date","==",str(datedata)).stream()
  count = 0
  for i in data:
    count = count + 1
  if count > 0:
    return render(request,"Employee/Homepage.html",{"msg":"Attendence is already added"})
  else:
    data={"date":str(datedata),"employee":request.session["eid"],"time":datetime.now()} 
    db.collection("tbl_attendence").add(data)
    return render(request,"Employee/Homepage.html",{"msg":"Attendence added"})


def complaint(request):
  if "eid" in request.session:
    com=db.collection("tbl_complaint").where("Employee_id","==",request.session["eid"]).stream()
    com_data=[]
    for i in com:
        data=i.to_dict()
        com_data.append({"com":data,"id":i.id})
    if request.method=="POST":
        datedata = date.today()
        data={"user_id":"","Employee_id":request.session["eid"],"complaint_content":request.POST.get("content"),"complaint_status":0,"complaint_date":str(datedata)}
        db.collection("tbl_complaint").add(data)
        return redirect("webemploye:complaint")
    else:
      return render(request,"Employee/Complaints.html",{"com":com_data})
  else:
    return render(request,"Guest/Login.html")

def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("webemploye:complaint")   

def logout(request):
  del request.session["uid"]
  return redirect("webguest:login")   