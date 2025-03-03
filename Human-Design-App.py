{\rtf1\ansi\ansicpg1252\cocoartf2820
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
from datetime import datetime\
from fpdf import FPDF\
import random\
\
# ---------------------------\
# Astrologische Berechnungen\
# ---------------------------\
def astrologischer_chart(name, geburtsdatum, geburtszeit, geburtsort):\
    tierkreiszeichen = [\
        "Widder", "Stier", "Zwillinge", "Krebs", "L\'f6we", "Jungfrau",\
        "Waage", "Skorpion", "Sch\'fctze", "Steinbock", "Wassermann", "Fische"\
    ]\
    \
    planeten = ["Sonne", "Mond", "Merkur", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun", "Pluto"]\
    \
    chart = \{\}\
    for planet in planeten:\
        haus = random.randint(1, 12)  # Simulierte Planetenposition\
        zeichen = random.choice(tierkreiszeichen)\
        chart[planet] = \{"Haus": haus, "Zeichen": zeichen\}\
    \
    return chart\
\
# ---------------------------\
# PDF-Generierung\
# ---------------------------\
def erstelle_pdf(report_data):\
    pdf = FPDF()\
    pdf.set_auto_page_break(auto=True, margin=15)\
    pdf.add_page()\
    pdf.set_font("Arial", size=12)\
\
    # Titel\
    pdf.set_font("Arial", style='B', size=16)\
    pdf.cell(200, 10, "Dein Pers\'f6nlicher Human Design & Astrologie Report", ln=True, align="C")\
    pdf.ln(10)\
\
    # Pers\'f6nliche Daten\
    pdf.set_font("Arial", style='B', size=14)\
    pdf.cell(200, 10, "Pers\'f6nliche Angaben", ln=True)\
    pdf.set_font("Arial", size=12)\
    pdf.multi_cell(0, 10, f"Name: \{report_data['name']\}\\nGeburtsort: \{report_data['geburtsort']\}\\nGeburtsdatum: \{report_data['geburtsdatum']\}\\nGeburtszeit: \{report_data['geburtszeit']\}")\
    pdf.ln(10)\
\
    # Astrologie\
    pdf.set_font("Arial", style='B', size=14)\
    pdf.cell(200, 10, "Astrologisches Geburtshoroskop", ln=True)\
    pdf.set_font("Arial", size=12)\
    \
    for planet, daten in report_data['chart'].items():\
        pdf.cell(0, 10, f"\{planet\}: \{daten['Zeichen']\} im \{daten['Haus']\}. Haus", ln=True)\
\
    pdf.ln(10)\
\
    # Speichern als PDF\
    pdf_filename = "Human_Design_Report.pdf"\
    pdf.output(pdf_filename)\
    return pdf_filename\
\
# ---------------------------\
# Streamlit Web-App\
# ---------------------------\
st.title("\uc0\u55357 \u56622  Human Design & Astrologie Report")\
\
st.sidebar.header("Gib deine Daten ein")\
name = st.sidebar.text_input("Name", value="Max Mustermann")\
geburtsort = st.sidebar.text_input("Geburtsort", value="Berlin")\
geburtsdatum = st.sidebar.date_input("Geburtsdatum", datetime(1986, 1, 26))\
geburtszeit = st.sidebar.time_input("Geburtszeit", value=datetime(1986, 1, 26, 10, 15).time())\
\
# Berechnung des astrologischen Charts\
chart = astrologischer_chart(name, geburtsdatum, geburtszeit, geburtsort)\
\
st.subheader("\uc0\u55357 \u56522  Dein Geburtshoroskop")\
for planet, daten in chart.items():\
    st.write(f"**\{planet\}:** \{daten['Zeichen']\} im \{daten['Haus']\}. Haus")\
\
# PDF-Download\
if st.button("\uc0\u55357 \u56549  Erstelle & lade deinen Report als PDF herunter"):\
    report_data = \{\
        "name": name,\
        "geburtsort": geburtsort,\
        "geburtsdatum": geburtsdatum.strftime("%d.%m.%Y"),\
        "geburtszeit": geburtszeit.strftime("%H:%M"),\
        "chart": chart\
    \}\
    pdf_file = erstelle_pdf(report_data)\
    with open(pdf_file, "rb") as file:\
        st.download_button("\uc0\u55357 \u56553  Download Report", file, file_name="Human_Design_Report.pdf", mime="application/pdf")\
}