# bcmftrule.py

def check_bc_fuel_tax_applicability(
    fuel_type: str,
    origin: str,  # 'manufactured' or 'imported'
    is_collector: bool,
    is_first_sale: bool,
    purchaser_type: str,  # 'collector', 'registered_reseller', 'end_user', 'export'
    use_case: str,  # 'engine_use', 'non_engine_use', 'export', 'resale', 'heating', 'farm_use'
    certificate: str = None,  # 'common_carrier', 'resale', 'farm_use', 'residential_heating', 'diplomat'
    bc_zone: str = None,  # 'Zone I', 'Zone II', 'Zone III'
    destination: str = None,  # 'BC', 'Outside BC'
    title_transfer_location: str = None  # 'BC', 'Outside BC'
):
    """
    Determines BC Motor Fuel Tax applicability based on transaction details.
    Returns tuple: (is_tax_applicable: bool, explanation: str)
    """
    reasons = []

    # Normalize inputs
    fuel_type = fuel_type.lower()
    purchaser_type = purchaser_type.lower()
    use_case = use_case.lower()
    certificate = certificate.lower() if certificate else None
    bc_zone = bc_zone.title() if bc_zone else None
    destination = destination.upper() if destination else None
    title_transfer_location = title_transfer_location.upper() if title_transfer_location else None

    # Rule 1: Exports
    if use_case == "export" or destination != "BC":
        if certificate == "common_carrier" and title_transfer_location != "BC":
            return False, "MFT Exempt: Export confirmed with Common Carrier Certificate and title transfer outside BC."
        else:
            return True, "MFT Applies: Export not properly supported by Common Carrier Certificate or title transfer occurred in BC."

    # Rule 2: Resale
    if use_case == "resale":
        if purchaser_type in ["collector", "registered_reseller"] and certificate == "resale":
            return False, "MFT Exempt: Valid resale to a Collector/Reseller with resale certificate."
        else:
            return True, "MFT Applies: Resale missing valid purchaser registration or resale certificate."

    # Rule 3: Residential Heating (Propane)
    if fuel_type == "propane" and use_case == "heating":
        if certificate == "residential_heating" and bc_zone in ["Zone II", "Zone III"]:
            return False, "MFT Exempt: Propane for residential heating in eligible zone with proper certificate."
        else:
            return True, "MFT Applies: Heating exemption invalid due to zone or certificate."

    # Rule 4: Farm Use
    if use_case == "farm_use":
        if certificate == "farm_use":
            return False, "MFT Exempt: Farm use with valid farm fuel certificate."
        else:
            return True, "MFT Applies: No farm use certificate provided."

    # Rule 5: Diplomatic
    if certificate == "diplomat":
        return False, "MFT Exempt: Diplomatic exemption."

    # Rule 6: General Engine Use
    if use_case == "engine_use":
        reasons.append("Fuel used in an internal combustion engine.")
        if fuel_type == "propane" and certificate in ["farm_use", "residential_heating"] and bc_zone in ["Zone II", "Zone III"]:
            return False, "MFT Exempt: Special propane use case met."
        return True, "MFT Applies: Fuel used in engine. No applicable exemption."

    # Rule 7: Non-engine use
    if use_case == "non_engine_use":
        return True, "MFT Applies: Non-engine use does not automatically exempt fuel. Documentation required to support exemption claim."

    return True, "MFT Applies: No valid exemption criteria met."


# Example usage
if __name__ == "__main__":
    result, explanation = check_bc_fuel_tax_applicability(
        fuel_type="propane",
        origin="imported",
        is_collector=False,
        is_first_sale=True,
        purchaser_type="end_user",
        use_case="heating",
        certificate="residential_heating",
        bc_zone="Zone II",
        destination="BC",
        title_transfer_location="BC"
    )
    print(f"Tax Applicable? {'Yes' if result else 'No'}\nReason: {explanation}")
