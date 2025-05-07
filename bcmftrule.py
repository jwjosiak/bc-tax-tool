# bcmftrule.py

def check_bc_fuel_tax_applicability(
    fuel_type: str,
    origin: str,
    is_collector: bool,
    is_first_sale: bool,
    purchaser_type: str,
    use_case: str,
    certificate: str = None,
    bc_zone: str = None,
    destination: str = None,
    title_transfer_location: str = None
):
    """
    Assume the seller will not charge BC MFT.
    Return (is_supported: bool, explanation: str or list of conditions required).
    """

    # Normalize inputs safely
    fuel_type = fuel_type.lower() if fuel_type else None
    purchaser_type = purchaser_type.lower() if purchaser_type else None
    use_case = use_case.lower() if use_case else None
    certificate = certificate.lower() if certificate else None
    bc_zone = bc_zone.title() if bc_zone else None
    destination = destination.upper() if destination else None
    title_transfer_location = title_transfer_location.upper() if title_transfer_location else None

    # Validation
    required_fields = ["fuel_type", "use_case", "purchaser_type", "destination", "title_transfer_location"]
    for field in required_fields:
        if not locals()[field]:
            return False, f"Missing required field: {field}. Please provide more detail to support MFT exemption."

    # --- EXPORT CASE ---
    if use_case == "export" or destination != "BC":
        if certificate == "common_carrier":
            return True, "You may proceed without charging MFT. Export supported with Common Carrier Certificate."
        else:
            return False, "To justify not charging MFT on an export, you must obtain a valid Common Carrier Certificate."

    # --- RESALE CASE ---
    if use_case == "resale":
        if purchaser_type in ["collector", "registered_reseller"] and certificate == "resale":
            return True, "You may proceed without charging MFT. Resale supported by registered purchaser and resale certificate."
        elif purchaser_type in ["collector", "registered_reseller"]:
            return False, "You must obtain a resale certificate from the purchaser to support the resale exemption."
        else:
            return False, "Purchaser is not a registered collector or reseller. You must charge MFT."

    # --- RESIDENTIAL HEATING CASE ---
    if fuel_type == "propane" and use_case == "heating":
        if certificate == "residential_heating" and bc_zone in ["Zone II", "Zone III"]:
            return True, "You may proceed without charging MFT. Residential heating exemption applies in qualifying zone with certificate."
        else:
            return False, "To exempt propane for heating, ensure customer resides in Zone II or III and provides a Residential Heating Certificate."

    # --- FARM USE CASE ---
    if use_case == "farm_use":
        if certificate == "farm_use":
            return True, "You may proceed without charging MFT. Farm use exemption supported with valid certificate."
        else:
            return False, "You must obtain a Farm Use Certificate to justify the exemption."

    # --- DIPLOMATIC CASE ---
    if certificate == "diplomat":
        return True, "You may proceed without charging MFT. Diplomatic exemption applies."

    # --- ENGINE USE CASE ---
    if use_case == "engine_use":
        if fuel_type == "propane" and certificate in ["farm_use", "residential_heating"] and bc_zone in ["Zone II", "Zone III"]:
            return True, "You may proceed without charging MFT. Special propane use case supported with certificate and zone."
        return False, "Fuel is used in an engine. No exemption applies. You must charge MFT."

    # --- NON-ENGINE USE CASE ---
    if use_case == "non_engine_use":
        return False, "Non-engine use does not automatically exempt fuel. You must document the purpose and may still be required to charge MFT unless CRA guidance supports exemption."

    # --- DEFAULT ---
    return False, "No valid exemption criteria detected. You must charge MFT or obtain proper documentation to support zero-rating."
