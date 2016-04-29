#!/usr/bin/python
# -*- coding: utf-8 -*-
# Version 0.1
import sqlite3, os

# Funktion create:
def create():
    if not os.path.exists("database"):
        os.mkdir("database")
        connection = sqlite3.connect("database/kunden.db")
        cursor = connection.cursor()
        sql = "CREATE TABLE kundenverz("\
              "id INTEGER PRIMARY KEY,"\
              "regdatum TEXT,"\
              "vname TEXT,"\
              "name TEXT,"\
              "adresse TEXT,"\
              "plz TEXT,"\
              "stadt TEXT,"\
              "telefon TEXT)"
        cursor.execute(sql)
        connection.close()
        connection = sqlite3.connect("database/jobs.db")
        cursor = connection.cursor()
        sql = "CREATE TABLE nextjobs(" \
              "id INTEGER,"\
              "beginn TEXT,"\
              "dauer TEXT,"\
              "datum TEXT,"\
              "personen INTEGER,"\
              "kinder INTEGER,"\
              "bahn INTEGER,"\
              "notizen TEXT,"\
              "auftragsid INTEGER PRIMARY KEY)"
        cursor.execute(sql)
        connection.close()

# Funktion Daten einfuegen kunden.db in Tabelle kundenverz
def insertkunden(dbregdatum, dbvname, dbname, dbadresse, dbplz, dbstadt, dbtelefon):
    connection = sqlite3.connect("database/kunden.db")
    cursor = connection.cursor()
    x = 0
    for i in range(1,99999):
        try:
            cursor.execute("""INSERT INTO kundenverz(id, regdatum, vname, name, adresse, plz, stadt, telefon)
                              VALUES(?,?,?,?,?,?,?,?)""", (i, dbregdatum, dbvname, dbname, dbadresse, dbplz, dbstadt, dbtelefon))
            connection.commit()
        except:
            x = x + 1 # nur, damit etwas passiert
        else:
            break
    connection.close()
    result = i
    return result

def double(dbvname, dbname, dbadresse, dbplz, dbstadt, dbtelefon): # Version 0.1
    connection = sqlite3.connect("database/kunden.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM kundenverz WHERE vname=?""", ([dbvname]))
    result = 0
    for dsatz in cursor:
        vglvname = dsatz[2]
        vglname = dsatz[3]
        vgladresse = dsatz[4]
        vglplz = dsatz[5]
        vglstadt = dsatz[6]
        vgltelefon = dsatz[7]
        if vglname == dbname and vgladresse == dbadresse and vglplz == dbplz and vglstadt == dbstadt and vgltelefon == dbtelefon:
            result = 1
            break
    connection.close()
    return result

def personsuchen(dbsuchfeld):
    connection = sqlite3.connect("database/kunden.db")
    cursor = connection.cursor()
    result = 0
    n = 0
    try:
        dbspliteis = dbsuchfeld.split()
        dbvname = dbspliteis[0]
        dbname = dbspliteis[1]
        cursor.execute("""SELECT * FROM kundenverz WHERE name=? COLLATE NOCASE""", ([dbname]))
        for dsatz in cursor:
            vglvname = dsatz[2]
            if vglvname == dbvname:
                n = n + 1
        connection.close()
        dbid = [0] * n
        x = 0
        connection = sqlite3.connect("database/kunden.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM kundenverz WHERE name=? COLLATE NOCASE""", ([dbname]))
        for dsatz in cursor:
            vglvname = dsatz[2]
            if vglvname == dbvname:
                dbid[x] = dsatz[0]
                x = x + 1
        connection.close()
        result = dbid
    except:
        result = ""
    return result

def idtoperson(dbid):
    connection = sqlite3.connect("database/kunden.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM kundenverz WHERE id=?""", ([dbid]))
    for dsatz in cursor:
        dbvname = dsatz[2]
        dbname = dsatz[3]
        dbadresse = dsatz[4]
        dbplz = dsatz[5]
        dbstadt = dsatz[6]
        dbtelefon = dsatz[7]
        result = [dbvname, dbname, dbadresse, dbplz, dbstadt, dbtelefon]
    connection.close()
    return result
# Funktion Daten einfuegen jobs.db in Tabelle nextjobs
def insertjobs(dbid, dbdatum, dbbeginn, dbdauer, dbpersonen, dbkinder, dbbahn, dbnotizen):
    x = 0
    dbbeginn = str(dbbeginn)
    dbdauer = str(dbdauer)
    dbbeginnsplit = dbbeginn.split(":")
    dbdauersplit = dbdauer.split(":")
    dbbeginn = str(dbbeginnsplit[0]) + ":" + str(dbbeginnsplit[1])
    dbdauer = str(dbdauersplit[0]) + ":" + str(dbdauersplit[1])
    connection = sqlite3.connect("database/jobs.db")
    cursor = connection.cursor()
    for i in range(1,999999):
        try:
            cursor.execute("""INSERT INTO nextjobs(id, beginn, dauer, datum, personen, kinder, bahn, notizen, auftragsid)
                              VALUES(?,?,?,?,?,?,?,?,?)""", (dbid, dbbeginn, dbdauer, dbdatum, dbpersonen, dbkinder, dbbahn, dbnotizen, i))
            connection.commit()
        except:
            x = x + 1 # nur, damit etwas passiert
        else:
            break
    connection.close()

def bahnreservierungsstatus(dbdatum, dbbeginn, dbdauer, dbbahn):
    if dbbahn == 0:
        bahnfrei = 0
        maxi = 1
        n = 0
        vglbeginnarray = []
        vgldauerarray = []
        zahlup = 0
        frei = 0
        dbbeginnsplit = dbbeginn.split(":")
        dbdauersplit = dbdauer.split(":")
        dbbeginnstunde = int(dbbeginnsplit[0])
        dbbeginnminute = int(dbbeginnsplit[1])
        dbendestunde = int(dbbeginnsplit[0]) + int(dbdauersplit[0])
        dbendeminute = int(dbbeginnsplit[1]) + int(dbdauersplit[1])
        connection = sqlite3.connect("database/jobs.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM nextjobs WHERE datum=? ORDER BY bahn ASC""", ([dbdatum]))
        for dsatz in cursor:
            n = n + 1
            if dsatz[6] > maxi:
                maxi = dsatz[6]
        connection.close()
        if maxi < 6 and n == 0:
            bahnfrei = 1
        if maxi < 6 and n != 0:
            maxi = maxi + 1
            bahnfrei = maxi
        if maxi == 6 and n != 0:
            for i in range(1,6):
                connection = sqlite3.connect("database/jobs.db")
                cursor = connection.cursor()
                cursor.execute("""SELECT * FROM nextjobs WHERE datum=? ORDER BY bahn ASC""", ([dbdatum]))
                for dsatz in cursor:
                    if dsatz[6] == i:
                        vglbeginnarray.append(dsatz[1])
                        vgldauerarray.append(dsatz[2])
                connection.close()
                for k in range(len(vglbeginnarray)):
                    vgldbeginnxyz = vglbeginnarray[k]
                    vgldbeginnxyz = str(vgldbeginnxyz)
                    vglbeginnsplit = vgldbeginnxyz.split(":")
                    vgldauerxyz = vgldauerarray[k]
                    vgldauerxyz = str(vgldauerxyz)
                    vgldauersplit = vgldauerxyz.split(":")
                    vglbeginnstunde = int(vglbeginnsplit[0])
                    vglbeginnminute = int(vglbeginnsplit[1])
                    vglendestunde = int(vglbeginnsplit[0]) + int(vgldauersplit[0])
                    vglendeminute = int(vglbeginnsplit[1]) + int(vgldauersplit[1])
                    if vglendestunde < dbbeginnstunde or vglendestunde == dbbeginnstunde and vglendeminute <= dbbeginnminute:
                        frei = frei + 1
                    elif vglbeginnstunde > dbendestunde or vglbeginnstunde == dbendestunde and vglbeginnminute >= dbendeminute:
                        frei = frei + 1
                    zahlup = zahlup + 1
                if frei == zahlup:
                    bahnfrei = i
                    break
                else:
                    frei = 0
                    zahlup = 0
                    vglbeginnarray = []
                    vgldauerarray = []
    else:
        vglbeginnarray = []
        vgldauerarray = []
        frei = 0
        zahlup = 0
        n = 0
        dbbeginnsplit = dbbeginn.split(":")
        dbdauersplit = dbdauer.split(":")
        dbbeginnstunde = int(dbbeginnsplit[0])
        dbbeginnminute = int(dbbeginnsplit[1])
        dbendestunde = int(dbbeginnsplit[0]) + int(dbdauersplit[0])
        dbendeminute = int(dbbeginnsplit[1]) + int(dbdauersplit[1])
        connection = sqlite3.connect("database/jobs.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM nextjobs WHERE datum=?""", ([dbdatum]))
        for dsatz in cursor:
            if int(dsatz[6]) == int(dbbahn):
                vglbeginnarray.append(dsatz[1])
                vgldauerarray.append(dsatz[2])
        connection.close()
        for k in range(len(vglbeginnarray)):
            vgldbeginnxyz = vglbeginnarray[k]
            vgldbeginnxyz = str(vgldbeginnxyz)
            vglbeginnsplit = vgldbeginnxyz.split(":")
            vgldauerxyz = vgldauerarray[k]
            vgldauerxyz = str(vgldauerxyz)
            vgldauersplit = vgldauerxyz.split(":")
            vglbeginnstunde = int(vglbeginnsplit[0])
            vglbeginnminute = int(vglbeginnsplit[1])
            vglendestunde = int(vglbeginnsplit[0]) + int(vgldauersplit[0])
            vglendeminute = int(vglbeginnsplit[1]) + int(vgldauersplit[1])
            if vglendestunde < dbbeginnstunde or vglendestunde == dbbeginnstunde and vglendeminute <= dbbeginnminute:
                frei = frei + 1
            elif vglbeginnstunde > dbendestunde or vglbeginnstunde == dbendestunde and vglbeginnminute >= dbendeminute:
                frei = frei + 1
            zahlup =zahlup + 1
        if zahlup == frei:
            bahnfrei = 7
        else:
            bahnfrei = 8
    return bahnfrei

def currentjobs(dbdatum, dbzeit):
    nextjobseid = []
    nextjobsaid = []
    y = 0
    dbzeitsplit = dbzeit.split(":")
    connection = sqlite3.connect("database/jobs.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM nextjobs WHERE datum=?""", ([dbdatum]))
    for dsatz in cursor:
        dbid = dsatz[0]
        vglbeginn = dsatz[1]
        dbaid = dsatz[8]
        vglbeginn = str(vglbeginn)
        vglbeginnsplit = vglbeginn.split(":")
        if vglbeginnsplit[0] >= dbzeitsplit[0]:
            nextjobseid.append(dbid)
            nextjobsaid.append(dbaid)
        y = y + 1
        if y == 11:
            break
    connection.close()
    return nextjobseid, nextjobsaid

def idtopersonlite(dbid):
    result = ""
    connection = sqlite3.connect("database/kunden.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM kundenverz WHERE id=?""", ([dbid]))
    for dsatz in cursor:
        dbvname = dsatz[2]
        dbname = dsatz[3]
        result = [dbvname, dbname]
    connection.close()
    return result

def idtojob(dbaid):
    result = ""
    connection = sqlite3.connect("database/jobs.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM nextjobs WHERE auftragsid=?""", ([dbaid]))
    for dsatz in cursor:
        dbbeginn = dsatz[1]
        dbdauer = dsatz[2]
        dbpersonen = dsatz[4]
        dbkinder = dsatz[5]
        dbbahn = dsatz[6]
        dbnotizen = dsatz[7]
        result = [dbbeginn, dbdauer, dbpersonen, dbkinder, dbbahn, dbnotizen]
    connection.close()
    return result

def existiertid(dbid):
    result = ""
    connection = sqlite3.connect("database/kunden.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM kundenverz WHERE id=?""", ([dbid]))
    for dsatz in cursor:
        dbname = dsatz[3]
        result = dbname
    connection.close()
    return result
