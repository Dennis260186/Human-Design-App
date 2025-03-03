import streamlit as st
from datetime import datetime
from fpdf import FPDF
import random
import requests
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------
# Human Design Berechnung
# ---------------------------
def berechne_human_design(name, geburtsdatum, geburtszeit, geburtsort):
    typen = ["Generator", "Manifestierender Generator", "Manifestor", "Projektor", "Reflektor"]
    autoritaet = ["Emotional", "Sakral", "Milz", "Ego", "Selbst", "Lunar"]
    profile = ["1/3 Forscher/Märtyrer", "4/6 Opportunist/Rollemodell", "5/1 Ketzer/Erforscher"]

    return {
        "Typ": random.choice(typen),
        "Strategie": "Reagieren" if "Generator" in random.choice(typen) else "Einladung abwarten",
        "Autorität": random.choice(autoritaet),
        "Profil": random.choice(profile),
        "Inkarnationskreuz": "Rechtswinkel-Kreuz der Spannung",
    }

# ---------------------------
# Astrologie API Berechnungen (ersetzt Swiss Ephemeris)
# ---------------------------
ASTRO_API_URL = "https://api.astrologyapi.com/v1/planets"
ASTRO_API_KEY = "DEIN_API_KEY"  # Bitte hier den API-Schlüssel einfügen

def astrologischer_chart(geburtsdatum, geburtszeit, geburtsort):
    payload = {
        "date": geburtsdatum.strftime("%Y-%m-%d"),
        "time": geburtszeit.strftime("%H:%M"),
        "location": geburtsort
    }
    headers = {
        "Authorization": f"Bearer {ASTRO_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(ASTRO_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Astrologie API konnte nicht abgerufen werden"}

# ---------------------------
# Astrologie-Radix Darstellung
# ---------------------------
def zeichne_radix(chart):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    for planet, daten in chart.items():
        if isinstance(daten, dict) and "longitude" in daten:
            x = np.cos(np.radians(daten["longitude"]))
            y = np.sin(np.radians(daten["longitude"]))
            ax.scatter(x, y, label=f'{planet}', s=100)

    ax.legend()
    return fig

# ---------------------------
# PDF-Generierung
# ---------------------------
def erstelle_pdf(report_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Titel
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Dein Persönlicher Human Design & Astrologie Report", ln=True, align="C")
    pdf.ln(10)

    # Persönliche Daten
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "Persönliche Angaben", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Name: {report_data['name']}\nGeburtsort: {report_data['geburtsort']}\nGeburtsdatum: {report_data['geburtsdatum']}\nGeburtszeit: {report_data['geburtszeit']}")
    pdf.ln(10)

    # Human Design
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "Human Design", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in report_data['human_design'].items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.ln(10)

    # Astrologie
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "Astrologisches Geburtshoroskop", ln=True)
    pdf.set_font("Arial", size=12)
    
    for planet, daten in report_data['chart'].items():
        if isinstance(daten, dict) and "longitude" in daten:
            pdf.cell(0, 10, f"{planet}: {daten['longitude']}°", ln=True)

    pdf.ln(10)

    # Speichern als PDF
    pdf_filename = "Human_Design_Report.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

# ---------------------------
# Streamlit Web-App
# ---------------------------
st.title("🔮 Human Design & Astrologie Report")

st.sidebar.header("Gib deine Daten ein")
name = st.sidebar.text_input("Name", value="Max Mustermann")
geburtsort = st.sidebar.text_input("Geburtsort", value="Berlin")
geburtsdatum = st.sidebar.date_input("Geburtsdatum", datetime(1986, 1, 26))
geburtszeit = st.sidebar.time_input("Geburtszeit", value=datetime(1986, 1, 26, 10, 15).time())

# Berechnungen
human_design = berechne_human_design(name, geburtsdatum, geburtszeit, geburtsort)
chart = astrologischer_chart(geburtsdatum, geburtszeit, geburtsort)

st.subheader("📊 Dein Geburtshoroskop")
if "error" not in chart:
    fig = zeichne_radix(chart)
    st.pyplot(fig)
else:
    st.error(chart["error"])

st.subheader("🔮 Human Design Ergebnisse")
for key, value in human_design.items():
    st.write(f"**{key}:** {value}")

# PDF-Download
if st.button("📥 Erstelle & lade deinen Report als PDF herunter"):
    report_data = {
        "name": name,
        "geburtsort": geburtsort,
        "geburtsdatum": geburtsdatum.strftime("%d.%m.%Y"),
        "geburtszeit": geburtszeit.strftime("%H:%M"),
        "human_design": human_design,
        "chart": chart
    }
    pdf_file = erstelle_pdf(report_data)
    with open(pdf_file, "rb") as file:
        st.download_button("📩 Download Report", file, file_name="Human_Design_Report.pdf", mime="application/pdf")
