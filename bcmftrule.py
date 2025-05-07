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
    Seller assumes they will not charge BC MFT.
    Returns (is_supported: bool, explanation_with_references: str)
    """

    # Normalize safely
    fuel_type = fuel_type.lower() if fuel_type else None
    purchaser_type = purchaser_type.lower() if purchaser_type else None
    use_case = use_case.lower() if use_case else None
    certificate = certificate.lower() if certificate else None
    bc_zone = bc_zone.title() if bc_zone else None
    destination = destination.upper() if destination else None
    title_transfer_location = title_transfer_location.upper() if title_transfer_location else None

    # Required fields check
    required_fields = ["fuel_type", "use_case", "purchaser_type", "destination", "title_transfer_location"]
    for field in required_fields:
        if not locals()[field]:
            return False, f"Missing required field: '{field}'. Cannot support exemption without it."

    # --- EXPORT CASE ---
    if use_case == "export" or destination != "BC":
        if certificate == "common_carrier":
            return True, (
                "✅ You may proceed without charging MFT. Export is supported by a Common Carrier Certificate. "
                "[Ref: MFT Act s. 1, s. 74; Bulletin MFT-CT 005]"
            )
        else:
            return False, (
                "❌ You must obtain a Common Carrier Certificate to support MFT exemption on exports. "
                "[Ref: MFT Act s. 1 'export', s. 74(1)(e); Bulletin MFT-CT 005]"
            )

    # --- RESALE CASE ---
    if use_case == "resale":
        if purchaser_type in ["collector", "registered_reseller"] and certificate == "resale":
            return True, (
                "✅ You may proceed without charging MFT. Sale for resale is supported by purchaser's status and resale certificate. "
                "[Ref: MFT Regulation s. 39; Bulletin MFT-CT 003]"
            )
        elif purchaser_type in ["collector", "registered_reseller"]:
            return False, (
                "❌ A resale certificate is required to justify exemption when selling to a registered reseller. "
                "[Ref: MFT Regulation s. 39; Bulletin MFT-CT 003]"
            )
        else:
            return False, (
                "❌ MFT must be charged. Purchaser is not a registered reseller or collector. "
                "[Ref: MFT Act s. 73(1); Bulletin MFT-CT 003]"
            )

    # --- RESIDENTIAL HEATING CASE ---
    if fuel_type == "propane" and use_case == "heating":
        if certificate == "residential_heating" and bc_zone in ["Zone II", "Zone III"]:
            return True, (
                "✅ You may proceed without charging MFT. Residential heating exemption applies in Zone II or III with certificate. "
                "[Ref: Bulletin MFT-CT 004; MFT Regulation Schedule Zones]"
            )
        else:
            return False, (
                "❌ You must obtain a Residential Heating Certificate and ensure the customer resides in Zone II or III. "
                "[Ref: Bulletin MFT-CT 004]"
            )

    # --- FARM USE CASE ---
    if use_case == "farm_use":
        if certificate == "farm_use":
            return True, (
                "✅ You may proceed without charging MFT. Farm fuel exemption supported by valid Farm Use Certificate. "
                "[Ref: MFT Regulation s. 18; Bulletin MFT-CT 006]"
            )
        else:
            return False, (
                "❌ You must obtain a Farm Use Certificate from the purchaser to support the exemption. "
                "[Ref: MFT Regulation s. 18; Bulletin MFT-CT 006]"
            )

    # --- DIPLOMATIC CASE ---
    if certificate == "diplomat":
        return True, (
            "✅ You may proceed without charging MFT. Diplomatic exemption applies. "
            "[Ref: CRA diplomatic tax relief guidelines; BC Finance may request evidence.]"
        )

    # --- ENGINE USE CASE ---
    if use_case == "engine_use":
        if fuel_type == "propane" and certificate in ["farm_use", "residential_heating"] and bc_zone in ["Zone II", "Zone III"]:
            return True, (
                "✅ You may proceed without charging MFT. Special propane engine use exemption applies with proper certificate and zone. "
                "[Ref: Bulletin MFT-CT 004 & 006]"
            )
        return False, (
            "❌ MFT must be charged. Fuel is used in an internal combustion engine and no applicable exemption applies. "
            "[Ref: MFT Act s. 73(1)]"
        )

    # --- NON-ENGINE USE CASE ---
    if use_case == "non_engine_use":
        return False, (
            "❌ MFT must generally be charged. Non-engine use does not automatically qualify for exemption unless documented for approved purposes (e.g. feedstock). "
            "[Ref: MFT Act s. 73; CRA fuel use policies]"
        )

    # --- CATCH-ALL ---
    return False, (
        "❌ No valid exemption detected. You must charge MFT unless supported by resale, export, heating, or farm documentation. "
        "[Ref: MFT Act s. 73; Bulletins MFT-CT 003–006]"
    )
