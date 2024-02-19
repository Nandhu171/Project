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

def homepage(request):
    return render(request,"Employee/Homepage.html")


def Myprofile (request):
    Employee = db.collection("tbl_Employeereg").document(request.session["uid"]).get().to_dict()
    return render(request,"Employee/Myprofile.html",{"Employee":Employee})

  
def Editprofile(request):
  Employee = db.collection("tbl_Employeereg").document(request.session["uid"]).get().to_dict()
  if request.method=="POST":
    data={"Employee_name":request.POST.get("name"),"Employee_contact":request.POST.get("contact"),"Employee_address":request.POST.get("address")}
    db.collection("tbl_Employeereg").document(request.session["uid"]).update(data)
    return redirect("webEmployee:Myprofile")
  else:
    return render(request,"Employee/EditProfile.html",{"Employee":Employee})  

def changepassword(request):
  Employee = db.collection("tbl_Employeereg").document(request.session["uid"]).get().to_dict()
  email = Employee["Employee_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET Employee.",#body
    settings.EMAIL_HOST_Employee,
    [email],
  )
  return render(request,"Employee/Homepage.html",{"msg":email})    
