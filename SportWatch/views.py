from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from datetime import date, timedelta, datetime
import mysql.connector
import locale
import time

locale.setlocale(locale.LC_TIME,'')

payload = {}
headers = {
  'X-Auth-Token': '3116f894971d478eaa890db823d9c2be'
}

filePwd = open('/home/ubuntu/connection.conf', "r")
dataPwd = filePwd.readlines()

dictNameLeague = {"cl": "Ligue Des Champions", "fl1": "Ligue 1", "pe1": "La Liga", "pl": "Premier League", "sai": "Série A", "bund1": "Bundesligua 1", "ppl": "Liga NOS", "ered": "Eredivisie"}

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
    dbAPI = mysql.connector.connect(
    host="127.0.0.1",
    user=dataPwd[0][0:-1], # [0:-1] for delete the /n char/home/ubuntu/
    passwd=dataPwd[1],
    database="dataAPI",
    auth_plugin='mysql_native_password'
)
    cursor = dbAPI.cursor()
    if comp == 'cl':
        rqSql = "SELECT * FROM matches_{} WHERE matcheStatus=1 ORDER BY date".format(comp)
    else:
        rqSql = "SELECT * FROM matches_{} WHERE matcheStatus=1 ORDER BY matcheDay, date".format(comp)
    cursor.execute(rqSql)
    data = cursor.fetchall()
    dataMatchs = list()
    for m in data:
        homeTeam = m[1]
        awayTeam = m[2]
        if m[3] == None:
            matchTime = 'Date non définie'
        else:
            matchTime = m[3] + timedelta(hours=2)
        idTeam1 = m[4]
        idTeam2 = m[5]
        dataMatchs.append((homeTeam, awayTeam, idTeam1, idTeam2, matchTime))

    title = dictNameLeague[comp]
    dbAPI.close()

    if (len(dataMatchs) == 0):
        return render(request, "noMatchesCalendar.html")
    else:
        return render(request, "matchs.html", locals())

def live(request, comp):
    dbAPI = mysql.connector.connect(
    host="127.0.0.1",
    user=dataPwd[0][0:-1], # [0:-1] for delete the /n char/home/ubuntu/
    passwd=dataPwd[1],
    database="dataAPI",
    auth_plugin='mysql_native_password'
)
    cursor = dbAPI.cursor()

    if comp == 'all':
        dataMatchs = list()
        for cp in dictNameLeague.keys():
            rqSQL = "SELECT * FROM matches_{} WHERE NOT matcheStatus=0 AND NOT matcheStatus=1 AND NOT matcheStatus=7 ORDER BY date".format(cp)
            cursor.execute(rqSQL)
            data = cursor.fetchall()

            for m in data:
                noAffiche = False
                rq = requests.get("https://api.fifa.com/api/v1/live/football/2000000000/0/0/{}".format(m[7]))
                homeTeam = m[1]
                awayTeam = m[2]
                if cp == "cl":
                    scoreHome = m[8]
                    awayScore = m[9]
                else:
                    scoreHome = m[9]
                    awayScore = m[10]
                idTeam1 = m[4]
                idTeam2 = m[5]
                timeMatch = 0
                if m[6] == 3:
                    timeMatch = str(rq.json()['MatchTime'])
                elif m[6] == 12:
                    timeMatch = "Le match va bientôt débuter !"
                else:
                    noAffiche = True

                if timeMatch == 'None':
                    if rq.json()['Period'] == 4:
                        timeMatch = "Mi-Temps !"
                    elif rq.json()['Period'] == 10:
                        timeMatch = "Fin du match !"

                if not noAffiche:
                    dataMatchs.append((homeTeam, awayTeam, idTeam1, idTeam2, scoreHome, awayScore, timeMatch))
    else:        
        rqSQL = "SELECT * FROM matches_{} WHERE NOT matcheStatus=0 AND NOT matcheStatus=1 AND NOT matcheStatus=7 ORDER BY date".format(comp)
        cursor.execute(rqSQL)
        data = cursor.fetchall()
        dataMatchs = list()
        for m in data:
            rq = requests.get("https://api.fifa.com/api/v1/live/football/2000000000/0/0/{}".format(m[7]))
            noAffiche = False
            homeTeam = m[1]
            awayTeam = m[2]
            if comp == "cl":
                scoreHome = m[8]
                awayScore = m[9]
            else:
                scoreHome = m[9]
                awayScore = m[10]
            idTeam1 = m[4]
            idTeam2 = m[5]
            timeMatch = 0
            if m[6] == 3:
                timeMatch = str(rq.json()['MatchTime'])
            elif m[6] == 12:
                timeMatch = "Le match va bientôt débuter !"
            else:
                noAffiche = True

            if timeMatch == 'None':
                if rq.json()['Period'] == 4:
                    timeMatch = "Mi-Temps !"
                elif rq.json()['Period'] == 10:
                    timeMatch = "Fin du matche !"

            if not noAffiche:
                dataMatchs.append((homeTeam, awayTeam, idTeam1, idTeam2, scoreHome, awayScore, timeMatch))

    dbAPI.close()
    
    if len(dataMatchs) == 0:
        return render(request, "noMatchesLive.html")    
    else:
        return render(request, "matchesLive.html", locals())

def resultsMatches(request, comp):
    dbAPI = mysql.connector.connect(
    host="127.0.0.1",
    user=dataPwd[0][0:-1], # [0:-1] for delete the /n char/home/ubuntu/
    passwd=dataPwd[1],
    database="dataAPI",
    auth_plugin='mysql_native_password'
)
    cursor = dbAPI.cursor()

    if comp == 'cl':
        rqSQL = "SELECT * FROM matches_{} WHERE matcheStatus=0 ORDER BY date".format(comp)
    else:
        rqSQL = "SELECT * FROM matches_{} WHERE matcheStatus=0 ORDER BY matcheDay, date".format(comp)
    cursor.execute(rqSQL)
    data = cursor.fetchall()
    dataMatchs = list()

    for m in data:
        homeTeam = m[1]
        awayTeam = m[2]
        matchTime = m[3] + timedelta(hours=1)
        idTeam1 = m[4]
        idTeam2 = m[5]
        if comp == 'cl':
            scoreHome = m[8]
            scoreAway = m[9]
        else:
            scoreHome = m[9]
            scoreAway = m[10]
        dataMatchs.append((homeTeam, awayTeam, idTeam1, idTeam2, scoreHome, scoreAway, matchTime))

    dataMatchs.reverse()
    title = dictNameLeague[comp]
    dbAPI.close()

    return render(request, "matchesResults.html", locals())