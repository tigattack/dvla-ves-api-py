"""Data models for the DVLA Vehicle Enquiry Service API"""

from datetime import date
from typing import Any, List, Optional, Union

from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass

from .enums import MotStatus, TaxStatus


@dataclass
class ErrorDetail:
    """
    Represents an individual error detail returned by the API

    Attributes:
        title: The error title
        status: The HTTP status code
        code: The error code
        detail: The error detail
    """

    title: str
    status: Optional[str] = None
    code: Optional[str] = None
    detail: Optional[str] = None


@dataclass
class ErrorResponse:
    """
    Represents an error response from the API

    Attributes:
        errors: A list of error details
    """

    errors: List[ErrorDetail] = Field(default_factory=list)


@dataclass
class Vehicle:
    """
    Represents a vehicle's details as retrieved from the DVLA Vehicle Enquiry Service API.

    Attributes:
        registrationNumber: The registration number of the vehicle (required).
        taxStatus: The tax status of the vehicle.
        taxDueDate: Date of tax liability, used in calculating licence information presented to the user.
        artEndDate: Additional Rate of Tax End Date, format: YYYY-MM-DD.
        motStatus: The MOT status of the vehicle.
        motExpiryDate: The expiry date of the MOT.
        make: The make of the vehicle.
        monthOfFirstDvlaRegistration: Month of the first DVLA registration.
        monthOfFirstRegistration: Month of the first registration.
        yearOfManufacture: Year of manufacture of the vehicle.
        engineCapacity: Engine capacity in cubic centimetres.
        co2Emissions: Carbon Dioxide emissions in grams per kilometre.
        fuelType: The fuel type (method of propulsion) of the vehicle.
        markedForExport: True if the vehicle has been export marked.
        colour: The colour of the vehicle.
        typeApproval: Vehicle Type Approval Category.
        wheelplan: Vehicle wheel plan.
        revenueWeight: Revenue weight in kilograms.
        realDrivingEmissions: Real Driving Emissions value.
        dateOfLastV5CIssued: Date of the last V5C issued.
        euroStatus: Euro Status (Dealer / Customer Provided for new vehicles).
        automatedVehicle: True if the vehicle is an Automated Vehicle (AV).
    """

    registrationNumber: str
    taxStatus: Optional[TaxStatus] = None
    taxDueDate: Optional[date] = None
    artEndDate: Optional[date] = None
    motStatus: Optional[MotStatus] = None
    motExpiryDate: Optional[date] = None
    make: Optional[str] = None
    monthOfFirstDvlaRegistration: Optional[date] = None
    monthOfFirstRegistration: Optional[date] = None
    yearOfManufacture: Optional[int] = None
    engineCapacity: Optional[int] = None
    co2Emissions: Optional[int] = None
    fuelType: Optional[str] = None
    markedForExport: Optional[bool] = None
    colour: Optional[str] = None
    typeApproval: Optional[str] = None
    wheelplan: Optional[str] = None
    revenueWeight: Optional[int] = None
    realDrivingEmissions: Optional[str] = None
    dateOfLastV5CIssued: Optional[date] = None
    euroStatus: Optional[str] = None
    automatedVehicle: Optional[bool] = None

    @field_validator(
        "monthOfFirstRegistration", "monthOfFirstDvlaRegistration", mode="before"
    )
    def parse_month(cls, value: Union[str, date]) -> Optional[date]:
        if value:
            if isinstance(value, date):
                return value
            else:
                try:
                    year = int(value.split("-")[0])
                    month = int(value.split("-")[1])
                    return date(year, month, 1)
                except ValueError:
                    raise ValueError(f"Invalid date format for 'YYYY-MM': {value}")
        return None
