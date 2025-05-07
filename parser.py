# parser.py

import re

def parse_fuel_tax_input(text: str) -> dict:
    """
    Parses natural language description of a fuel transaction into structured fields
    for check_bc_fuel_tax_applicability().
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

    # --- FUEL TYPE ---
    for fuel in ["gasoline", "diesel", "propane", "aviation fuel", "jet fuel"]:
        if fuel in text:
            result["fuel_type"] = fuel
            break

    # --- ORIGIN ---
    if "imported" in text or "from the us" in text:
        result["origin"] = "imported"
    elif "manufactured in bc" in text or "produced in bc" in text:
        result["origin"] = "manufactured"

    # --- COLLECTOR STATUS ---
    if "we are a collector" in text or "as a collector" in text:
        result["is_collector"] = True

    # --- PURCHASER TYPE ---
    if "registered reseller" in text or "reseller" in text:
        result["purchaser_type"] = "registered_reseller"
    elif "collector" in text:
        result["purchaser_type"] = "collector"
    elif "retail dealer" in text:
        result["purchaser_type"] = "retail_dealer"
    elif "export" in text:
        result["purchaser_type"] = "export"
    elif "end user" in text or "customer" in text:
        result["purchaser_type"] = "end_user"

    # --- USE CASE ---
    if re.search(r"(engine|machine|truck|vehicle|combustion)", text):
        result["use_case"] = "engine_use"
    elif re.search(r"(resale|resell)", text):
        result["use_case"] = "resale"
    elif re.search(r"(export|exported|outside bc|to alberta|to the us)", text):
        result["use_case"] = "export"
    elif re.search(r"(heating|residential)", text):
        result["use_case"] = "heating"
    elif re.search(r"(farm|farming|agriculture)", text):
        result["use_case"] = "farm_use"
    elif re.search(r"(feedstock|industrial|non-engine|nonengine)", text):
        result["use_case"] = "non_engine_use"

    # --- CERTIFICATE ---
    if "common carrier" in text:
        result["certificate"] = "common_carrier"
    elif "resale certificate" in text or "reseller certificate" in text:
        result["certificate"] = "resale"
    elif "farm fuel certificate" in text or "farm certificate" in text:
        result["certificate"] = "farm_use"
    elif "residential certificate" in text or "heating certificate" in text:
        result["certificate"] = "residential_heating"
    elif "diplomat" in text or "foreign government" in text:
        result["certificate"] = "diplomat"

    # --- BC ZONE ---
    if "zone i" in text:
        result["bc_zone"] = "Zone I"
    elif "zone ii" in text:
        result["bc_zone"] = "Zone II"
    elif "zone iii" in text:
        result["bc_zone"] = "Zone III"

    # --- DESTINATION ---
    if re.search(r"(export|to alberta|to the us|outside of bc|another province)", text):
        result["destination"] = "OUTSIDE BC"
    elif re.search(r"(in bc|within bc|customer in bc|stays in bc|remains in bc)", text):
        result["destination"] = "BC"

    # --- TITLE TRANSFER LOCATION ---
    if "title transfers outside bc" in text:
        result["title_transfer_location"] = "OUTSIDE BC"
    elif "title transfers in bc" in text or "sold in bc" in text or "selling in bc" in text:
        result["title_transfer_location"] = "BC"

    # --- PARSER WARNING for vague phrases ---
    if "operations" in text and not result.get("use_case"):
        result["parser_warning"] = "⚠️ The phrase 'operations' is too vague. Please specify if this is engine use, heating, resale, or export."

    # --- DEFAULT FALLBACKS ---
    if not result["destination"]:
        result["destination"] = "BC"
    if not result["title_transfer_location"]:
        result["title_transfer_location"] = "BC"

    return result


# --- Example usage ---
if __name__ == "__main__":
    example = """
    I am selling propane in BC to a customer in BC who is using it in a machine.
    """
    parsed = parse_fuel_tax_input(example)
    for key, value in parsed.items():
        print(f"{key}: {value}")
