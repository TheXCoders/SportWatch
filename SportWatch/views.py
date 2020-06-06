import json
import locale
import time
from datetime import date, datetime, timedelta

import mysql.connector
import requests
from django.http import HttpResponse
from django.shortcuts import render

locale.setlocale(locale.LC_TIME,'')

filePwd = open('/home/ubuntu/connection.conf', "r")
dataPwd = filePwd.readlines()

headers = {
    'x-rapidapi-host': "sportwatch-soccer.p.rapidapi.com",
    'x-rapidapi-key': dataPwd[2]
}

dictNameLeague = {"cl": "Ligue Des Champions", "fl1": "Ligue 1", "pe1": "La Liga", "pl": "Premier League", 
                "sai": "Série A", "bund1": "Bundesligua 1", "ppl": "Liga NOS", "ered": "Eredivisie"}

#Début de la définition des pages d'accueils
def index(request):
    return render(request, "indexCalendrier.html")

def indexCalendrier(request):
    return render(request, "indexCalendrier.html")

def indexLive(request):
    return render(request, "indexLive.html")

def indexResults(request):
    return render(request, "indexResultats.html")

def indexMaintenance(request):
    return render(request, "indexMaintenance.html")
#Fin

def calendrierMatches(request, comp):
    rqAPI = requests.get("https://sportwatch-soccer.p.rapidapi.com/getCalendar/{}".format(comp),
                         headers=headers)

    data = rqAPI.json()['Results']

    dataMatchs = list()
    for m in data:
        homeTeam    = m['homeTeam']
        awayTeam    = m['awayTeam']
        urlLogoHome = m['urlLogoHome']
        urlLogoAway = m['urlLogoAway']
        matchTime   = datetime.strptime(m['matchTime'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
        matchDay    = m['matchDay']

        dataMatchs.append((homeTeam, awayTeam, urlLogoHome, urlLogoAway, matchTime, matchDay))

    title = dictNameLeague[comp]    

    if (len(dataMatchs) == 0):
        return render(request, "noMatchesCalendar.html")
    else:
        return render(request, "matchs.html", locals())

def resultsMatches(request, comp):
    rqAPI = requests.get("https://sportwatch-soccer.p.rapidapi.com/getResults/{}".format(comp),
                         headers=headers)

    data = rqAPI.json()['Results']

    dataMatchs = list()
    for m in data:
        homeTeam    = m['homeTeam']
        awayTeam    = m['awayTeam']
        matchTime   = datetime.strptime(m['matchTime'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
        urlLogoHome = m['urlLogoHome']
        urlLogoAway = m['urlLogoAway']
        scoreHome   = m['scoreHome']
        scoreAway   = m['scoreAway']
        matchId = m['matchId']

        dataMatchs.append((homeTeam, awayTeam, urlLogoHome, urlLogoAway, scoreHome, scoreAway, matchTime, matchId))

    title = dictNameLeague[comp]

    return render(request, "matchesResults.html", locals())

def getInfosLive(comp):
    #? This function is useful to not duplicate code in live function

    rq = requests.get("https://sportwatch-soccer.p.rapidapi.com/getLiveByComp/{}".format(comp), headers=headers)
    data = rq.json()['Results']

    dataArray = list()
    for m in data:
        homeTeam    = m['homeTeam']
        awayTeam    = m['awayTeam']
        urlLogoHome = m['urlLogoHome']
        urlLogoAway = m['urlLogoAway']
        scoreHome   = m['scoreHome']
        scoreAway   = m['scoreAway']
        timeMatch   = m['matchTime']
        matchId     = m['matchId']

        dataArray.append((homeTeam, awayTeam, urlLogoHome, urlLogoAway, scoreHome, scoreAway, timeMatch, comp, matchId))
        
    return dataArray

def live(request, comp):

    if comp == 'all':
        dataMatchs = list()
        for cp in dictNameLeague.keys():
            dataMatchs += getInfosLive(cp)
    else:        
        dataMatchs = list()
        dataMatchs += getInfosLive(comp)
    
    if len(dataMatchs) == 0:
        return render(request, "noMatchesLive.html")    
    else:
        return render(request, "matchesLive.html", locals())

def matchStats(request, methode, comp, matchId):
    rqAPI = requests.get("https://sportwatch-soccer.p.rapidapi.com/getLiveStats/{}/{}".format(comp, matchId), headers=headers)

    data = rqAPI.json()['Results']
    dataMatchs = list()

    if data != []:
        homeTeam       = data[0]['homeTeam']      
        awayTeam       = data[0]['awayTeam']      
        urlLogoHome    = data[0]['urlLogoHome']   
        urlLogoAway    = data[0]['urlLogoAway']   
        scoreHome      = data[0]['scoreHome']     
        scoreAway      = data[0]['scoreAway']     
        matchTime      = data[0]['matchTime']     
        possessionHome = data[0]['possessionHome']
        possessionAway = data[0]['possessionAway']
        listGoalHome   = data[0]['listGoalHome']  
        listGoalAway   = data[0]['listGoalAway']  

        if possessionHome != None:                
            possessionArray = [possessionHome, possessionAway]
        else:
            possessionArray = list()

        labelArray = [homeTeam, awayTeam]

        dataMatchs.append((homeTeam, awayTeam, urlLogoHome, urlLogoAway, scoreHome, scoreAway, 
                            matchTime, possessionHome, possessionAway, listGoalHome, listGoalAway))
        
        if methode == "live":
            return render(request, "matchesLive-Stats.html", locals())
        elif methode == "results":
            return render(request, "matchesResults-Stats.html", locals())
        else:
            return render(request, "noMatchesLive.html")
    else:
        return render(request, "noMatchesLive.html")