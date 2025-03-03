import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# ---------------------------
# Human Design Berechnung (Dummy-Daten für Demo)
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
# Human Design Bodygraph Zeichnen
# ---------------------------
def zeichne_bodygraph():
    fig, ax = plt.subplots(figsize=(5, 8))
    
    # Zentren Koordinaten
    zentren = {
        "Kopf": (0, 7), "Ajna": (0, 5.5), "Kehle": (0, 4),
        "G-Zentrum": (0, 2.5), "Herz": (1, 2.5), "Solarplexus": (1, 1),
        "Milz": (-1, 1), "Sakral": (0, 0), "Wurzel": (0, -1.5)
    }
    
    # Zentren zeichnen
    for name, (x, y) in zentren.items():
        ax.scatter(x, y, s=800, color="lightgrey", edgecolor="black", zorder=2)
        ax.text(x, y, name, fontsize=10, ha="center", va="center", zorder=3, color="black")

    # Kanäle verbinden Zentren
    verbindungen = [
        ("Kopf", "Ajna"), ("Ajna", "Kehle"), ("Kehle", "G-Zentrum"),
        ("G-Zentrum", "Sakral"), ("Sakral", "Wurzel"), ("G-Zentrum", "Herz"),
        ("Herz", "Solarplexus"), ("Sakral", "Solarplexus"), ("Sakral", "Milz"),
        ("Wurzel", "Solarplexus"), ("Wurzel", "Milz")
    ]

    for start, end in verbindungen:
        x_values = [zentren[start][0], zentren[end][0]]
        y_values = [zentren[start][1], zentren[end][1]]
        ax.plot(x_values, y_values, "k-", linewidth=2, alpha=0.5)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 8)
    ax.axis("off")
    return fig

# ---------------------------
# Streamlit Web-App
# ---------------------------
st.title("🔮 Dein persönlicher Human Design Bodygraph")

st.sidebar.header("Gib deine Daten ein")
name = st.sidebar.text_input("Name", value="Max Mustermann")
geburtsort = st.sidebar.text_input("Geburtsort", value="Berlin")
geburtsdatum = st.sidebar.date_input("Geburtsdatum")
geburtszeit = st.sidebar.time_input("Geburtszeit")

# Berechnung
human_design = berechne_human_design(name, geburtsdatum, geburtszeit, geburtsort)

st.subheader("📊 Dein Human Design Chart")
fig = zeichne_bodygraph()
st.pyplot(fig)

st.subheader("🔮 Human Design Details")
for key, value in human_design.items():
    st.write(f"**{key}:** {value}")
