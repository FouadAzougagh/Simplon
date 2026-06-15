import sqlite3
import requests
import csv
import io

#Création base de données
conn = sqlite3.connect("PME.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = OFF;")

cursor.execute("DROP TABLE IF EXISTS Vente")
cursor.execute("DROP TABLE IF EXISTS Produit")
cursor.execute("DROP TABLE IF EXISTS Magasin")

cursor.execute("PRAGMA foreign_keys = ON;")


#Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Magasin (
    idMagasin TEXT PRIMARY KEY,
    ville TEXT NOT NULL,
    nbrSalarie INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Produit (
    idProduit TEXT PRIMARY KEY,
    nom TEXT NOT NULL,
    prix REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Vente (
    idProduit TEXT NOT NULL,
    idMagasin TEXT NOT NULL,
    date TEXT NOT NULL,
    quantite INTEGER NOT NULL,
    PRIMARY KEY(idProduit, idMagasin, date),
    FOREIGN KEY (idProduit) REFERENCES Produit(idProduit),
    FOREIGN KEY (idMagasin) REFERENCES Magasin(idMagasin)
)
""")

#Import des fichiers
urlMagasins = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
urlProduits = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
urlVentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"

produits = requests.get(urlProduits)
contentProduit = produits.text
csvProduits = csv.reader(io.StringIO(contentProduit))

magasins = requests.get(urlMagasins)
contentMagasin = magasins.text
csvMagasins = csv.reader(io.StringIO(contentMagasin))

ventes = requests.get(urlVentes)
contentVente = ventes.text
csvVentes = csv.reader(io.StringIO(contentVente))

# Alimentation de la base de donnees
next(csvProduits)
for row in csvProduits:
    cursor.execute(""" INSERT INTO Produit (idProduit, nom, prix, stock) VALUES (?, ?, ?, ?) """, (row[1], row[0], row[2], row[3]))

next(csvMagasins)
for row in csvMagasins:
    cursor.execute(""" INSERT INTO Magasin (idMagasin, ville, nbrSalarie) VALUES (?, ?, ?) """, (row[0], row[1], row[2]))

next(csvVentes)
for row in csvVentes:
    cursor.execute(""" INSERT OR IGNORE INTO Vente (idProduit, idMagasin, date, quantite) VALUES (?, ?, ?, ?) """, (row[1], row[3], row[0], row[2]))

#Requetes SQL

#cursor.execute("""SELECT SUM(P.prix * V.quantite) AS "Chiffre d affaire" FROM Vente V, Produit P WHERE P.idProduit == V.idProduit;""")
#cursor.execute("""SELECT SUM(V.Quantite) AS "Vente par produit" FROM Vente V, Produit P WHERE P.idProduit == V.idProduit GROUP BY P.idProduit;""")
cursor.execute("""SELECT SUM(V.Quantite) AS "Vente par region" FROM Vente V, Magasin M WHERE M.idMagasin == V.idMagasin GROUP BY M.ville;""")

tables = cursor.fetchall()

print(tables)