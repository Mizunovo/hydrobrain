# HydroBrain MVP – Web App with Streamlit

import streamlit as st
from typing import Optional

st.set_page_config(page_title="HydroBrain – Brackish RO Designer")
st.title("HydroBrain – Brackish Water RO Designer")

st.markdown("""
Welcome to **HydroBrain**, your AI assistant for water treatment system design.
Please enter your feedwater characteristics below to begin.
""")

# Input form
with st.form("input_form"):
    flow_gpm = st.number_input("Flow Rate (GPM)", min_value=1.0, step=1.0)
    temperature_f = st.number_input("Temperature (°F)", min_value=32.0, max_value=150.0)
    pressure_psi = st.number_input("Inlet Pressure (PSIG)", min_value=0.0, step=1.0)
    tds = st.number_input("TDS (mg/L)", min_value=0.0)
    hardness = st.number_input("Hardness (mg/L as CaCO₃)", min_value=0.0)
    silica = st.number_input("Silica (mg/L)", min_value=0.0)
    toc = st.number_input("TOC (mg/L)", min_value=0.0)
    ph = st.number_input("pH", min_value=0.0, max_value=14.0)
    sdi = st.number_input("Silt Density Index (SDI)", min_value=0.0, step=0.1)
    iron = st.number_input("Iron (mg/L)", min_value=0.0, step=0.01)
    manganese = st.number_input("Manganese (mg/L)", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Run HydroBrain")

if submitted:
    recommendations = {}

    if sdi > 3:
        recommendations['Pretreatment'] = "Add Dual Media Filter (SDI > 3)"
    if hardness > 150:
        recommendations['Softening'] = "Add antiscalant or softener (Hardness > 150 mg/L)"
    if silica > 40:
        recommendations['Silica'] = "Limit RO recovery to 65% (Silica > 40 mg/L)"
    if iron > 0.3:
        recommendations['Iron'] = "Add oxidation + filtration (Iron > 0.3 mg/L)"

    recommendations['RO Configuration'] = {
        "Flux": "15 LMH",
        "Recovery": "75% (adjustable)",
        "Staging": "2:1 Array",
        "Membrane": "DOW BW30 or equivalent"
    }

    st.subheader("Recommended Design")
    for key, value in recommendations.items():
        st.write(f"**{key}**: {value}")

    st.success("HydroBrain analysis complete!")
