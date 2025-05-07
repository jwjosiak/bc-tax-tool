# parser.py

import re

def parse_fuel_tax_input(text: str) -> dict:
    """
    Parses a natural language input describing a fuel transaction into a structured dictionary
    suitable for use with bcmftrule.py's check_bc_fuel_tax_applicability().

    Returns a dictionary with all required fields.
    """

    result = {
        "fuel_type": None,
        "origin": None,
        "is_collector": False,
        "is_first_sale": True,
        "purchaser_type": None,
        "use_case": None,
        "certificate": None,
        "bc_zone": None,
        "destination": None,
        "title_transfer_location": None
    }

    text = text.lower()

    # FUEL TYPE
    for fuel in ["gasoline", "diesel", "propane", "aviation fuel", "jet fuel"]:
        if fuel in text:
            result["fuel_type"] = fuel
            break

    # ORIGIN
    if "imported" in text:
        result["origin"] = "imported"
    elif "manufactured in bc" in text or "produced in bc" in text:
        result["origin"] = "manufactured"
    
    # COLLECTOR STATUS
    if "collector" in text or "we are a collector" in text:
        result["is_collector"] = True
    
    # PURCHASER TYPE
    for purchaser in ["collector", "registered reseller", "reseller", "end user", "retail dealer", "export"]:
        if purchaser in text:
            result["purchaser_type"] = purchaser.replace(" ", "_")
            break

    # USE CASE
    if "engine" in text or "combustion" in text:
        result["use_case"] = "engine_use"
    elif "non-engine" in text or "feedstock" in text:
        result["use_case"] = "non_engine_use"
    elif "resell" in text or "resale" in text:
        result["use_case"] = "resale"
    elif "farm" in text:
        result["use_case"] = "farm_use"
    elif "heating" in text or "residential" in text:
        result["use_case"] = "heating"
    elif "export" in text or "outside bc" in text:
        result["use_case"] = "export"
    
    # CERTIFICATES
    if "common carrier" in text:
        result["certificate"] = "common_carrier"
    elif "resale certificate" in text or "reseller certificate" in text:
        result["certificate"] = "resale"
    elif "farm fuel" in text or "farm use certificate" in text:
        result["certificate"] = "farm_use"
    elif "heating certificate" in text or "residential certificate" in text:
        result["certificate"] = "residential_heating"
    elif "diplomat" in text or "foreign government" in text:
        result["certificate"] = "diplomat"

    # BC ZONE
    for zone in ["zone i", "zone ii", "zone iii"]:
        if zone in text:
            result["bc_zone"] = zone.title()
            break

    # DESTINATION
    if "outside bc" in text or "to alberta" in text or "to the us" in text:
        result["destination"] = "OUTSIDE BC"
    elif "within bc" in text or "in bc" in text:
        result["destination"] = "BC"

    # TITLE TRANSFER LOCATION
    if "title transfers in bc" in text:
        result["title_transfer_location"] = "BC"
    elif "title transfers outside bc" in text:
        result["title_transfer_location"] = "OUTSIDE BC"

    return result


# Example usage
if __name__ == "__main__":
    sample_input = """
    We are selling propane imported from the US to an end user in Zone II for residential heating.
    The buyer has a residential heating certificate and lives in BC. Title transfers in BC.
    """
    parsed = parse_fuel_tax_input(sample_input)
    for k, v in parsed.items():
        print(f"{k}: {v}")
