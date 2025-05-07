# hybrid_interface.py

from parser import parse_fuel_tax_input
from bcmftrule import check_bc_fuel_tax_applicability

def run_hybrid_interface():
    print("📦 BC Motor Fuel Tax Hybrid Interface")
    print("-------------------------------------")
    print("Enter a transaction description (natural language). Example:\n")
    print('"We sold propane to a registered reseller for export outside BC. Title transfers in Alberta and they provided a common carrier certificate."\n')

    while True:
        user_input = input("📝 Describe the transaction (or type 'exit' to quit):\n> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Parse the user's input
        parsed_data = parse_fuel_tax_input(user_input)

        print("\n🔍 Parsed transaction details:")
        for key, value in parsed_data.items():
            print(f"  {key}: {value}")

        # Check MFT applicability
        is_taxable, explanation = check_bc_fuel_tax_applicability(**parsed_data)

        print("\n⚖️ Tax Determination:")
        print(f"  ➤ MFT Applicable? {'Yes' if is_taxable else 'No'}")
        print(f"  ➤ Reason: {explanation}")
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    run_hybrid_interface()
