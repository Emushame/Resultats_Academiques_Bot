# Resultats_Academiques_Bot
Ce projet permet de générer des relevés académiques pour les étudiants à partir d'une base de données MySQL. Le projet comprend une API Flask et un bot Telegram pour interagir avec les utilisateurs et fournir les relevés au format PDF.
Fonctionnalités principales

API Flask :

Obtenir les résultats d'un étudiant par son matricule.

Obtenir la liste de tous les résultats des étudiants.

Bot Telegram :

Générer un relevé de cotes en PDF en fonction du matricule fourni par l'utilisateur.

Génération de PDF :

Inclut les informations personnelles de l'étudiant, les notes par matière, la moyenne annuelle, et une décision académique.

Structure du projet

Releves_Academiques/
├── bot.py         # Bot Telegram pour générer et envoyer les relevés.
├── api.py         # API Flask pour interagir avec la base de données.
├── db.sql        # Script de création de la base de données.
├── logo.png      # Logo utilisé dans les PDF.
├── requirements.txt  # Dépendances Python.
├── README.md     # Documentation du projet.

1. Prérequis

Outils requis

Python 3.8+

MySQL

Virtualenv (optionnel)

Telegram Bot Token

Installation des dépendances

Créez et activez un environnement virtuel (optionnel) :

python -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate

Installez les dépendances :

pip install -r requirements.txt

2. Configuration de la base de données

Script SQL (db.sql)

Créez une base de données MySQL et exécutez le script suivant :

CREATE DATABASE resultats_etudiants;
USE resultats_etudiants;

CREATE TABLE etudiants (
    matricule VARCHAR(20) PRIMARY KEY,
    nom_complet VARCHAR(100) NOT NULL,
    promotion VARCHAR(50) NOT NULL,
    mention VARCHAR(50) NOT NULL,
    moyenne_annuelle FLOAT NOT NULL,
    appreciation VARCHAR(100) NOT NULL,
    credits_valides INT NOT NULL,
    decision VARCHAR(100) NOT NULL,
    notes JSON NOT NULL
);

INSERT INTO etudiants (matricule, nom_complet, promotion, mention, moyenne_annuelle, appreciation, credits_valides, decision, notes)
VALUES (
    'ETU001', 'Jean Dupont', 'L1', 'Très Bien', 15.5, 'Excellent', 30, 'Réussi',
    '{"Mathématiques": {"credit": 6, "moyenne": 15, "total": 90}, "Informatique": {"credit": 5, "moyenne": 16, "total": 80}}'
);

3. API Flask

L'API Flask gère les requêtes pour récupérer les données des étudiants.

Lancer l'API

Exécutez le fichier api.py :

python api.py

Par défaut, l'API sera disponible à http://127.0.0.1:5000.

Endpoints

Obtenir les résultats d'un étudiant

GET /resultat/<matricule>

Exemple :

curl http://127.0.0.1:5000/resultat/ETU001

Obtenir tous les résultats

GET /resultats

Exemple :

curl http://127.0.0.1:5000/resultats

4. Bot Telegram

Le bot interagit avec l'utilisateur pour générer les relevés académiques.

Configuration

Modifiez le token du bot dans bot.py :

bot_token = "VOTRE_TELEGRAM_BOT_TOKEN"

Lancer le bot

Exécutez le fichier bot.py :

python bot.py

Commandes disponibles

Générer un relevé

Utilisez la commande /resultat <matricule> dans Telegram.

Exemple :

/resultat ETU001

Le bot génère un relevé PDF et l'envoie directement à l'utilisateur.

5. Personnalisation

Hardcoder l'année académique

Dans bot.py :
Ajoutez une constante pour l'année académique :

ACADEMIC_YEAR = "2023-2024"

Et utilisez-la dans le PDF :

f"Année académique : {ACADEMIC_YEAR}"

Dans api.py :
Ajoutez l'année académique dans les réponses de l'API :

student['annee_academique'] = "2023-2024"

6. Dépendances

Liste des bibliothèques requises (dans requirements.txt) :

Flask
mysql-connector-python
python-telegram-bot
reportlab
requests

Installez-les avec :

pip install -r requirements.txt

7. Améliorations futures

Ajouter une interface utilisateur pour les requêtes.

Gérer dynamiquement les sessions académiques.

Ajouter un système d'authentification pour plus de sécurité.

8. Auteur

Projet réalisé par Edouard MUSHAME.

