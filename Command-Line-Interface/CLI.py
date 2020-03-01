import requests
from requests.exceptions import ConnectionError
import os
import re
import sys
import argparse
from django.http import HttpResponse
import datetime
import json
import csv

url = 'http://localhost:8765/energy/api/'

def createkey(token):
    file = open("softeng19bAPI.token","w")
    file.write(token)
    file.close()
    return

def http_response(err):
    if err.status_code == 400:
        print('Error 400: Bad Request')
    elif err.status_code == 401:
        print('Error 401: Not Authorized')
    elif err.status_code == 402:
        print('Error 402: Out of quota')
    elif err.status_code == 403:
        print('Error 403: No data')
    elif err.status_code == 404:
        print('Error 404: Page not Found')
    else:
        print(err)
        exit()

def getkey():
    try:
        file = open("softeng19bAPI.token","r")
        token = file.read()
        file.close()
        return token
    except FileNotFoundError:
        return ''

def month_type(month):
    try:
        temp = month.split('-')
        if int(temp[1]) > 0 and int(temp[1]) < 13 and int(temp[0]) > 0:
            try:
                temp[2]
                print('Invalid date')
            except:
                return month
    except:
        print('Invalid date')

def year_type(year):
    try:
        if int(year) > 0:
            return year
    except ValueError:
        print('Invalid date')

def is_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        print('Invalid date')

def csv_file(source):
    if source.find('.csv') > -1 :
        if source.split('.')[-1] == 'csv':
            return source
    print('Invalid file format')

def psw(passw):
    if len(passw) <= 32 and len(passw) > 0:
        return passw
    else:
        print('Invalid sized password')

def main():
    def try_except(result):
        try:
            if result.status_code == 200:
                if args.format == 'json':
                    print(result.json())
                else:
                    print(result.text)
            else:
                http_response(result)
        except json.JSONDecodeError:
            http_response(result)

    def date_type():
        if args.date:
            return (args.date,"date")
        elif args.month:
            return (args.month,'month')
        elif args.year:
            return (args.year,'year')
        else:
            print('None of --date/--month/--year attributes was found')

    command_line = argparse.ArgumentParser()

    command_line.add_argument('SCOPE', choices = ['HealthCheck','Reset','Login','Logout','ActualTotalLoad',
                                            'AggregatedGenerationPerType','DayAheadTotalLoadForecast',
                                            'ActualvsForecast','Admin'])

    command_line.add_argument('--username', default = '')
    command_line.add_argument('--passw', type = psw, default = '')
    command_line.add_argument('--area')
    command_line.add_argument('--timeres', choices = ['PT15M','PT30M','PT60M'])
    command_line.add_argument('--date', type = is_date)
    command_line.add_argument('--month', type = month_type)
    command_line.add_argument('--year', type = year_type)
    command_line.add_argument('--productiontype', nargs = '+')
    command_line.add_argument('--format', choices = ['json','csv'], default = 'json')
    command_line.add_argument('--apikey')
    command_line.add_argument('--newuser', action ='store_true')
    command_line.add_argument('--email')
    command_line.add_argument('--quota', type = int)
    command_line.add_argument('--userstatus', action ='store_true')
    command_line.add_argument('--moduser', action ='store_true')
    command_line.add_argument('--newdata', choices = ['ActualTotalLoad','AggregatedGenerationPerType','DayAheadTotalLoadForecast'])
    command_line.add_argument('--source', type = csv_file)

    args = command_line.parse_args()

    #Yes
    if args.SCOPE == 'ActualTotalLoad' :
        api_key = getkey()
        if not args.area or args.area == None:
            print("No area parameter was found")
            return "Invalid parameter"
        if not args.timeres:
            print("No time resolution parameter was found")
            return "Invalid parameter"
        if date_type() is None:
            return "Invalid parameter"
        (dmy,type) = date_type()
        if args.apikey:
            api_key = args.apikey
        try:
            url_format = url + 'ActualTotalLoad/' + args.area + '/' + args.timeres + '/' + type + '/' + dmy + '&format=' + args.format
            result = requests.post(url_format, headers = {'header' : api_key})
            try_except(result)
            return 1
        except ConnectionError as Err:
            print('An error occured \n',Err)

    #Yes
    if args.SCOPE == 'HealthCheck' :
        try:
            url_format = url + 'HealthCheck'
            result = requests.get(url_format)
            try:
                print(result.json())
                return 1
            except json.JSONDecodeError:
                http_response(result)
        except ConnectionError as Err:
            print('reached \n',Err)

    #Yes
    if args.SCOPE == 'Reset' :
        try:
            url_format = url + 'Reset'
            result = requests.post(url_format, data = {'username' : 'admin' , 'password' : '321nimda'})
            try:
                print(result.json())
            except json.JSONDecodeError:
                http_response(result)
            return 1
        except ConnectionError as Err:
            print('An error occured \n',Err)

    #Yes
    if args.SCOPE == 'Login':
        try:
            if not args.username:
                print('Please enter your username')
                exit()
            if not args.passw:
                print('Please enter passw')
                exit()
            url_format = 'http://localhost:8765/urlencoded'
            result = requests.post(url_format, data = {'username' : args.username , 'password' : args.passw})
            if result.status_code == 200:
                createkey(result.json()['token'])
            else:
                http_response(result)
            return 1
        except ConnectionError as Err:
            print('An error occured \n',Err)

    #Yes
    if args.SCOPE == 'Logout':
        try:
            api_key = getkey()
            if args.apikey:
                api_key = args.apikey
            url_format = url + 'Logout'
            result = requests.post(url_format, headers = {'api_key' : api_key})
            if result.status_code == 200:
                try:
                    os.remove("./softeng19bAPI.token")
                    return 1
                except FileNotFoundError:
                    print('An error occured with your validation key \n')
                    return 2
            else:
                http_response(result)
        except ConnectionError as Err:
            print('An error occured \n',Err)

    #Yes
    if args.SCOPE == 'AggregatedGenerationPerType':
        try:
            prod = ' '.join(args.productiontype)
            api_key = getkey()
            if not args.area:
                print("No area parameter was found")
                return "Invalid parameter"
            if not args.timeres:
                print("No time resolution parameter was found")
                return "Invalid parameter"
            if date_type() is None:
                return "Invalid parameter"
            (dmy,type) = date_type()
            if args.apikey:
                api_key = args.apikey
            if not args.productiontype:
                print("No production type parameter was found")
                return "Invalid parameter"
            url_format = url + 'AggregatedGenerationPerType/' + args.area + '/' + prod + '/' + args.timeres + '/' + type + '/' + dmy + '&format=' + args.format
            result = requests.post(url_format, headers = {'header' : api_key})
            try_except(result)
            return 1
        except ConnectionError as Err:
            print('An error occured \n',Err)

    #Yes
    if args.SCOPE == 'DayAheadTotalLoadForecast':
        try:
            api_key = getkey()
            if not args.area:
                print("No area parameter was found")
                return "Invalid parameter"
            if not args.timeres:
                print("No time resolution parameter was found")
                return "Invalid parameter"
            if date_type() is None:
                return "Invalid parameter"
            (dmy,type) = date_type()
            if args.apikey:
                api_key = args.apikey
            url_format = url + 'DayAheadTotalLoadForecast/' + args.area + '/' + args.timeres + '/' +  type + '/' + dmy + '&format=' + args.format
            result = requests.post(url_format, headers = {'header' : api_key})
            try_except(result)
            return 1
        except ConnectionError as Err:
            print('An error occured \n',Err)

    #Yes
    if args.SCOPE == 'ActualvsForecast':
        try:
            api_key = getkey()
            if not args.area:
                print("No area parameter was found")
                return "Invalid parameter"
            if not args.timeres:
                print("No time resolution parameter was found")
                return "Invalid parameter"
            if date_type() is None:
                return "Invalid parameter"
            (dmy,type) = date_type()
            if args.apikey:
                api_key = args.apikey
            url_format = url + 'ActualvsForecast/' + args.area + '/' + args.timeres + '/' +  type + '/' + dmy + '&format=' + args.format
            result = requests.post(url_format, headers = {'header' : api_key})
            try_except(result)
            return 1
        except ConnectionError as Err:
            print('An error occured \n',Err)

    if args.SCOPE == 'Admin':

        if args.newuser:
            try:
                if not args.username or not args.passw or not args.email or not args.quota:
                    print('Not all parameters were given')
                    return "Invalid parameter"
                api_key = getkey()
                if args.apikey:
                    api_key = args.apikey
                url_format = url + 'Admin/' + 'newuser'
                result = requests.post(url_format, data = {'username' : args.username, 'password' : args.passw, 'email' : args.email, 'quotas' : args.quota})
                if result.status_code == 200:
                    if result.json()['token'] != 'already exists':
                        createkey(result.json()['token'])
                    else:
                        print(args.username,'already exists')
                    return 1
                else:
                    http_response(result)
                    return 2
            except ConnectionError as Err:
                print('An error occured \n',Err)
        elif args.moduser:
            try:
                if not args.username or not args.passw or not args.email or not args.quota:
                    print('Not all parameters were given')
                    return "Invalid parameter"
                api_key = getkey()
                if args.apikey:
                    api_key = args.apikey
                url_format = url + 'Admin/' + 'moduser'
                result = requests.post(url_format, data = {'username' : args.username, 'password' : args.passw, 'email' : args.email, 'quotas' : args.quota})
                if result.status_code == 200:
                    print('User modified successfully')
                    return 1
                else:
                    http_response(result)
                    return 2
            except ConnectionError as Err:
                print('An error occured \n',Err)
        elif args.userstatus:
            try:
                if not args.username:
                    print('Not all parameters were given')
                    return "Invalid parameter"
                api_key = getkey()
                if args.apikey:
                    api_key = args.apikey
                url_format = url + 'Admin/' + 'userstatus'
                result = requests.post(url_format, data = {'username' : args.username})
                try_except(result)
                return 1
            except ConnectionError as Err:
                print('An error occured \n',Err)
        elif args.newdata:
            try:
                if not args.source:
                    print('No source provided')
                    return "Invalid parameter"
                url_format = url + 'Admin/' + 'newdata'
                try:
                    source = './' + args.source
                    with open(source, 'rb') as f:
                        result = requests.post(url_format, data = {'filename' : args.source, 'type' : args.newdata}, files = {'file' : f})
                        print(result.text)
                        try_except(result)
                        return 1
                except FileNotFoundError:
                    print('File was not found in the directory')
                    return 2
            except ConnectionError as Err:
                print('An error occured \n',Err)

if __name__ == '__main__':
    main()

def ss(a):
    return a
