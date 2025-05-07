# test_hybrid.py

import unittest
from parser import parse_fuel_tax_input
from bcmftrule import check_bc_fuel_tax_applicability

class TestHybridInterface(unittest.TestCase):

    def run_case(self, input_text, expected_taxable, expected_reason_fragment):
        parsed = parse_fuel_tax_input(input_text)
        taxable, reason = check_bc_fuel_tax_applicability(**parsed)
        self.assertEqual(taxable, expected_taxable)
        self.assertIn(expected_reason_fragment.lower(), reason.lower())

    def test_export_with_common_carrier(self):
        text = "We exported propane to Alberta using a common carrier and title transfers outside BC."
        self.run_case(text, False, "export confirmed with common carrier")

    def test_heating_in_zone_ii(self):
        text = "We sold propane for residential heating in Zone II with a heating certificate."
        self.run_case(text, False, "residential heating in eligible zone")

    def test_heating_in_zone_i(self):
        text = "Customer used propane for heating in Zone I and had a certificate."
        self.run_case(text, True, "heating exemption invalid due to zone")

    def test_engine_use_regular(self):
        text = "Diesel was sold to an end user in BC for use in a truck engine."
        self.run_case(text, True, "fuel used in engine")

    def test_farm_use_without_certificate(self):
        text = "Propane was sold to a farmer for farm use but they didn’t give us a certificate."
        self.run_case(text, True, "no farm use certificate")

    def test_valid_resale(self):
        text = "Propane sold to a registered reseller with a resale certificate."
        self.run_case(text, False, "valid resale")

    def
