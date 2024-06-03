from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import request
from rest_framework.views import APIView
from  .models import *
from datetime import datetime as dt
# Create your views here.

from .serializers import UserTblSerializers

class LoginPage(APIView):
    @csrf_exempt
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("username",username)
        print("password",password)
        check_data = UserTbl.objects.get(username=username,password=password)
        if check_data:
            request.session['id']=check_data.id
            userid = request.session['id']
            user_completed_todo = Todotable.objects.filter(userid=userid, status="completed").count()
            print("user_compelted_todo", user_completed_todo)
            user_pending_todo = Todotable.objects.filter(userid=userid, status="pending").count()
            print("user_pending_todo", user_pending_todo)
            response_data ={
                "status":"success",
                "name":check_data.name,
                "id":userid,
                "user_pending_todo": user_pending_todo,
                "user_compelted_todo": user_completed_todo,

            }
            return  JsonResponse(response_data)
        else:
            return JsonResponse({'status': 'error'})


class Logout(APIView):
    @csrf_exempt
    def post(self,request):
        del request.session['id']
        return JsonResponse({'status': 'error'})


class ToDo(APIView):
    @csrf_exempt
    def post(self,request):
        id = request.data.get('id')
        user_todo = Todotable.objects.filter(userid=id)
        print("user_todo",user_todo)
        if user_todo.exists():
            new_list = []
            for i in user_todo:
                data = {
                    "taskname":i.taskname,
                    "date":i.date,
                    "description":i.description,
                    "status":i.status,
                    "userid":i.userid.id,
                }
            new_list.append(data)
            return JsonResponse(new_list,safe=False)
        else:
            return JsonResponse(None, safe=False)


class TaskInsert(APIView):
    @csrf_exempt
    def post(self,request):
        id = request.data.get('id')
        taskName = request.data.get('taskName')
        description = request.data.get('description')
        dateinput1 = request.data.get('dateinput1')
        status = "pending"
        try:
            user_id=UserTbl.objects.get(id=id)
            val=user_id.id
            user_todo = Todotable(userid=user_id,taskname=taskName,date=dateinput1,status=status,description=description)
            user_todo.save()
            return JsonResponse({"status":"success"},safe=False)
        except Exception as e:
            print("exception",e)
            return JsonResponse(None, safe=False)


#----------------------------------------------------------------------------------------------------------#

# HTML #

def login(request):
    return render(request,'loginPage.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = UserTbl.objects.get(username=username, password=password)
        new_list = []
        if user:
            request.session['id'] =  user.id
            user_id = request.session['id']
            dt_date = dt.now().date()
            print("dt_date",dt_date)
            user_todo = Todotable.objects.filter(userid=user_id,date=dt_date,isdelete=0)
            print("user_todo",user_todo)
            # if user_todo.exists():
            #     for i in user_todo:
            #         data = {
            #             "taskname":i.taskname,
            #             "date":i.date,
            #             "description":i.description,
            #             "status":i.status,
            #             "userid":i.userid.id,
            #         }
            #     new_list.append(data)
            #     print("new_list",new_list) 
            return render(request, 'index.html',{'user_todo':user_todo})
        else:
            return HttpResponse('<script>alert("Invalid username or password");window.location="/login/"</script>')
    else:
        return render(request, 'loginPage.html')



def todoinsert(request):
    if request.method=='POST':
        user_id = request.session['id']
        taskName = request.POST['taskName']
        description = request.POST['description']
        dateinput1 = request.POST['dateinput1']
        color = request.POST['color']
        isdelete=0
        status = "pending"
        try:
            user_id=UserTbl.objects.get(id=user_id)
            val=user_id.id
            user_todo = Todotable(userid=user_id,taskname=taskName,date=dateinput1,color=color,status=status,description=description,isdelete=isdelete)
            user_todo.save()
            return HttpResponse('<script>alert("Successfully Added");window.location="/user_login/"</script>')
        except Exception as e:
            print("exception",e)
            return render(request, 'index.html')


def viewtodo(request):
    if request.method=='POST':
        user_id = request.session['id']
        dt_date = dt.now().date()
        dateinput1 = dt_date
        status = request.POST['status']
        print("status",status)
        try:
            user_id=UserTbl.objects.get(id=user_id)
            val=user_id.id
            user_todo_data = Todotable.objects.filter(userid=user_id,date=dateinput1,status=status)
            todo_list = []
            for i in user_todo_data:
                todo_data = {
                "taskName":i.taskname,
                "description":i.description,
                "user_id":i.userid.id,
                "status":i.status,
                "id":i.id
                }
                todo_list.append(todo_data)
                print("todo_list",todo_list)
            return JsonResponse(todo_list,safe=False)
        except Exception as e:
            print("error",e)
            return JsonResponse({"status":"error"},safe=False)


def todo_delete(request):
    if request.method == 'POST':
        try:
            user_id = request.session['id']
            todo_id = request.POST.get('todo_id')  # Get the ID of the to-do item to be deleted
            user_todo_data = Todotable.objects.get(userid=user_id, id=todo_id)
            user_todo_data.status = "completed"
            user_todo_data.isdelete = 1
            user_todo_data.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("error", e)
            return JsonResponse({'status': 'error'})
    else:
        return render(request, 'index.html')



def todo_view(request):
    if request.method == 'POST':
        try:
            todo_id = request.POST.get('todo_id') 
            print("todo_id",todo_id) # Get the ID of the to-do item to be deleted
            user_todo_data = Todotable.objects.get(id=todo_id)
            todo_data = [{
            "id":user_todo_data.id,
            "taskname":user_todo_data.taskname,
            "date":user_todo_data.date,
            "description":user_todo_data.description,
            "status":user_todo_data.status,
            "color":user_todo_data.color
            }]
            print("todo_data",todo_data)
            return JsonResponse(todo_data,safe=False)
        except Exception as e:
            print("error", e)
            return JsonResponse({'status': 'error'})
    else:
        return render(request, 'index.html')

def todo_update(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('id') 
            user_todo_data = Todotable.objects.get(id=id)
            user_todo_data.taskname = request.POST.get('taskname')
            user_todo_data.date = request.POST.get('date')
            user_todo_data.description = request.POST.get('description')
            user_todo_data.save()
            return HttpResponse('<script>alert("Successfully Updated");window.location="/user_login/"</script>')
        except Exception as e:
            print("error", e)
            return JsonResponse({'status': 'error'})
    else:
        return render(request, 'index.html')



def todo_logout(request):
    if request.method == 'POST':
        try:
            user_id = request.session['id']
            todo_id = request.POST.get('todo_id')  # Get the ID of the to-do item to be deleted
            user_todo_data = UserTbl.objects.get(id=user_id)
            user_todo_data.status = "completed"
            del request.session['id']
            return HttpResponse('<script>alert("Logout successfully");window.location="/login/";</script>')
        except Exception as e:
            print("error", e)
            return HttpResponse('<script>alert("Error");window.location="/login/";</script>')
    else:
        return render(request, 'index.html')
