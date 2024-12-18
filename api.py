# 2. api.py
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

# Connexion à la base de données MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='resultats_etudiants',
            user='root',  # Remplacez par votre utilisateur
            password=''  # Remplacez par votre mot de passe
        )
        if connection.is_connected():
            print("Connexion réussie à la base de données")
        return connection
    except Error as e:
        print("Erreur de connexion à MySQL", e)
        return None

# Route pour obtenir les résultats d'un étudiant par matricule
@app.route('/resultat/<string:matricule>', methods=['GET'])
def get_resultat(matricule):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)

        # Récupération des informations de l'étudiant
        cursor.execute("SELECT * FROM etudiants WHERE matricule = %s", (matricule,))
        student = cursor.fetchone()

        if student:
            # Récupération des notes de l'étudiant
            cursor.execute("""
                SELECT cours.nom_cours, cours.credit, resultats.moyenne, resultats.total
                FROM resultats
                JOIN cours ON resultats.code_cours = cours.code_cours
                WHERE resultats.matricule = %s
            """, (matricule,))
            notes = cursor.fetchall()

            # Structuration des données
            student['notes'] = {note['nom_cours']: {
                "credit": note['credit'],
                "moyenne": note['moyenne'],
                "total": note['total']
            } for note in notes}

            connection.close()
            return jsonify(student), 200
        else:
            connection.close()
            return jsonify({"message": "Étudiant non trouvé"}), 404
    else:
        return jsonify({"message": "Erreur de connexion à la base de données"}), 500


# Route pour obtenir tous les résultats des étudiants
@app.route('/resultats', methods=['GET'])
def get_all_results():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etudiants")
        students = cursor.fetchall()

        # Conversion des notes en dictionnaire pour chaque étudiant
        for student in students:
            student['notes'] = json.loads(student['notes'])

        connection.close()
        return jsonify(students), 200
    else:
        return jsonify({"message": "Erreur de connexion à la base de données"}), 500

if __name__ == '__main__':
    app.run(debug=True)
