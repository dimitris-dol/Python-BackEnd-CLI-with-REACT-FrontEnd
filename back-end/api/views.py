from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from api.models import *
from api.forms import *
from rest_framework import viewsets
from api.serializers import *
import bcrypt
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import django_excel as excel
from django import forms
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework import views
import json
import unicodecsv
import jwt
from operator import itemgetter
from django.db.models import Sum
import csv
from datetime import datetime
from io import StringIO
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import *
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.template import Context, loader

#Den yparxei to email sti database
class newuser(views.APIView):
    def post(self,request,*args,**kwargs):
        token = request.headers['headers']
        user = User.objects.filter(loginname = 'admin')
        if user[0].api_key != token:
            return HttpResponse(status = 401)
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))
        email = request.POST.get('email')
        quotas = request.POST.get('quotas')
        time = timezone.now().date()
        with connection.cursor() as cursor:
            user = User.objects.filter(loginname = username)
            if user is not None:
                return JsonResponse({'token' : 'already exists'})
            cursor.execute('INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(username,password,None,None,email,None,0,time,quotas))
        user = User.objects.filter(loginname = username)
        user[0].save()
        jwt_token = {'token' : user[0].api_key}
        return JsonResponse(jwt_token)

#Den yparxei to email sth database
#Xreiazetai na leei an den uparxei xristis??
class moduser(views.APIView):
    def post(self,request,*args,**kwargs):
        token = request.headers['headers']
        user = User.objects.filter(loginname = 'admin')
        if user[0].api_key != token:
            return HttpResponse(status = 401)
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))
        email = request.POST.get('email')
        quotas = request.POST.get('quotas')
        with connection.cursor() as cursor:
            cursor.execute('''UPDATE user
                              SET Password = %s,
                                  email = %s,
                                  quotas = %s
                              WHERE LoginName = %s''',(password,email,quotas,username))
        return JsonResponse({'status':'OK'})


class userstatus(views.APIView):
    def post(self,request,*args,**kwargs):
        token = request.headers['headers']
        user = User.objects.filter(loginname = 'admin')
        if user[0].api_key != token:
            return HttpResponse(status = 401)
        username = request.POST.get('username')
        with connection.cursor() as cursor:
            cursor.execute('''SELECT api_key, quotas, counter, dateOfkey, email
                            FROM user
                            WHERE LoginName = %s''',[username])
            table = cursor.fetchall()
            try:
                return JsonResponse({'username': username,
                                'API key' : table[0][0],
                                'email' : table[0][4],
                                'quota' : table[0][1],
                                'Current Period' : table[0][3],
                                'Remaining calls' : table[0][1] - table[0][2]})
            except:
                return JsonResponse({username : 'does not exist'})


class newdata(views.APIView):
    def post(self,request,*args,**kwargs):
        token = request.headers['headers']
        user = User.objects.filter(loginname = 'admin')
        if user[0].api_key != token:
            return HttpResponse(status = 401)
        if request.POST and request.FILES:
            type = request.POST['type']
            filename = request.POST['filename']
            csvfile = request.FILES['file']
            csv_file = csvfile.open()
            csv_reader = unicodecsv.reader(csv_file, delimiter=',')
            with connection.cursor() as cursor:
                try:
                    counter = 0
                    if type == 'ActualTotalLoad':
                        cursor.execute('SELECT COUNT(id) FROM Actualtotalload')
                    elif type == 'AggregatedGenerationPerType':
                        cursor.execute('SELECT COUNT(id) FROM Aggregatedgenerationpertype')
                    elif type == 'DayAheadTotalLoadForecast':
                        cursor.execute('SELECT COUNT(id) FROM Dayaheadtotalloadforecast')
                    init = int(cursor.fetchall()[0][0])
                    for cr in csv_reader:
                        counter = counter + 1
                        if counter == 1:
                            continue
                        c = cr[0].split(';')
                        if type == 'ActualTotalLoad': #16
                            cursor.execute('INSERT INTO Actualtotalload VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Entitymodifiedat = %s',(c[0],datetime.strptime(c[1].split('.')[0],'%Y-%m-%d %H:%M:%S'),datetime.strptime(c[2].split('.')[0],'%Y-%m-%d %H:%M:%S'),c[3],None,c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],c[16],datetime.strptime(c[2].split('.')[0],'%Y-%m-%d %H:%M:%S')))
                        elif type == 'AggregatedGenerationPerType': #18
                            cursor.execute('INSERT INTO Aggregatedgenerationpertype VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Entitymodifiedat = %s',(c[0],datetime.strptime(c[1].split('.')[0],'%Y-%m-%d %H:%M:%S'),datetime.strptime(c[2].split('.')[0],'%Y-%m-%d %H:%M:%S'),c[3],None,c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],c[16],c[17],c[18],datetime.strptime(c[2].split('.')[0],'%Y-%m-%d %H:%M:%S')))
                        elif type == 'DayAheadTotalLoadForecast': #16
                            cursor.execute('INSERT INTO Dayaheadtotalloadforecast VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Entitymodifiedat = %s',(c[0],datetime.strptime(c[1].split('.')[0],'%Y-%m-%d %H:%M:%S'),datetime.strptime(c[2].split('.')[0],'%Y-%m-%d %H:%M:%S'),c[3],None,c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],c[16],datetime.strptime(c[2].split('.')[0],'%Y-%m-%d %H:%M:%S')))
                    if type == 'ActualTotalLoad':
                        cursor.execute('SELECT COUNT(id) FROM Actualtotalload')
                    elif type == 'AggregatedGenerationPerType':
                        cursor.execute('SELECT COUNT(id) FROM Aggregatedgenerationpertype')
                    elif type == 'DayAheadTotalLoadForecast':
                        cursor.execute('SELECT COUNT(id) FROM Dayaheadtotalloadforecast')
                    fin = int(cursor.fetchall()[0][0])
                except:
                    return JsonResponse({'file' : 'invalid content'})
            return JsonResponse({'status' : 'ok',
                                'num of data in file' : counter-1,
                                'number of added data' : fin - init,
                                'number of data in database' : fin})
        return JsonResponse({'status' : 'upload failed'})



#destroy everything
def reset(request):
    Actualtotalload.objects.all().delete()
    Aggregatedgenerationpertype.objects.all().delete()
    Dayaheadtotalloadforecast.objects.all().delete()
    User.objects.all().delete()
    Allocatedeicdetail.objects.all().delete()
    Areatypecode.objects.all().delete()
    Mapcode.objects.all().delete()
    Productiontype.objects.all().delete()
    Resolutioncode.objects.all().delete()
    User.objects.create(loginname = 'admin', password = '321nimda' , email = 'ex@gmail.com' , dateOfkey = datetime.now() , quotas = 1)
    return JsonResponse({'status':'OK'})

#Login class after submit button on webpage
class Login(views.APIView):
    def post(self,request,*args,**kwargs):
        if not request.data:
            return HttpResponse({'Error: please provide username and password'}, status=400)
        username = request.POST.get('username')
        password = request.POST.get('password')
        #request.content_type = "application/x-www-form-urlencoded"
        user = User.objects.filter(loginname = username)
        if User.objects.filter(loginname = username).exists() == False:
            return HttpResponse({'Error: invalid username or password'},status=400)
        gg = check_password(password,user[0].password)
        ggg = make_password(password)
        user[0].save()
        if gg or ggg == user[0].password:
            jwt_token = {'token' : user[0].api_key}
            return JsonResponse(
                jwt_token
            )
        else:
            return HttpResponse(
                "error: invalid credentials",
                status=400,
                content_type="application/json"
            )

#logout seesion--under construction
class Logout(views.APIView):
    def post(self,request,*args,**kwargs):
        #del request #deletiung token
        template = loader.get_template("log.html")
        return HttpResponse(template.render(),status=200)

#not used
class UploadFileForm(forms.Form):
    file = forms.FileField()

#Authentication
def auth_token(token):
    users = User.objects.all()
    flag = False
    for dd in users:
        if token.find(dd.api_key) > -1 and (len(token) - len(dd.api_key)) <=20:
            user = dd
            flag = True
            break
    if flag == False:
        return 1
    if timezone.now().date() == user.dateOfkey.date():
        ttt = user.quotas
        if user.counter >= user.quotas:
            return 0
        else:
            user.counter = user.counter + 1
            user.save()
            return 2
    else:
        user.dateOfkey=timezone.now()
        user.counter=1
        user.save()
    return 2

#fix for only admin
def usss(request,username):
    user = User.objects.filter(loginname=username)
    serializer = UserSerializer(user,many=True)
    return JsonResponse(serializer.data,json_dumps_params={'indent': 2},safe=False)


#upload file not used
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(),"csv",file_name = "download")
    else:
        form = UploadFileForm()
    return render(request,'upload_form.html',{'form': form, 'title': 'Excel file and download', 'header' : ('Please choose any excel file '  +  'from your pc')})



#Healtcheck
def process_request(request):
        try:
            u = Allocatedeicdetail.objects.all()
            success = True
        except:
            success = False

        if success == True:
            j = {"status":"OK"}
            return JsonResponse(j)
        else:
            j = {"status" : "NOT OK"}
            return JsonResponse(j)

#@crsf_exempt
#returns all users
def user_list(request):
    if request.method =='GET':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return JsonResponse(serializer.data,json_dumps_params={'indent': 2},safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

#@csrf_exempt
#return user from hiw userid
def user_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user,data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

#returns all actualTotalLoads objects
#@login_required(login_url='/api/Login')
def actualtotalload_list(request):
    if request.method == 'POST':
        actualtotalloads = Actualtotalload.objects.all()
        data_to_export = []
        for data in actualtotalloads:
            areatype = data.areatypecodeid.areatypecodetext
            map = data.mapcodeid.mapcodetext
            resolution = data.resolutioncodeid.resolutioncodetext
            data_to_export.append({
            'source': 'entsoe',
            'dataset': 'Actualtotalload',
            'areaname': data.areaname,
            'areatypecode': areatype,
            'mapcode': map,
            'resolutioncode': resolution,
            'year': data.year,
            'month': data.month,
            'day': data.day,
            'datetimeUTC': data.datetime,
            'ActualTotalLoadValue' : data.totalloadvalue,
            'updatetimeUTC' : data.updatetime
            })
        return JsonResponse(data_to_export,json_dumps_params={'indent': 2},safe = False)

#actual total load
#@login_required(login_url='home')
def actual(request,areaname,resolutioncode,date,info):
    t = ['PT15M','PT60M','PT30M','P7D','P1M','P1Y','P1D','CONTRACT']
    if resolutioncode not in t:
        return HttpResponse(status=400)
    if date == 'date':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        tmp = info[8:10]
        day = int(tmp)
        format = 'json'
        if info.find('csv') >-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token) == 2:
            return actualtotalload_detail2(request,areaname,resolutioncode,year,month,day,format)
        elif auth_token(token) ==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'month':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return actualtotalload_detail1(request,areaname,resolutioncode,year,month,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'year':
        tmp = info[0:4]
        year = int(tmp)
        format = 'json'
        if info.find('csv') > -1:
            format = 'csv'
        print(format)
        token = request.headers['headers']
        print("gg")
        print(token)
        if auth_token(token)==2:
            return actualtotalload_detail(request,areaname,resolutioncode,year,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    else:
        return HttpResponse(status=400)

#aggregated generation per type
#@login_required(login_url='/api/Login')
def aggre(request,areaname,productiontype,resolutioncode,date,info):
    t = ['PT15M','PT60M','PT30M','P7D','P1M','P1Y','P1D','CONTRACT']
    if resolutioncode not in t:
        return HttpResponse(status=400)
    t1 = ['Fossil Gas','Hydro Run-of-river and poundage','Hydro Pumped Storage','Hydro Water Reservoir','Fossil Hard coal','Nuclear','Fossil Brown coal/Lignite','Fossil Oil','Fossil Oil shale','Biomass','Fossil Peat','Wind Onshore','Other','Wind Offshore','Fossil Coal-derived gas','Waste','Solar','Geothermal','Other renewable','Marine','AC Link','Transformer','DC Link','Substation']
    if productiontype not in t1:
        return HttpResponse(status=400)
    if date == 'date':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        tmp = info[8:10]
        day = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return aggregatedgenerationpertype_detail2(request,areaname,productiontype,resolutioncode,year,month,day,format)
        elif auth_token(token) ==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'month':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return aggregatedgenerationpertype_detail1(request,areaname,productiontype,resolutioncode,year,month,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'year':
        tmp = info[0:4]
        year = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return aggregatedgenerationpertype_detail(request,areaname,productiontype,resolutioncode,year,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    else:
        return HttpResponse(status=400)

#dayahead total load forecast
#@login_required(login_url='/api/Login')
def dayahead(request,areaname,resolutioncode,date,info):
    t = ['PT15M','PT60M','PT30M','P7D','P1M','P1Y','P1D','CONTRACT']
    if resolutioncode not in t:
        return HttpResponse(status=400)
    if date == 'date':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        tmp = info[8:10]
        day = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return dayaheadtotalloadforecast_detail2(request,areaname,resolutioncode,year,month,day,format)
        elif auth_token(token) ==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'month':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return dayaheadtotalloadforecast_detail1(request,areaname,resolutioncode,year,month,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'year':
        tmp = info[0:4]
        year = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return dayaheadtotalloadforecast_detail(request,areaname,resolutioncode,year,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    else:
        return HttpResponse(status=400)

#actual total load versu day ahead total load forecast
##@login_required(login_url='/api/Login')
def actualvs(request,areaname,resolutioncode,date,info):
    t = ['PT15M','PT60M','PT30M','P7D','P1M','P1Y','P1D','CONTRACT']
    if resolutioncode not in t:
        return HttpResponse(status=400)
    if date == 'date':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        tmp = info[8:10]
        day = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return actualvsforecast_detail2(request,areaname,resolutioncode,year,month,day,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'month':
        tmp = info[0:4]
        year = int(tmp)
        tmp = info[5:7]
        month = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'

        token = request.headers['headers']
        if auth_token(token)==2:
            return actualvsforecast_detail1(request,areaname,resolutioncode,year,month,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    elif date == 'year':
        tmp = info[0:4]
        year = int(tmp)
        format = 'json'
        if info.find('csv')>-1:
            format = 'csv'
        token = request.headers['headers']
        if auth_token(token)==2:
            return actualvsforecast_detail(request,areaname,resolutioncode,year,format)
        elif auth_token(token)==1 :
            return HttpResponse({'Not Authorized'},status = 401)
        else:
            return HttpResponse({'Out of Quotas'},status = 402)
    else:
        return HttpResponse(status=400)

#actualtotalload
def actualtotalload_detail2(request,areaname,resolutioncode,year,month,day,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    resolutioncodeid = tmp[0].id
    data_to_export = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=month,day=day)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode = dd.mapcodeid.mapcodetext
        data.append({
        'Source': 'entso-e',
        'Dataset': 'ActualTotalLoad',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'DateTimeUTC': dd.datetime,
        'ActualTotalLoadValue': dd.totalloadvalue,
        'UpdateTimeUTC':dd.updatetime
        })
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['DateTimeUTC'])
        if  format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','datetime','actualtotalloadvalue','updatetime']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "ActualTotalLoad.csv"'
                return response
        else:
            return HttpResponse(status=400)

def actualtotalload_detail1(request,areaname,resolutioncode,year,month,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    resolutioncodeid = tmp[0].id
    data_to_export = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=month)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode = dd.mapcodeid.mapcodetext
        sum = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=month,day =dd.day,areatypecodeid = dd.areatypecodeid,mapcodeid = dd.mapcodeid).aggregate(Sum('totalloadvalue'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'ActualTotalLoad',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'ActualTotalLoadByDayValue': sum['totalloadvalue__sum'],
        })
        if temp  not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Day'])
        if format =='json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','actualtotalloadvalue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "ActualTotalLoad.csv"'
                return response
        else:
            return HttpResponse("Bad rerquest")


def actualtotalload_detail(request,areaname,resolutioncode,year,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    resolutioncodeid = tmp[0].id
    data_to_export = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode = dd.mapcodeid.mapcodetext
        sum = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=dd.month,areatypecodeid = dd.areatypecodeid,mapcodeid = dd.mapcodeid).aggregate(Sum('totalloadvalue'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'ActualTotalLoad',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'ActualTotalLoadByMonthValue': sum['totalloadvalue__sum'],
        })
        if temp  not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Month'])
        if format=='json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format=='csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','actualtotalloadvalue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "ActualTotalLoad.csv"'
                return response
        else:
            return HttpResponse(status=400)

#Aggregatedgenerationpertype
def aggregatedgenerationpertype_list(request):
    agge = Aggregatedgenerationpertype.objects.all()
    data_to_export = []
    for data in agge:
        areatype = data.areatypecodeid.areatypecodetext
        map = data.mapcodeid.mapcodetext
        resolution = data.resolutioncodeid.resolutioncodetext
        production = data.productiontypeid.productiontypetext
        data_to_export.append({
        'Source': 'entso-e',
        'Dataset': 'Aggregatedgenerationpertype',
        'AreaName': data.areaname,
        'AreaTypeCode': areatype,
        'MapCode': map,
        'ResolutionCode': resolution,
        'Year': data.year,
        'Month': data.month,
        'Day': data.day,
        'DateTimeUTC': data.datetime,
        'ProductionType': production,
        'ActualGenerationOutputValue': data.actualgenerationoutput,
        'UpdateTimeUTC':data.updatetime
        })
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        return JsonResponse(data_to_export,json_dumps_params={'indent': 2},safe = False)


#@csrf_exempt
def aggregatedgenerationpertype_detail2(request,areaname,productiontype,resolutioncode,year,month,day,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    tmp2 = Productiontype.objects.filter(productiontypetext = productiontype)
    data_to_export = Aggregatedgenerationpertype.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id, productiontypeid = tmp2[0].id,year = year, month = month, day = day)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode =dd.mapcodeid.mapcodetext
        data.append({
        'Source': 'entso-e',
        'Dataset': 'Aggregatedgenerationpertype',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'DateTimeUTC': dd.datetime,
        'ProductionType': productiontype,
        'ActualGenerationOutputValue': dd.actualgenerationoutput,
        'UpdateTimeUTC':dd.updatetime
        })
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['DateTimeUTC'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format =='csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','datetime','productiontype','ActualGenerationOutputValue','updatetime']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "AggreatedGenerationPerType.csv"'
                return response
        else:
            return HttpResponse(status=400)

def aggregatedgenerationpertype_detail1(request,areaname,productiontype,resolutioncode,year,month,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    tmp2 = Productiontype.objects.filter(productiontypetext = productiontype)
    data_to_export = Aggregatedgenerationpertype.objects.filter(areaname = areaname, resolutioncodeid = tmp[0], productiontypeid = tmp2[0].id,year = year, month = month)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode =dd.mapcodeid.mapcodetext
        sum = Aggregatedgenerationpertype.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id, productiontypeid = tmp2[0].id,year = year, month = month,day = dd.day,areatypecodeid = dd.areatypecodeid,mapcodeid = dd.mapcodeid).aggregate(Sum('actualgenerationoutput'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'AggregatedGenerationPerType',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'ProductionType': productiontype,
        'ActualGenerationOutputByDayValue': sum['actualgenerationoutput__sum'] ,
        })
        if temp not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Day'])
        if format=='json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format=='csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','productiontype','ActualGenerationOutputValue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "AggreatedGenerationPerType.csv"'
                return response
        else:
            return HttpResponse(status=400)

def aggregatedgenerationpertype_detail(request,areaname,productiontype,resolutioncode,year,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    tmp2 = Productiontype.objects.filter(productiontypetext = productiontype)
    data_to_export = Aggregatedgenerationpertype.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id, productiontypeid = tmp2[0].id,year = year)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode =dd.mapcodeid.mapcodetext
        sum = Aggregatedgenerationpertype.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id, productiontypeid = tmp2[0].id,year = year, month = dd.month,areatypecodeid = dd.areatypecodeid,mapcodeid = dd.mapcodeid).aggregate(Sum('actualgenerationoutput'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'Aggregatedgenerationpertype',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Productiontype': productiontype,
        'ActualGenerationOutputByMonthValue': sum['actualgenerationoutput__sum'],
        })
        if temp not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Month'])
        if format == 'json':
            return JsonResponse(data,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','productiontype','ActualGenerationOutputValue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "AggreatedGenerationPerType.csv"'
                return response
        else:
            return HttpResponse(status=400)

#dayaheadtotalloadforecast

#@crsf_exempt
def dayaheadtotalloadforecast_list(request):
    dayahead = Dayaheadtotalloadforecast.objects.all()
    data_to_export = []
    for data in dayahead:
        areatypecode = data.areatypecodeid.areatypecodetext
        mapcode = data.mapcodeid.mapcodetext
        resolutioncode = data.resolutioncodeid.resolutioncodetext

        data_to_export.append({
        'source': 'entso-e',
        'dataset': 'DayAheadTotalLoadForecast',
        'areaname': data.areaname,
        'areatypecode': areatypecode,
        'mapcode': mapcode,
        'resolutioncode': resolutioncode,
        'year': data.year,
        'month': data.month,
        'day': data.day,
        'datetime': data.datetime,
        'productiontype': data.totalloadvalue,
        'DayAheadTotalLoadForecastValue': data.actualgenerationoutput,
        'updatetime':data.updatetime
        })
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        return JsonResponse(data_to_export,json_dumps_params={'indent': 2},safe = False)

#@csrf_exempt
def dayaheadtotalloadforecast_detail2(request,areaname,resolutioncode,year,month,day,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    data_to_export = Dayaheadtotalloadforecast.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id,year = year, month = month, day = day)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode =dd.mapcodeid.mapcodetext
        data.append({
        'Source': 'entso-e',
        'Dataset': 'DayAheadTotalLoadForecast',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'DateTimeUTC': dd.datetime,
        'DayAheadTotalLoadForecastValue': dd.totalloadvalue,
        'UpdateTimeUTC':dd.updatetime
        })
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['DateTimeUTC'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','datetime','DayAheadTotalLoadForecastValue','updatetime']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "DayAheadTotalLoadForecast.csv"'
                return response
        else:
            return HttpResponse(status=400)

def dayaheadtotalloadforecast_detail1(request,areaname,resolutioncode,year,month,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    data_to_export = Dayaheadtotalloadforecast.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id,year = year, month = month)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode =dd.mapcodeid.mapcodetext
        sum =  Dayaheadtotalloadforecast.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id,year = year, month = month, day = dd.day,mapcodeid = dd.mapcodeid,areatypecodeid = dd.areatypecodeid).aggregate(Sum('totalloadvalue'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'DayAheadTotalLoadForecast',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'DayAheadTotalLoadForecastByDayValue': sum['totalloadvalue__sum'],
        })
        if temp not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Day'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','DayAheadTotalLoadForecastValue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "Dayaheadtotalloadforecast.csv"'
                return response
        else:
            return HttpResponse(status=400)

def dayaheadtotalloadforecast_detail(request,areaname,resolutioncode,year,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    data_to_export = Dayaheadtotalloadforecast.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id,year = year)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode =dd.mapcodeid.mapcodetext
        sum =  Dayaheadtotalloadforecast.objects.filter(areaname = areaname, resolutioncodeid = tmp[0].id,year = year, month = dd.month,areatypecodeid = dd.areatypecodeid,mapcodeid = dd.mapcodeid).aggregate(Sum('totalloadvalue'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'DayAheadTotalLoadForecast',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'DayAheadTotalLoadForecastByMonthValue': sum['totalloadvalue__sum'],
        })
        if temp not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Month'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','DayAheadTotalLoadForecastValue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "DayAheadTotalLoadForecast.csv"'
                return response
        else:
            return HttpResponse('Bad request')


#Actual Total Load vs Day-Ahead Total Load Forecast

def actualvsforecast_detail2(request,areaname,resolutioncode,year,month,day,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    resolutioncodeid = tmp[0].id
    data_to_export = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=month,day=day)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode = dd.mapcodeid.mapcodetext
        nes = Dayaheadtotalloadforecast.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,mapcodeid = dd.mapcodeid,datetime = dd.datetime,year=year,month=month,day=day)
        print(nes)
        data.append({
        'Source': 'entso-e',
        'Dataset': 'ActualTotalLoad',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'DateTimeUTC': dd.datetime,
        'DayAheadTotalLoadForecastValue': nes[0].totalloadvalue,
        'ActualTotalLoadValue': dd.totalloadvalue,
        })
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['DateTimeUTC'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','datetime','DayAheadTotalLoadForecastValue','actualtotalloadvalue','updatetime']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "ActualVsForecast.csv"'
                return response
        else:
            return HttpResponse('Bad rerquest')

def actualvsforecast_detail1(request,areaname,resolutioncode,year,month,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    resolutioncodeid = tmp[0].id
    data_to_export = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=month)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode = dd.mapcodeid.mapcodetext
        sum = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=month,day =dd.day,mapcodeid = dd.mapcodeid,areatypecodeid = dd.areatypecodeid).aggregate(Sum('totalloadvalue'))
        nes = Dayaheadtotalloadforecast.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,mapcodeid = dd.mapcodeid,year=year,month=month,day=dd.day,areatypecodeid = dd.areatypecodeid).aggregate(Sum('totalloadvalue'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'ActualTotalLoad',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'Day': dd.day,
        'DayAheadTotalLoadForecastByDayValue': nes['totalloadvalue__sum'],
        'ActualTotalLoadByDayValue': sum['totalloadvalue__sum']
        })
        if temp  not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Day'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','day','DayAheadTotalLoadForecastValue','actualtotalloadvalue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "ActualVsForecast.csv"'
                return response
        else:
            return HttpResponse("Bad reqquest")

def actualvsforecast_detail(request,areaname,resolutioncode,year,format):
    tmp = Resolutioncode.objects.filter(resolutioncodetext = resolutioncode)
    resolutioncodeid = tmp[0].id
    data_to_export = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year)
    data = []
    for dd in data_to_export:
        areatypecode = dd.areatypecodeid.areatypecodetext
        mapcode = dd.mapcodeid.mapcodetext
        sum = Actualtotalload.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,year=year,month=dd.month,mapcodeid = dd.mapcodeid,areatypecodeid = dd.areatypecodeid).aggregate(Sum('totalloadvalue'))
        nes = Dayaheadtotalloadforecast.objects.filter(areaname = areaname,resolutioncodeid = resolutioncodeid,mapcodeid = dd.mapcodeid,year=year,month=dd.month,areatypecodeid = dd.areatypecodeid).aggregate(Sum('totalloadvalue'))
        temp = ({
        'Source': 'entso-e',
        'Dataset': 'ActualTotalLoad',
        'AreaName': dd.areaname,
        'AreaTypeCode': areatypecode,
        'MapCode': mapcode,
        'ResolutionCode': resolutioncode,
        'Year': dd.year,
        'Month': dd.month,
        'DayAheadTotalLoadForecastByMonthValue': nes['totalloadvalue__sum'],
        'ActualTotalLoadByMonthValue': sum['totalloadvalue__sum']
        })
        if temp  not in data:
            data.append(temp)
    if data == []:
        return HttpResponse(status=403)
    if request.method == 'POST':
        newdata = sorted(data, key=lambda k: k['Month'])
        if format == 'json':
            return JsonResponse(newdata,json_dumps_params={'indent': 2},safe = False)
        elif format == 'csv':
            csv_file = "Names.csv"
            csv_columns = ['source','dataset','areaname','areatypecode','mapcode','resolutioncode','year','month','DayAheadTotalLoadForecastValue','actualtotalloadvalue']
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for d in newdata:
                    writer.writerow(d)
            with open(csv_file) as csvfile:
                response = HttpResponse(csvfile,content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename = "ActualTotalLoad.csv"'
                return response
        else:
            return HttpResponse(status=400)
