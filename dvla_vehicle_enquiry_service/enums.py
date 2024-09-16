"""Enumerations for DVLA Vehicle Enquiry Service API"""

from enum import Enum


class TaxStatus(Enum):
    """Enumeration for the tax status of a vehicle."""

    NOT_TAXED = "Not Taxed for on Road Use"
    SORN = "SORN"
    TAXED = "Taxed"
    UNTAXED = "Untaxed"


class MotStatus(Enum):
    """Enumeration for the MOT status of a vehicle."""

    NO_DETAILS_HELD = "No details held by DVLA"
    NO_RESULTS_RETURNED = "No results returned"
    NOT_VALID = "Not valid"
    VALID = "Valid"
