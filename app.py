# HydroBrain MVP – Web App with Streamlit (Expanded Inputs + Outputs + Output Package Selection)

import streamlit as st
from typing import Optional
import zipfile
import io
import pandas as pd

st.set_page_config(page_title="HydroBrain – Brackish RO Designer")
st.title("HydroBrain – Brackish Water RO Designer")

st.markdown("""
Welcome to **HydroBrain**, your AI assistant for water treatment system design.
Please enter your feedwater characteristics below to begin.
""")

with st.form("input_form"):
    st.header("Basic Parameters")
    flow_gpm = st.number_input("Flow Rate (GPM)", min_value=1.0, step=1.0)
    temperature_f = st.number_input("Temperature (°F)", min_value=32.0, max_value=150.0)
    pressure_psi = st.number_input("Inlet Pressure (PSIG)", min_value=0.0, step=1.0)
    ph = st.number_input("pH", min_value=0.0, max_value=14.0)
    conductivity = st.number_input("Conductivity (µS/cm)", min_value=0.0)

    st.header("Key Water Quality Indicators")
    tds = st.number_input("TDS (mg/L)", min_value=0.0)
    hardness = st.number_input("Total Hardness (mg/L as CaCO₃)", min_value=0.0)
    silica = st.number_input("Silica (mg/L as SiO2)", min_value=0.0)
    toc = st.number_input("Total Organic Carbon (TOC) (mg/L)", min_value=0.0)
    sdi = st.number_input("Silt Density Index (SDI)", min_value=0.0, step=0.1)
    tss = st.number_input("Total Suspended Solids (TSS) (mg/L)", min_value=0.0)
    turbidity = st.number_input("Turbidity (NTU)", min_value=0.0)

    st.header("Metals (Cations)")
    iron = st.number_input("Iron (Fe, mg/L)", min_value=0.0, step=0.01)
    manganese = st.number_input("Manganese (Mn, mg/L)", min_value=0.0, step=0.01)
    calcium = st.number_input("Calcium (Ca, mg/L)", min_value=0.0)
    magnesium = st.number_input("Magnesium (Mg, mg/L)", min_value=0.0)
    sodium = st.number_input("Sodium (Na, mg/L)", min_value=0.0)

    st.header("Anions")
    chloride = st.number_input("Chloride (Cl, mg/L)", min_value=0.0)
    sulfate = st.number_input("Sulfate (SO4, mg/L)", min_value=0.0)
    nitrate = st.number_input("Nitrate (NO3, mg/L)", min_value=0.0)
    alkalinity = st.number_input("Total Alkalinity (as CaCO₃, mg/L)", min_value=0.0)

    st.header("Select Output Package")
    out_design_basis = st.checkbox("📄 Design Basis Memo")
    out_equipment_list = st.checkbox("🗂️ Equipment List (Excel)")
    out_capex = st.checkbox("💵 Budgetary CAPEX Estimate")
    out_diagram = st.checkbox("🛠️ Process Flow Diagram")
    out_zip = st.checkbox("📤 Downloadable ZIP (All files)")
    out_narrative = st.checkbox("🧠 Narrative Design Summary")

    submitted = st.form_submit_button("Run HydroBrain")

if submitted:
    recommendations = {}
    if sdi > 3 or turbidity > 1 or tss > 10:
        recommendations['Pretreatment'] = "Add Dual Media Filter (SDI > 3 or Turbidity > 1 NTU or TSS > 10 mg/L)"
    if hardness > 150:
        recommendations['Scaling Control'] = "Add antiscalant or softener (Hardness > 150 mg/L)"
    if silica > 40:
        recommendations['Silica Limit'] = "Limit RO recovery to 65% (Silica > 40 mg/L)"
    if iron > 0.3:
        recommendations['Iron Removal'] = "Add oxidation + filtration (Iron > 0.3 mg/L)"

    ro_config = {
        "Flux": "15 LMH",
        "Recovery": "75% (adjustable based on silica/alkalinity)",
        "Staging": "2:1 Array",
        "Membrane Type": "DOW BW30 or equivalent",
        "Operating Pressure Estimate": "200–300 psi",
        "Design Flow": f"{flow_gpm} GPM"
    }
    recommendations['RO System Design'] = ro_config

    st.subheader("HydroBrain Recommended Design Summary")
    for key, value in recommendations.items():
        st.write(f"**{key}**:")
        st.json(value)

    # Simulated Output Files
    output_files = {}

    if out_design_basis:
        design_text = f"HydroBrain Design Memo\n\nFlow: {flow_gpm} GPM\nRecovery: {ro_config['Recovery']}\nPretreatment: {recommendations.get('Pretreatment', 'None')}"
        output_files['design_basis.txt'] = design_text

    if out_equipment_list:
        df = pd.DataFrame([ro_config])
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Equipment')
        output_files['equipment_list.xlsx'] = buffer.getvalue()

    if out_capex:
        capex_text = "Estimated CAPEX: $300,000 ±30% (Class 4 Rough Estimate)"
        output_files['capex.txt'] = capex_text

    if out_narrative:
        narrative = "HydroBrain analyzed your brackish feedwater and proposed a standard 2-stage RO with pretreatment."
        output_files['narrative.txt'] = narrative

    if out_zip:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a") as zf:
            for name, data in output_files.items():
                if isinstance(data, str):
                    zf.writestr(name, data)
                elif isinstance(data, bytes):
                    zf.writestr(name, data)
        st.download_button("Download ZIP", data=zip_buffer.getvalue(), file_name="hydrobrain_outputs.zip")

    st.success("HydroBrain system design complete with selected outputs.")
