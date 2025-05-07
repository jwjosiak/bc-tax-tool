# app.py

import streamlit as st
from parser import parse_fuel_tax_input
from bcmftrule import check_bc_fuel_tax_applicability

st.set_page_config(page_title="BC Motor Fuel Tax Tool", layout="centered")

st.title("🚛 BC Motor Fuel Tax Determination Tool")
st.markdown("Enter a natural-language description of your fuel transaction below.")

# Text input
user_input = st.text_area("📝 Transaction Description", height=200, placeholder="""
Example: 
We sold propane imported from the US to a registered reseller for residential heating in Zone II. 
They provided a residential heating certificate. Title transfers in BC.
""")

if user_input.strip():
    # Parse user input
    parsed = parse_fuel_tax_input(user_input)

    st.subheader("📋 Parsed Transaction Details")
    st.json(parsed)

    # Determine MFT applicability
    is_taxable, explanation = check_bc_fuel_tax_applicability(**parsed)

    st.subheader("⚖️ MFT Determination Result")
    if is_taxable:
        st.error("MFT Applicable")
    else:
        st.success("MFT Exempt")

    st.markdown(f"**🧾 Explanation:** {explanation}")
