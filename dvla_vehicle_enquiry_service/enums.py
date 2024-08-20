"""Enumerations for DVLA Vehicle Enquiry Service API"""

from enum import Enum


class TaxStatus(Enum):
    NOT_TAXED = "Not Taxed for on Road Use"
    SORN = "SORN"
    TAXED = "Taxed"
    UNTAXED = "Untaxed"


class MotStatus(Enum):
    NO_DETAILS_HELD = "No details held by DVLA"
    NO_RESULTS_RETURNED = "No results returned"
    NOT_VALID = "Not valid"
    VALID = "Valid"
