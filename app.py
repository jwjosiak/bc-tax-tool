# app.py

import streamlit as st
from parser import parse_fuel_tax_input
from bcmftrule import check_bc_fuel_tax_applicability

st.set_page_config(page_title="BC Motor Fuel Tax Tool", layout="centered")

st.title("🚛 BC Motor Fuel Tax Determination Tool")

with st.expander("ℹ️ Click here for input guidance"):
    st.markdown("""
    To ensure the tool works properly, please use **clear and specific phrasing**.

    **✅ Fuel Type**
    - “We are selling **propane**…”  
    - “I sold **diesel**…”

    **✅ Location**
    - “The sale happened **in BC**”
    - “The customer is **in BC**” or “**outside BC**”

    **✅ Use Case**
    - “Used **in a machine**” → engine use  
    - “Used for **residential heating**”  
    - “They will **resell it**”  
    - “They will **export it to Alberta**”  

    **✅ Certificates**
    - “They provided a **common carrier certificate**”  
    - “We have a **resale certificate**”  
    - “It’s for **farm use**”  

    ❌ Avoid vague phrases like “used in operations.” Instead, say:
    - “Used **in a vehicle**”
    - “Used **for heating**”
    """)

# Text input
user_input = st.text_area("📝 Describe the transaction:", height=200, placeholder="""
Example: 
We sold propane in BC to a customer who is exporting it to Alberta using a common carrier. Title transfers outside BC.
""")

if user_input.strip():
    # Parse user input
    parsed = parse_fuel_tax_input(user_input)

    st.subheader("📋 Parsed Transaction Details")
    st.json(parsed)

    # Show parser warning if applicable
    if "parser_warning" in parsed:
        st.warning(parsed["parser_warning"])

    # Remove parser_warning before rule engine call
    parsed_cleaned = {k: v for k, v in parsed.items() if k != "parser_warning"}

    # Determine MFT applicability
    is_taxable, explanation = check_bc_fuel_tax_applicability(**parsed_cleaned)

    st.subheader("⚖️ MFT Determination Result")
    if is_taxable:
        st.error("MFT Applicable")
    else:
        st.success("MFT Exempt")

    st.markdown(f"**🧾 Explanation:** {explanation}")
    
if "operations" in text and not result.get("use_case"):
        result["parser_warning"] = "⚠️ The phrase 'operations' is too vague. Please specify if this is engine use, resale, heating, or export."
