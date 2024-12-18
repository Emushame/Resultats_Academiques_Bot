from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io

# API Endpoint
API_BASE_URL = "http://127.0.0.1:5000"
ACADEMIC_YEAR = "2023-2024"
SESSION = "Rattrapage"

def generate_result_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-tête avec le logo et les infos de l'institution
    logo_path = "logo_2.png"  # Assurez-vous que le fichier est dans le même répertoire
    c.drawImage(logo_path, 40, height - 90, width=70, height=70)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(120, height - 40, "ISTA - KOLWEZI")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(120, height - 55, "Secrétariat Général Académique")
    c.setFont("Helvetica", 10)
    c.drawString(120, height - 70, "Adresse : 435 Av. Kasavubu, C/ Dilala, Kolwezi")
    c.drawString(120, height - 85, "Tél : +243970049135, Email : info@ista-kolwezi.ac")

    # Titre principal
    y_position = height - 120
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_position, "RELEVÉ DE COTES")
    y_position -= 30

    # Informations de l'étudiant
    c.setFont("Helvetica", 10)
    infos = [
        f"Matricule : {data['matricule']}",
        f"Nom complet : {data['nom_complet']}",
        f"Promotion : {data['promotion']}",
        f"Année académique : {ACADEMIC_YEAR}",
        f"Session : {SESSION}",
        f"Mention : {data['mention']}"
    ]
    for info in infos:
        c.drawString(40, y_position, info)
        y_position -= 15

    # Tableau des matières
    y_position -= 20
    table_data = [["Matières suivies", "Crédit", "Moyenne", "Total"]]
    for matiere, details in data['notes'].items():
        table_data.append([matiere, details['credit'], details['moyenne'], details['total']])

    # Ajout du tableau
    table = Table(table_data, colWidths=[260, 70, 70, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))
    table.wrapOn(c, 40, y_position - 150)
    table.drawOn(c, 40, y_position - 150)

    # Résumé des résultats
    y_position -= (len(data['notes']) + 1) * 20 + 100
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y_position, f"MOYENNE ANNUELLE : {data['moyenne_annuelle']}")
    c.drawString(40, y_position - 15, f"APPRECIATION : {data['appreciation']}")
    c.drawString(40, y_position - 30, f"CREDITS VALIDES : {data['credits_valides']}")
    c.drawString(40, y_position - 45, f"DECISION : {data['decision']}")

    # Signature
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 100, "Fait à Kolwezi, Le 29 / 11 / 2024")
    c.drawString(40, 80, "Le Secrétaire Général Académique")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, 60, "MUTENTA MUZALA André")
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 45, "Professeur Associé")

    # Finalisation
    c.save()
    buffer.seek(0)
    return buffer

# Commande /resultat pour un étudiant unique
async def get_resultat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage : /resultat <matricule>")
        return

    matricule = context.args[0]
    response = requests.get(f"{API_BASE_URL}/resultat/{matricule}")

    if response.status_code == 200:
        data = response.json()
        pdf_buffer = generate_result_pdf(data)
        await update.message.reply_document(
            document=pdf_buffer,
            filename=f"releve_{matricule}.pdf",
            caption=f"Relevé de cotes pour {data['nom_complet']}."
        )
    else:
        await update.message.reply_text("Étudiant non trouvé.")

# Commande /resultats pour tous les étudiants
async def get_all_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f"{API_BASE_URL}/resultats")

    if response.status_code == 200:
        students = response.json()

        # Générer un PDF avec tous les résultats
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y_position = height - 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y_position, "RESULTATS DE TOUS LES ETUDIANTS")
        y_position -= 20

        c.setFont("Helvetica", 10)
        for student in students:
            c.drawString(40, y_position, f"{student['matricule']} - {student['nom_complet']} - {student['promotion']}")
            y_position -= 15
            if y_position < 50:  # Nouvelle page si espace insuffisant
                c.showPage()
                y_position = height - 40

        c.save()
        buffer.seek(0)

        await update.message.reply_document(
            document=buffer,
            filename="resultats_tous_etudiants.pdf",
            caption="Résultats de tous les étudiants."
        )
    else:
        await update.message.reply_text("Erreur lors de la récupération des résultats.")

# Fonction principale
def main():
    bot_token = "7899674380:AAHnhcbZL5-zpN6wKrMQD5MdvBKBVD_TAUg"
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("resultat", get_resultat))
    app.add_handler(CommandHandler("resultats", get_all_results))

    print("Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
