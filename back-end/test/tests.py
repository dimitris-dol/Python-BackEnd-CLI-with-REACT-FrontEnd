from django.test import TestCase
from api.models import *
from django.test import Client
from django.utils import timezone
from api.urls import *
from django.urls import *

class LoginTestCase(TestCase):

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        User.objects.create(loginname='teo',password='10',email='alfa@gmail.com',dateOfkey=timezone.now())
        User.objects.create(loginname='theo',password='100',email='olfa@gmail.com',dateOfkey=timezone.now())
        Resolutioncode.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),resolutioncodetext='PT60M')
        Resolutioncode.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),resolutioncodetext='PT30M')
        Productiontype.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),productiontypetext='Fossil Gas')
        Productiontype.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),productiontypetext='Waste')
        Mapcode.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),mapcodetext='BE')
        Mapcode.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),mapcodetext='Gr')
        Areatypecode.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),areatypecodetext='CTA')
        Areatypecode.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),areatypecodetext='BZN')
        Allocatedeicdetail.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),mrid='10T-1001-10010AS',docstatusvalue='A05',attributeinstancecomponent='International',longnames='Tie Line Koman-KosovoB',displaynames='L_KOM-KOSB',lastrequestdateandortime=timezone.now(),deactivaterequestdateandortime=timezone.now(),isdeleted=0,)
        Actualtotalload.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=1,day=4,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),totalloadvalue=567.56,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'))
        Actualtotalload.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=1,day=5,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),totalloadvalue=567.56,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'))
        Actualtotalload.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=2,day=4,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),totalloadvalue=567.56,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'))
        Aggregatedgenerationpertype.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=1,day=4,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),actualgenerationoutput=567.56,actualconsuption=15,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'),productiontypeid=Productiontype.objects.get(productiontypetext='Waste'))
        Aggregatedgenerationpertype.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=2,day=4,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),actualgenerationoutput=567.56,actualconsuption=15,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'),productiontypeid=Productiontype.objects.get(productiontypetext='Waste'))
        Aggregatedgenerationpertype.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=2,day=5,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),actualgenerationoutput=567.56,actualconsuption=15,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'),productiontypeid=Productiontype.objects.get(productiontypetext='Waste'))
        Dayaheadtotalloadforecast.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=1,day=4,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),totalloadvalue=567.56,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'))
        Dayaheadtotalloadforecast.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=2,day=4,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),totalloadvalue=567.56,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'))
        Dayaheadtotalloadforecast.objects.create(entitycreatedat=timezone.now(),entitymodifiedat=timezone.now(),actiontaskid=312126,year=2018,month=2,day=5,datetime=timezone.now(),areaname='Greece',updatetime=timezone.now(),totalloadvalue=567.56,areatypecodeid=Areatypecode.objects.get(areatypecodetext='BZN'),areacodeid=Allocatedeicdetail.objects.get(docstatusvalue='A05'),resolutioncodeid=Resolutioncode.objects.get(resolutioncodetext='PT60M'),mapcodeid=Mapcode.objects.get(mapcodetext='GR'))

#ActualTotalLoad tests
    def test_sum_year_actualltotalload(self):
        print("ActualTotalLoad year sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/ActualTotalLoad/Greece/PT60M/year/2018',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_sum_month_actualltotalload(self):
        print("ActualTotalLoad month sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/ActualTotalLoad/Greece/PT60M/year/2018-01',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_full_date_actualltotalload(self):
        print("ActualTotalLoad full date")
        user = User.objects.all()
        response = self.client.get('/energy/api/ActualTotalLoad/Greece/PT60M/year/2018-01-04',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)
#end of ActualTotalLoad tests

#AggreatedGenerationPerType tests
    def test_year_sum_aggregatedgenerationpertype(self):
        print("AggreatedGenerationPerType year sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/AggreatedGenerationPerType/Greece/PT60M/year/2018',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_year_sum_aggregatedgenerationpertype(self):
        print("AggreatedGenerationPerType year sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/AggreatedGenerationPerType/Greece/PT60M/year/2018',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_full_date_aggregatedgenerationpertype(self):
        print("AggreatedGenerationPerType month sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/AggreatedGenerationPerType/Greece/PT60M/year/2018-01-04',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)
#end of AggreatedGenerationPerType tests

#test for DayAheadTotalLoadForecast
    def test_year_sum_dayaheadtotalloadforecast(self):
        print("DayAheadTotalLoadForecast year sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/DayAheadTotalLoadForecast/Greece/PT60M/year/2018',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_month_sum_dayaheadtotalloadforecast(self):
        print("DayAheadTotalLoadForecast month sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/DayAheadTotalLoadForecast/Greece/PT60M/year/2018-01',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_full_date_dayaheadtotalloadforecast(self):
        print("DayAheadTotalLoadForecast full date")
        user = User.objects.all()
        response = self.client.get('/energy/api/DayAheadTotalLoadForecast/Greece/PT60M/year/2018-01-04',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)
#end of DayAheadTotalLoadForecast tests

#test for ActualvsForecast
    def test_year_sum_actualvsforecast(self):
        print("ActualvsForecast year sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/ActualvsForecast/Greece/PT60M/year/2018',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_month_sum_actualvsforecast(self):
        print("ActualvsForecast month sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/ActualvsForecast/Greece/PT60M/year/2018-01',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

    def test_full_year_actualvsforecast(self):
        print("ActualvsForecast year sum")
        user = User.objects.all()
        response = self.client.get('/energy/api/ActualvsForecast/Greece/PT60M/year/2018-01-04',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response['actualtotalloadvalue'],1702.68)

#end of ActualvsForecast tests

#succesfull login
    def test_login(self):
        print("Succesfull Login")
        user = User.objects.all()
        response = self.client.post('/urlencoded', data = {'username': 'teo', 'password': '10'})
        print (response)
        self.assertEqual(response.status_code,200)

#unsuccessfull login
def test_login(self):
    print("Unsuccesfull login")
    user = User.objects.all()
    response = self.client.post('/urlencoded', data = {'username': 'teo', 'password': '1980'})
    print (response)
    self.assertEqual(response.status_code,400)


#logout
    def test_logout(self):
        print("Logout")
        response = self.client.post('/energy/api/Logout')
        print(response)
        self.assertEqual(response.status_code,200)

#Healthcheck
    def test_healthCheck(self):
        print("HealthCheck")
        response = self.client.get('/energy/api/HealthCheck')
        print(response)
        self.assertEqual(response.status_code,200)

#out of Quotas
    def test_out_of_quotas(self):
        print("out of quotas")
        user = User.objects.all()
        user[0].counter = user[0].quotas + 1
        response = self.client.get('/energy/api/ActualvsForecast/Greece/PT60M/year/2018-01-04',**{X_OBSERVATORY_AUTH:user[0].api_key})
        print(response)
        self.assertEqual(response.status_code,402)

#reset
    def test_reset(self):
        response = self.client.get('/energy/api/Reset')
        print(rersponse)
        self.assertEqual(response.status_code,200)
# Create your tests here.
