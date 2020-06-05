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
        homeTeam = m['homeTeam']
        awayTeam = m['awayTeam']
        urlLogoHome = m['urlLogoHome']
        urlLogoAway = m['urlLogoAway']
        matchTime = datetime.strptime(m['matchTime'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
        matchDay = m['matchDay']

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
        homeTeam = m['homeTeam']
        awayTeam = m['awayTeam']
        matchTime = datetime.strptime(m['matchTime'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
        urlLogoHome = m['urlLogoHome']
        urlLogoAway = m['urlLogoAway']
        scoreHome = m['scoreHome']
        scoreAway = m['scoreAway']

        dataMatchs.append((homeTeam, awayTeam, urlLogoHome, urlLogoAway, scoreHome, scoreAway, matchTime))

    title = dictNameLeague[comp]

    return render(request, "matchesResults.html", locals())

def getInfosLive(comp):
    #? This function is useful to not duplicate code in live function

    rq = requests.get("https://sportwatch-soccer.p.rapidapi.com/getLiveByComp/{}".format(comp), headers=headers)
    data = rq.json()['Results']

    dataArray = list()
    for m in data:
        homeTeam =    m['homeTeam']
        awayTeam =    m['awayTeam']
        urlLogoHome = m['urlLogoHome']
        urlLogoAway = m['urlLogoAway']
        scoreHome = m['scoreHome']
        scoreAway = m['scoreAway']
        timeMatch = m['matchTime']

        dataArray.append((homeTeam, awayTeam, urlLogoHome, urlLogoAway, scoreHome, scoreAway, timeMatch))
        
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
