# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 01:35:26 2016

@author: Leo
"""

import pickle
from github import Github
from os import system
import datetime
from unicodedata import normalize
#import json 
#from unicodedata import normalize
#from operator import itemgetter
#import datetime
import time
from operator import itemgetter
import csv
import json 
dicUsers={}
def erroUser(Login):
    listErro=[Login]
    cont=0
    for login in listErro:
        try:
            user=client.get_user(login)
        except Exception:
            print "Erro no user: ", login, ". Repetindo a busca!"
            cont+=1
            listErro.append(login)
        if cont==10:
            return -1
    return user
    
def erroContributors(Repo):
    listErro=[Repo]
    cont=0
    for repo in listErro:
        try:
            contributors=[i for i in repo.get_contributors()]
        except Exception:
            print "Erro ao buscar os contribuidores do repo: ", repo.name, ". Repetindo a busca!"
            cont+=1
            listErro.append(repo)
        if cont==10:
            return -1
    return contributors    
 
def erroRepos(Orga):
    listErro=[Orga]
    cont=0
    for orga in listErro:
        try:
            repos=[s for s in orga.get_repos()]
        except Exception:
            print "Erro ao buscar os repositorios da organização:", orga.name, ". Repetindo a busca!"
            cont+=1
            listErro.append(orga)
        if cont==10:
            return -1
    return repos
    
def erroEvents(user):
    listErro=[user]
    cont=0
    for u in listErro:
        try:
            events=[i for i in u.get_public_events()]
        except Exception:
            print "Erro ao buscar os eventos do user:", u.login, ". Repetindo a busca!"
            cont+=1
            listErro.append(u)
        if cont>=10:
            return -1
    return events    
    

def printUsers():
    print "Total de users: ", len(dicUsers.keys())
    print 
    for user in dicUsers.keys():
        print "Login: ", user, ", Nome: ",dicUsers[user]["name"],", Email: ", dicUsers[user]["email"], ", Followers: ", dicUsers[user]["followers"], ", Following: ", dicUsers[user]["following"], ", Organization: ", dicUsers[user]["organization"], ", Contribuitions: ",dicUsers[user]["contribuitions"]

def expReposCsv(listSorted):
    Fieldnames=["login", "name", "email","location","followers", "following", "organization", "contribuitions", "totalContribuitions","lastEvent"]
    firstLine={"login":"Login","name":"Name", "email":"Email", "location":"Location","followers":"Followers", "following":"Following", "organization":"Organization", "contribuitions":"Contribuitions", "totalContribuitions": "Total_Contribuitions", "lastEvent":"Last Events(for 3 months) "}
    fileResul=open("Resul.csv","wb")
    csvWriter=csv.DictWriter(fileResul,delimiter=';',fieldnames=Fieldnames)
    csvWriter.writerow(firstLine)
    for user in listSorted:
        if dicUsers[user[0]]["email"] != None:
            row={"login":user[0], "name":unicode(dicUsers[user[0]]["name"]).encode("utf8"),"email":dicUsers[user[0]]["email"], "location": unicode(dicUsers[user[0]]["location"]).encode("utf-8"), "followers":dicUsers[user[0]]["followers"], "following":dicUsers[user[0]]["following"], "organization":dicUsers[user[0]]["organization"], "contribuitions":dicUsers[user[0]]["contribuitions"], "totalContribuitions":user[1], "lastEvent":dicUsers[user[0]]["lastEvent"]}
        else:
            row={"login":user[0], "name":unicode(dicUsers[user[0]]["name"]).encode("utf8"),"email":"None", "location": unicode(dicUsers[user[0]]["location"]).encode("utf-8"),"followers":dicUsers[user[0]]["followers"], "following":dicUsers[user[0]]["following"], "organization":dicUsers[user[0]]["organization"], "contribuitions":dicUsers[user[0]]["contribuitions"], "totalContribuitions":user[1], "lastEvent":dicUsers[user[0]]["lastEvent"]}
        csvWriter.writerow(row)
        #w.writerow({k:v.encode('utf8') for k,v in row.items()})
    fileResul.close()
    

def isStateBrazil(location):
    cont=0
    for j in states:
        if (" "+j["NAME"]+" " in location) or (" "+j["ABBREVIATION"]+" " in location) or (" "+j["CAPITAL"]+" " in location):
            cont=1
            break
    if cont==0:
        return False
    else:
        return True

def isBrazil(location):
        aux=location
        aux=normalize('NFKD', aux).encode('ASCII','ignore')
        aux=aux.upper()
        aux=aux.replace(")"," ")
        aux=aux.replace("("," ")
        aux=aux.replace(","," ")
        aux=aux.replace(".","")
        aux=aux.replace("-"," ")
        aux=aux.replace("|"," ")
        aux=aux.replace("/"," ")
        aux=aux.replace("\\"," ")
        aux=aux.replace(">"," ")
        aux=aux.replace("<"," ")
        aux=aux.replace("?"," ")
        aux=" "+aux+" "
        aux=aux.replace(" BRASIL "," BRAZIL ")
        aux=aux.replace("    "," ")
        aux=aux.replace("   "," ")
        aux=aux.replace("  "," ")
        if aux == " BRAZIL ":
            return True
        else:
            return isStateBrazil(aux)



ACCESS_TOKEN = '8d0cd2b4a8ef40967412d0895d116cf9d6f53aee'
client = Github(ACCESS_TOKEN, per_page=100)
#print client.get_rate_limit().raw_data["resources"]["core"]["remaining"]
system("cls")# -*- coding: utf-8 -*-

ListOrganization=["okfn-brasil","dadosgovbr","LabPi"]


"""
dicUsers={login:{
                 name: string
                 email:string
                 Followers:int
                 Following:int
                 organizations:[]
                 repos:[]
                 events:[(event, nameRepo)]//ainda fazendo!
                 contributions:[(NameRepo, int)]
                }
                }
"""

cont=5000#verifica o limite de acesso
listErro=[]
listUserAux=[]
c=0
listOrgs=[]
for nameOrga in ListOrganization:
    orga=client.get_organization(nameOrga)
    cont-=1
    try:
        repos=[s for s in orga.get_repos()]
    except Exception:
            print "Erro ao buscar os repositorios da organização: ", nameOrga, ". Repetindo a busca!"
            repos=erroRepos(orga)
    if repos==-1:
        continue        
    
    print "Total de repos na ",nameOrga, " é: ", len(repos)
    for repo in repos:
        cont-=1
        print repo.full_name
        try:
            contributors=[i for i in repo.get_contributors()]
        except Exception:
            print "Erro ao buscar os contribuidores do repo: ", repo.name, "repetindo a busca!"
            contributors=erroContributors(repo)    
        if contributors==-1:
            continue
        listOrgsTemp=[]
        for contributor in contributors:
            cont-=1
            try:
                user=client.get_user(contributor.login)
            except Exception, e:
                print "Erro no user: ", contributor.login, "repetindo a busca!"
                user=erroUser(contributor.login)
            if user==-1:
                continue
        
            if dicUsers.has_key(user.login):
                if not(nameOrga in dicUsers[user.login]["organization"]):
                    dicUsers[user.login]["organization"].append(nameOrga)
                dicUsers[user.login]["repos"].append(repo.full_name)
                #"events":[()]
                dicUsers[user.login]["contribuitions"].append((str(repo.full_name), contributor.contributions))
                dicUsers[user.login]["totalContribuitions"]+=contributor.contributions
            else:
                dicUsers.update({user.login:{"name":user.name,
                                             "location":user.location,
                                             "email":user.email,
                                             "followers":user.followers,
                                             "following":user.following,
                                             "organization":[nameOrga],
                                             "repos":[repo.full_name],
                                             #"events":[()]
                                             "contribuitions":[(str(repo.full_name), contributor.contributions)],  
                                             "totalContribuitions":contributor.contributions,
                                             "lastEvent":""
                
                }})
                
            if (user.login in listUserAux)==False:
                listUserAux.append(user.login)
                try:
                    events=[i for i in user.get_public_events()]
                except Exception, e:
                    print "Erro nos eventos do user: ", contributor.login, "repetindo a busca!"
                    events=erroEvents(user)
                if events==-1:
                    continue
                
                for event in events:
                    #if event.created_at.date()>datetime.date(2015,4,26):
                        if event.org!=None:
                            #if (event.org.login in listOrgsTemp)==False:
                            #    listOrgsTemp.append(event.org.login)
                            if event.org.login in ListOrganization:
                                dicUsers[user.login]["lastEvent"]+="(Date= "+str(event.created_at.date())+"; type= "+event.type+"; repo= "+event.repo.name+") ; "
                    #else:
                    #    break
        #listOrgs.extend(listOrgsTemp)
        if cont<=100:
            aux=int(client.get_rate_limit().raw_data["resources"]["core"]["remaining"])-int(time.time())
            if aux>0:
                print "Waiting ", aux," s."  
                time.sleep(aux+1)
                cont=5000


print "Total de contribuídores: ", len(dicUsers.keys())
#Verificar usuários com o email cadastrado
dicUsersValid={}
for user in dicUsers.keys():
    if dicUsers[user]["email"]!=None:
        dicUsersValid.update({user:dicUsers[user]})

print "Total de usuários com email: ", len(dicUsersValid.keys())
#Verificar usuários do Brasil 
try:
    arq = file('states.json')
    states=json.load(arq)
    arq.close() 
except IOError:
    print "Saindo..."
    system.exit(0)
            
dicUsersValidFinal={}
for user in dicUsersValid.keys():
    if dicUsersValid[user]["location"]!=None and isBrazil(dicUsersValid[user]["location"]):
        dicUsersValidFinal.update({user:dicUsersValid[user]})

print "Total de usuários localizados no Brasil: ", len(dicUsersValidFinal.keys())
#Salva em .csv              
listSorted=[]
for user in dicUsersValidFinal.keys():
    listSorted.append((user,dicUsersValidFinal[user]["totalContribuitions"]))

listSorted=sorted(listSorted, key=itemgetter(1), reverse=True)
dicUsers= dicUsersValidFinal
expReposCsv(listSorted)
