# app.py

import streamlit as st
from parser import parse_fuel_tax_input
from bcmftrule import check_bc_fuel_tax_applicability

st.set_page_config(page_title="BC Motor Fuel Tax Tool", layout="centered")
st.title("🌲 BC Motor Fuel Tax Determination Tool")

with st.expander("ℹ️ Click here for input guidance"):
    st.markdown("""
    This tool assumes you will **not** charge BC Motor Fuel Tax (MFT) on a transaction.

    It will tell you what conditions or documents are required to justify that position.

    ---
    ### ✅ Use clear phrases like:
    - “We sold **propane** in BC to a customer who is **exporting** it to Alberta.”
    - “Sold **diesel** to a **registered reseller** who provided a **resale certificate**.”
    - “**Propane** sold to a **farmer** for **heating** in Zone II with a certificate.”
    - “Used in a **machine**, **vehicle**, or for **combustion**” → *engine use*
    - “Used in a **boiler**, for **steam generation**, or as **feedstock**” → *non-engine use*

    ---
    ### ❌ Avoid vague language:
    - “Used in operations”
    - “General use” or “business use”

    ✅ Be as specific as possible. The tool uses keywords to classify the tax treatment.
    """)

user_input = st.text_area(
    "📝 Describe the transaction:",
    height=200,
    placeholder="Example: Sold propane in BC to a customer exporting to Alberta using a common carrier. Title transfers outside BC."
)

if user_input.strip():
    # Parse input
    parsed = parse_fuel_tax_input(user_input)

    # Show parser warning if applicable
    if "parser_warning" in parsed:
        st.warning(parsed["parser_warning"])

    # Clean dictionary for rules engine
    parsed_cleaned = {k: v for k, v in parsed.items() if k != "parser_warning"}

    # Friendly summary
    st.markdown("**🧾 Summary of Key Inputs**")
    st.markdown(f"- Fuel Type: `{parsed_cleaned.get('fuel_type', 'N/A')}`")
    st.markdown(f"- Use Case: `{parsed_cleaned.get('use_case', 'N/A')}`")
    st.markdown(f"- Certificate: `{parsed_cleaned.get('certificate', 'None')}`")
    st.markdown(f"- Destination: `{parsed_cleaned.get('destination', 'N/A')}`")

    # Optional parsed dump
    with st.expander("🧪 Show full parsed input (for developers or audit purposes)"):
        st.write(parsed_cleaned)

    # Check tax treatment
    is_supported, message = check_bc_fuel_tax_applicability(**parsed_cleaned)

    st.subheader("⚖️ MFT Exemption Guidance")
    if is_supported:
        st.success("✅ You may proceed without charging MFT.")
        st.markdown(f"**Reason:** {message}")
    else:
        st.error("⚠️ Charging no MFT is not currently supported.")
        st.markdown(f"**Action Required:** {message}")
