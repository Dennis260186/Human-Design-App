import streamlit as st

st.title("🔮 Dein Human Design Chart")

# HTML-Code zur Einbettung des BodyGraph Charts
html_code = """
<script src="https://app.bodygraphchart.com/integrate-chart/js" defer></script>
<bodygraph-embed chart-id="20748" token="83b1d17c-1cdd-48ba-ae67-90979911f380"></bodygraph-embed>
"""

# Human Design Chart in Streamlit einbinden
st.components.v1.html(html_code, height=600)

