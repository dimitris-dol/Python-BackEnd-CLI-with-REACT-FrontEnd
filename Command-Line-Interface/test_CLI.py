import pytest
import sys
import CLI
import os

def test_u_createkey(monkeypatch):
    CLI.createkey("key")
    file = open("softeng19bAPI.token","r")
    assert file.read() == "key"
    file.close()

def test_u_getkey(monkeypatch):
    file = open("softeng19bAPI.token","w")
    file.write('key')
    file.close()
    assert CLI.getkey() == 'key'
    os.remove("./softeng19bAPI.token")
    assert CLI.getkey() == ''

def test_u_is_date(monkeypatch):
    assert CLI.is_date('2018-02-29') is None
    assert CLI.is_date('2018-01-29') is '2018-01-29'
    assert CLI.is_date('-2018-01') is None
    assert CLI.is_date('2018-a0') is None
    assert CLI.is_date('error') is None
    assert CLI.is_date('2020-02-29') is '2020-02-29'
    assert CLI.is_date('2018') is None
    assert CLI.is_date('2018-22') is None
    assert CLI.is_date('2018-00') is None
    assert CLI.is_date('2018-02') is None

def test_u_month_type(monkeypatch):
    assert CLI.month_type('2018-02-29') is None
    assert CLI.month_type('2018-01-29') is None
    assert CLI.month_type('error') is None
    assert CLI.month_type('-2018-01') is None
    assert CLI.month_type('2020-02-29') is None
    assert CLI.month_type('2018') is None
    assert CLI.month_type('2018-22') is None
    assert CLI.month_type('2018-00') is None
    assert CLI.month_type('2018-a0') is None
    assert CLI.month_type('2018-02') is '2018-02'

def test_u_year_type(monkeypatch):
    assert CLI.year_type('2018-02-29') is None
    assert CLI.year_type('2018-01-29') is None
    assert CLI.year_type('2018-a0') is None
    assert CLI.year_type('-2018-01') is None
    assert CLI.year_type('2020-02-29') is None
    assert CLI.year_type('2018') is '2018'
    assert CLI.year_type('2018-22') is None
    assert CLI.year_type('error') is None
    assert CLI.year_type('2018-00') is None
    assert CLI.year_type('2018-02') is None
    assert CLI.year_type('-2018') is None

def test_u_csv_file(monkeypatch):
    assert CLI.csv_file('file') == None
    assert CLI.csv_file('file.csv') == 'file.csv'
    assert CLI.csv_file('file.csv.csv') == 'file.csv.csv'
    assert CLI.csv_file('file.json') is None
    assert CLI.csv_file('file.csv.json') is None
    assert CLI.csv_file('file.csvkgf') is None

def test_u_pssw_type(monkeypatch):
    assert CLI.psw('sdfl;dfkglkjdfvl;sdzdfr') == 'sdfl;dfkglkjdfvl;sdzdfr'
    assert CLI.psw('sdfl;dfkgASl%^278kjdfvl;sdzdfr') == 'sdfl;dfkgASl%^278kjdfvl;sdzdfr'
    assert CLI.psw('sdfl;dfkgASl%^278kjdfvl;sslkdmflkmvs;lasdxae324546HDGO@$Tgxdfdzdfr') == None


def test_f_ActualTotalLoad(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Greece','--timeres','PT60M','--year','2018','--format','csv'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--timeres','PT15M','--area','Greece','--year','-2018'])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','','--timeres','PT60M','--year','2018'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Greece','--format','csv','--year','asdf','--timeres','PT60M'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Italy','--timeres','PT60M','--year','2018-95'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Belgium','--timeres','PT30M','--month','2018-95'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Spain','--timeres','PT30M','--month','2018-02'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Greece','--timeres','PT15M','--month','2018-02-01'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Greece','--timeres','PT60M','--date','2018-02-30'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualTotalLoad','--area','Russia','--format','csv','--timeres','PT60M','--date','2018-01-29'])
        assert CLI.main() == 1

def test_f_HealthCheck(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','HealthCheck'])
        assert CLI.main() == 1
'''
def test_f_Reset(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Reset'])
        assert CLI.main() == 1
'''

def test_f_Login(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Login','--username','dimitris','--passw','8717'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Login','--username','dimitris','--passw','8817'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Login','--username','dmitris','--passw','8717'])
        assert CLI.main() == 1

def test_f_Logout(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newuser','--username','dimitris','--passw','8717','--email','some@gmail.com','--quota','100'])
        CLI.main()
        m.setattr(sys, 'argv', ['CLI','Login','--username','dimitris','--passw','8717'])
        CLI.main()
        m.setattr(sys, 'argv', ['CLI','Logout'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Logout'])
        assert CLI.main() == 2

def test_f_AggregatedGenerationPerType(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--area','Greece','--productiontype','Nuclear','--year','2018','--timeres','PT60M'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--productiontype','nuclear','--area','Greece','--timeres','PT15M','--year','-2018'])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--area','','--timeres','PT60M','--year','2018','--productiontype','Nuclear'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--area','Greece','--productiontype','nuclear','--format','csv','--timeres','PT60M','--year','asdf'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--timeres','PT60M','--year','2018-95','--productiontype','nuclear','--area','Italy'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--timeres','PT30M','--format','csv','--area','Belgium','--month','2018-95','--productiontype','nuclear'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--timeres','PT30M','--month','2018-02','--area','Spain','--productiontype','Fossil Oil''--format','csv',])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--area','Greece','--timeres','PT15M','--productiontype','Fossil Oil','--month','2018-02-01'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--area','Greece','--timeres','PT60M','--date','2018-02-30','--productiontype','Air'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','AggregatedGenerationPerType','--area','Russia','--productiontype','Fossil oil','--timeres','PT60M','--date','2018-01-29'])
        assert CLI.main() == 1

def test_f_DayAheadTotalLoadForecast(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Greece','--timeres','PT60M','--year','2018','--format','csv'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--timeres','PT15M','--area','Greece','--year','-2018'])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','','--timeres','PT60M','--year','2018'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Greece','--year','asdf','--timeres','PT60M'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Italy','--timeres','PT60M','--format','csv','--year','2018-95'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Belgium','--timeres','PT30M','--month','2018-95'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Spain','--timeres','PT30M','--month','2018-02'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Greece','--timeres','PT15M','--month','2018-02-01'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--format','csv','--area','Greece','--timeres','PT60M','--date','2018-02-30'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','DayAheadTotalLoadForecast','--area','Russia','--timeres','PT60M','--date','2018-01-29'])
        assert CLI.main() == 1

def test_f_ActualvsForecast(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Greece','--timeres','PT60M','--year','2018'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--timeres','PT15M','--area','Greece','--year','-2018','--format','csv'])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','','--timeres','PT60M','--year','2018'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Greece','--year','asdf','--timeres','PT60M'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Italy','--timeres','PT60M','--year','2018-95'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Belgium','--timeres','PT30M','--format','csv','--month','2018-95'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Spain','--timeres','PT30M','--month','2018-02'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Greece','--timeres','PT15M','--month','2018-02-01'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Greece','--format','csv','--timeres','PT60M','--date','2018-02-30'])
        assert CLI.main() == "Invalid parameter"
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','ActualvsForecast','--area','Russia','--timeres','PT60M','--date','2018-01-29'])
        assert CLI.main() == 1

def test_f_newuser(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newuser','--username','dimitris','--passw','8717','--email','some@gmail.com','--quota','100'])
        assert CLI.main() ==1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newuser','--username','dimitris','--passw','8717','--email','some@gmail.com','--quota','100'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newuser','--username','ttest','--passw','8717','--email','','--quota','100'])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newuser','--username','','--passw','8717','--email','some@gmail.com','--quota','100'])
        assert CLI.main() == 'Invalid parameter'

def test_f_moduser(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--moduser','--username','dimitris','--passw','8717','--email','some@gmail.com','--quota','100'])
        assert CLI.main() ==1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--moduser','--username','dimitris','--passw','8717','--email','some@gmail.com','--quota','100'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--moduser','--username','ttest','--passw','8717','--email','','--quota','100'])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--moduser','--username','','--passw','8717','--email','some@gmail.com','--quota','100'])
        assert CLI.main() == 'Invalid parameter'

def test_f_userstatus(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--userstatus','--username','dimitris'])
        assert CLI.main() ==1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--userstatus','--username',''])
        assert CLI.main() == 'Invalid parameter'
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--userstatus','--username','doesnotexist'])
        assert CLI.main() == 1

def test_f_newdata(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newdata','ActualTotalLoad','--source','saom.csv'])
        assert CLI.main() == 1
    with monkeypatch.context() as m:
        m.setattr(sys, 'argv', ['CLI','Admin','--newdata','DayAheadTotalLoadForecast','--source','doesnotexist.csv'])
        assert CLI.main() == 2
