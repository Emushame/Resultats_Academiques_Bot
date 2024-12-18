import pandas as pd
import mysql.connector
from mysql.connector import Error
import json
import random


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


# Lecture du fichier Excel
def read_excel(file_path):
    return pd.read_excel(file_path)


# Insertion des données dans la base de données
# Fonction pour calculer le pourcentage, la mention, et la cote pondérée
def calculate_percentage_and_mention(notes, weights):
    total_points = sum([notes[course] * weights[course] for course in notes])
    total_weight = sum(weights.values())
    weighted_average = total_points / total_weight

    percentage = (weighted_average / 20) * 100  # La note maximale est 20
    mention = ""

    # Déterminer la mention
    if percentage >= 85:
        mention = "Grande Distinction"
    elif percentage >= 70:
        mention = "Distinction"
    elif percentage >= 50:
        mention = "Satisfaction"
    else:
        mention = "Ajourné"

    return round(weighted_average, 2), round(percentage, 2), mention


# Liste des étudiants
students = [
    "BANZA MALOBA YUMBA Ken", "BONDO BINENE Sam", "ILUNGA MANIEMA Jiriel",
    "ILUNGA MWENZE Anne-Marie", "ILUNGA NGOIE Betty", "KABAMBA MWAPE Rebecca",
    "KABWIT YAV David", "KALUWE KASELA Gracia", "KANAM NAWEJ Tryphene",
    "KAPINGA WA ZEYA Rosie", "KASONGO KAZEMBE Schadrack", "KAVUNG SANGON Chadrack",
    "KAWAYA UFUMBA Samson", "KAZADI BALTAZARD Dieu-Merci", "KOJI KAMBWANDJA Séraphin",
    "KUMWIMBA KAYEYE Bernice", "MANDA MWANA MUHOYO Crispin", "MUJINGA MILANGA Melissa",
    "MURUND CHIMWANG Lydia", "MWANABUTE MUKENA Prodige", "NGIOE MUJINGA Victoire",
    "NGOYI MUTONI Jhonson", "NTAMB MBAV Christian", "SAFALANI MWAYUMA Véronique",
    "TSHIYAMB KANTENG Joy", "TUMBA LOSHIMA Boustin"
]

# Liste des promotions
promotions = ["BAC1", "BAC2", "BAC3"]

# Liste des cours pour BAC1
bac1_courses = [
    "Informatique et bureautique", "Initiation à l'Informatique", "Bureautique",
    "Algorithmique 1", "Langage de Programmation-1 (langage VBnet)", "Langue et techniques d'expressions",
    "Anglais 1", "Français", "Introduction à la recherche et méthodologie du travail",
    "Valeurs, principes et symboles de la République et Ethique", "Mathématique pour Ingénieur Informaticien",
    "Comptabilité Générale", "Programmation Web-1", "Droit civil et législation sociale",
    "Architecture des ordinateurs et réseaux", "Architecture des ordinateurs", "Réseaux", "Physiques",
    "Electricité", "Electronique", "Introduction à l'Economie", "Projet-1"
]

# Liste des cours pour BAC2
bac2_courses = [
    "Algorithmique et Méthodes de programmation", "Langages de Programmation Objet (VB.Net et C++)",
    "Modélisation et base de données", "Méthode Mérise", "Base de données", "Statistique (Probabilité)",
    "Géometrie pour Ingénieur Informaticien", "Système d'exploitation", "Circuits Logiques", "Programmation Web-2",
    "Méthodes & Analyse Numérique", "Réseaux Informatiques-1 (Réseaux Informatiques)", "Anglais Techniques-2",
    "Gestion de Projets Informatiques", "Techniques de Maintenance-1", "Projet-2"
]

# Liste des cours pour BAC3
bac3_courses = [
    "Machine Learning", "Langage de Programmation Mobile", "Génie Logiciel", "Administration de base de données",
    "Conception des systèmes d'information", "Introduction à la Cryptologie", "Programmation Objet-3 (Python)",
    "Droit Informatique et Cybercriminalité", "Déontologie de l'informaticien", "Séminaire Informatique",
    "Audit Informatique", "Projet Tutoré", "Stage Académique", "Architecture des Systèmes Informatiques",
    "Système d'Information et Gestion", "Sécurité des Systèmes et Réseaux", "Blockchain et Cryptomonnaies"
]


# Script pour insérer les cours et notes
def insert_students_and_courses():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Générer les données des étudiants
            student_data = []
            for index, student in enumerate(students):
                promotion = random.choice(promotions)
                matricule = f"ETU{str(index + 1).zfill(3)}"
                filiere = "Informatique"
                notes = {}
                weights = {}

                # Générer des notes et des pondérations pour chaque cours
                if promotion == "BAC1":
                    courses = bac1_courses
                elif promotion == "BAC2":
                    courses = bac2_courses
                else:
                    courses = bac3_courses

                for course in courses:
                    notes[course] = random.randint(1, 20)  # Note sur 20
                    weights[course] = random.randint(1, 6)  # Pondération aléatoire entre 1 et 6

                weighted_average, percentage, mention = calculate_percentage_and_mention(notes, weights)

                student_data.append((student, matricule, filiere, promotion, notes, weights, weighted_average, percentage, mention))

            # Insérer les données dans la base de données
            # Insérer les données dans la base de données
            for student in student_data:
                query = """
                INSERT INTO etudiants 
                (matricule, nom_complet, promotion, filiere, notes, poids, moyenne_ponderee, pourcentage, mention)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    student[1],  # Matricule
                    student[0],  # Nom complet
                    student[3],  # Promotion
                    student[2],  # Filière
                    json.dumps(student[4]),  # Notes sous forme de JSON
                    json.dumps(student[5]),  # Pondérations sous forme de JSON
                    student[6],  # Moyenne pondérée
                    student[7],  # Pourcentage
                    student[8]  # Mention
                ))
            connection.commit()
            print(f"{len(student_data)} étudiants ajoutés avec succès.")

        except Error as e:
            print("Erreur lors de l'insertion :", e)
        finally:
            connection.close()
    else:
        print("Erreur de connexion à la base de données.")


# Fonction principale
def main():
    file_path = 'Resultats_Exemple.xlsx'  # Spécifiez le chemin vers votre fichier Excel
    connection = create_connection()

    if connection:
        data = read_excel(file_path)
        insert_students_and_courses()  # Appel à la fonction correcte pour insérer les étudiants et leurs notes
        connection.close()


if __name__ == "__main__":
    main()
