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
def district(request):
    if "aid" in request.session:
        dis=db.collection("tbl_district").stream()
        dis_data=[]
        for i in dis:
            data=i.to_dict()
            dis_data.append({"dis":data,"id":i.id})
        if request.method=="POST":
            data={"district_name":request.POST.get("District")}
            db.collection("tbl_district").add(data)
            return redirect("webadmin:district")
        else:
            return render(request,"Admin/District.html",{"district":dis_data})
    else:
        return render(request,"Guest/Login.html")   
    dis=db.collection("tbl_district").stream()
    dis_data=[]
    for i in dis:
        data=i.to_dict()
        dis_data.append({"dis":data,"id":i.id})
    if request.method=="POST":
        data={"district_name":request.POST.get("District")}
        db.collection("tbl_district").add(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"district":dis_data})
    

def deldistrict(request,id):
    db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:district")   

def editdistrict(request,id):
    dis=db.collection("tbl_district").document(id).get().to_dict()
    if request.method=="POST":
        data={"district_name":request.POST.get("District")}
        db.collection("tbl_district").document(id).update(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"dis_data":dis}) 
   
def Place(request):
    if "aid" in request.session:
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
            result.append({'district_data':district_dict,'place_data':place_dict,'placeid':place.id})
        if request.method=="POST":
            data={"place_name":request.POST.get("Place"),"district_id":request.POST.get("district")}
            db.collection("tbl_place").add(data)
            return redirect("webadmin:Place")
        else:
            return render(request,"Admin/Place.html",{"district":dis_data,"place":result})
    else:
            return render(request,"Guest/login.html")   

        
def delPlace(request,id):
    db.collection("tbl_place").document(id).delete()
    return redirect("webadmin:Place") 

def editPlace(request,id):
    db.collection()  


def vacancy(request):
    if "aid" in request.session:
        w=db.collection("tbl_vacancy").stream()
        w_data=[]
        for i in w:
            data=i.to_dict()
            w_data.append({"w":data,"id":i.id})
        if request.method=="POST":
            data={"CompanyName":request.POST.get("CompanyName"),"vacancy_postion":request.POST.get("postion"),"vacancy_details":request.POST.get("Details")}
            db.collection("tbl_vacancy").add(data)
        return render(request,"Admin/vacancy.html",{"vacancy":w_data})
    else:    
        return render(request,"Guest/login.html")   

        
def Employe(request):
    if "aid" in request.session:
        dis = db.collection("tbl_district").stream()
        dis_data = []
        for d in dis:
            dis_data.append({"dis":d.to_dict(),"id":d.id})
        w=db.collection("tbl_Employereg").stream()
        w_data=[]
        for i in w:
            data=i.to_dict()
            w_data.append({"w":data,"id":i.id})
        if request.method =="POST":
            email = request.POST.get("email")
            password = request.POST.get("Password")
            try:
                Employe = firebase_admin.auth.create_user(email=email,password=password)
            except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
                return render(request,"Admin/Employe.html",{"msg":error})
            image=request.FILES.get("photo")
            if image :
                path="EmployeePhoto/" + image.name
                st.child(path).put(image)
                e_url=st.child(path).get_url(None)
            db.collection("tbl_Employereg").add({"Employe_id":Employe.uid,"Employe_name":request.POST.get("name"),"Employe_contact":request.POST.get("contact"),"Employee_email":request.POST.get("email"),"Employee_address":request.POST.get("Address"),"Employee_gender":request.POST.get("Gender"),"Employee_photo":e_url,"place_id":request.POST.get("sel_place")})
            return redirect("webadmin:Employe")
        else:
            return render(request,"Admin/Employe.html",{"wdata":w_data,"district":dis_data}) 
    else:    
            return render(request,"Guest/login.html")               


def viewreq(request):
    if "aid" in request.session:
        req=db.collection("tbl_request").where("request_status","==",0).stream()
        req_data=[]
        for i in req:
            data=i.to_dict()
            user=db.collection("tbl_userreg").document(data["user_id"]).get().to_dict()
            vacancy=db.collection("tbl_vacancy").document(data["vacancy_id"]).get().to_dict()
            req_data.append({"view":data,"id":i.id,"user":user,"vacancy":vacancy})
            # print(req_data)
        return render(request,"Admin/Viewrequest.html",{"view":req_data}) 
    else:    
        return render(request,"Guest/login.html")   

        
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
    db.collection("tbl_Employereg").add({"Employe_id":empid,"Employe_name":user["user_name"],"Employe_contact":user["user_contact"],"Employee_email":user["user_email"],"Employee_address":user["user_address"],"Employee_gender":user["user_gender"],"Employee_photo":user["user_photo"],"place_id":user["place_id"]})
    db.collection("tbl_userreg").document(request["user_id"]).delete()
    db.collection("tbl_request").document(id).delete()
    return redirect("webadmin:viewreq")
    

def reject(request,id):
    req=db.collection("tbl_request").document(id).update({"request_status":2})
    return redirect("webuser:viewreq")
   
def homepage(request):
    if "aid" in request.session:
        return render(request,"Admin/Homepage.html") 
    else:
        return render(request,"Guest/login.html")   




def viewcomplaint(request):
    if "aid" in request.session:
        user_data=[]
        employee_data=[]
        ecom = db.collection("tbl_complaint").where("employee_id", "!=","").where("complaint_status", "==", 0).stream()
        for i in ecom:
            edata = i.to_dict()
            employee = db.collection("tbl_Employereg").document(edata["employee_id"]).get().to_dict()
            employee_data.append({"complaint":i.to_dict(),"id":i.id,"employee":employee})
        ucom=db.collection("tbl_complaint").where("user_id","!=",0).where("complaint_status","==",0).stream()
        for i in ucom:
            udata = i.to_dict()
            user = db.collection("tbl_userreg").document(udata["user_id"]).get().to_dict()
            user_data.append({"complaint":i.to_dict(),"id":i.id,"user":user}) 
        return render(request,"Admin/ViewComplaints.html",{"user":user_data,"employee":employee_data}) 
    else:    
        return render(request,"Guest/login.html")         

def reply(request,id):
    if request.method == "POST":
            db.collection("tbl_complaint").document(id).update({"complaint_reply":request.POST.get("reply"),"complaint_status":"1"})
            return render(request,"Admin/Reply.html",{"msg":"Reply Sended..."})
    return render(request,"Admin/Reply.html")    

def logout(request):
  del request.session["uid"]
  return redirect("webguest:login")      


def viewattendance(request,id):
    attendance=db.collection("tbl_attendence").where("employee","==",request.session["eid"]).stream()
    attendance_data=[]
    for i in attendance:
        data=i.to_dict()
        attendance_data.append({"attendance":data,"id":i.id})
        print(attendance_data)
    return render(request,"Admin/ViewAttendance.html",{"attendance":attendance_data})    


def viewemployee(request):
    if "aid" in request.session:
        w=db.collection("tbl_Employereg").stream()
        w_data=[]
        for i in w:
            data=i.to_dict()
            w_data.append({"w":data,"id":i.id})
        return render(request,"Admin/ViewEmployee.html",{"wdata":w_data})
    else:
        return render(request,"Guest/login.html")    


def admin(request):
    # if "aid" in request.session:
        if request.method =="POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                admin = firebase_admin.auth.create_user(email=email,password=password)
            except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
                return render(request,"Admin/Admin.html",{"msg":error})
            db.collection("tbl_admin").add({"admin_id":admin.uid,"admin_name":request.POST.get("name"),"admin_contact":request.POST.get("contact"),"admin_email":request.POST.get("email")})    
            return render(request,"Admin/Admin.html")
        else:
            return render(request,"Admin/Admin.html")
    # else:
    #     return render(request,"Guest/Login.html")        