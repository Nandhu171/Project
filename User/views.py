from django.shortcuts import render,redirect
import firebase_admin 
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
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



def homepage(request):
    return render(request,"User/Homepage.html")


def Myprofile (request):
    user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
    return render(request,"User/Myprofile.html",{"user":user})

def Editprofile(request):
  user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
  if request.method=="POST":
    data={"user_name":request.POST.get("name"),"user_contact":request.POST.get("contact"),"user_address":request.POST.get("address")}
    db.collection("tbl_userreg").document(request.session["uid"]).update(data)
    return redirect("webuser:Myprofile")
  else:
    return render(request,"User/EditProfile.html",{"user":user})  

def changepassword(request):
  user = db.collection("tbl_userreg").document(request.session["uid"]).get().to_dict()
  email = user["user_email"]
  password_link = firebase_admin.auth.generate_password_reset_link(email) 
  send_mail(
    'Reset your password ', 
    "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + password_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET user.",#body
    settings.EMAIL_HOST_USER,
    [email],
  )
  return render(request,"User/Homepage.html",{"msg":email})    


def viewvacancy(request):
    w=db.collection("tbl_vacancy").stream()
    w_data=[]
    for i in w:
        data=i.to_dict()
        w_data.append({"w":data,"id":i.id})
        return render(request,"User/viewvacancy.html",{"vacancy":w_data})

def sendreq(request,id):
  if request.method=="POST":
    Resume = request.FILES.get("Resume")
    print(Resume)
    if Resume:
      path = "UserResume/" + Resume.name
      st.child(path).put(Resume)
      u_url = st.child(path).get_url(None)
    data={"vacancy_id":id,"user_id":request.session["uid"],"request_status":0,"user_resume":u_url} 
    db.collection("tbl_request").add(data)
    return redirect("webuser:viewvacancy")
  else:  
    return render(request,"User/SendRequest.html")   
  
<<<<<<< HEAD


def logout(request):
  del request.session["uid"]
  return redirect("webguest:Login")



def complaint(request):
  com=db.collection("tbl_complaint").where("user_id","==",request.session["uid"]).stream()
  com_data=[]
  for i in com:
      data=i.to_dict()
      com_data.append({"com":data,"id":i.id})
  if request.method=="POST":
      datedata = date.today()
      data={"user_id":request.session["uid"],"Employee_id":"","complaint_content":request.POST.get("content"),"complaint_status":0,"complaint_date":str(datedata)}
      db.collection("tbl_complaint").add(data)
      return redirect("webuser:complaint")
  else:
    return render(request,"User/Complaint.html",{"com":com_data})


def delcomplaint(request,id):
  db.collection("tbl_complaint").document(id).delete()     
  return redirect("webuser:complaint")  
=======
  
def logout(request):
  del request.session["uid"]
  return redirect("webguest:login")
>>>>>>> 6747d5d6cace1e7dff62efc55c1e8b7e82695daa
