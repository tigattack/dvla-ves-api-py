"""Data models for the DVLA Vehicle Enquiry Service API"""

from datetime import date
from typing import Optional, Union

from pydantic import field_validator
from pydantic.dataclasses import dataclass

from .enums import MotStatus, TaxStatus


@dataclass
class VehicleResponse:
    """Represents a vehicle's details as retrieved from the DVLA Vehicle Enquiry Service API.

    Attributes:
        registrationNumber: The registration number of the vehicle (required).
        taxStatus: The tax status of the vehicle.
        taxDueDate: Date of tax liability, used in calculating licence information.
        artEndDate: Additional Rate of Tax End Date.
        motStatus: The MOT status of the vehicle.
        motExpiryDate: The expiry date of the MOT.
        make: The make of the vehicle.
        monthOfFirstDvlaRegistration: Month of the first DVLA registration.
        monthOfFirstRegistration: Month of the first registration.
        yearOfManufacture: Year of manufacture of the vehicle.
        engineCapacity: Engine capacity in cubic centimetres.
        co2Emissions: CO2 emissions in grams per kilometre.
        fuelType: The fuel type of the vehicle.
        markedForExport: Whether the vehicle has been export marked.
        colour: The vehicle's colour.
        typeApproval: The vehicle's type approval category.
        wheelplan: The vehicle's wheel plan.
        revenueWeight: The vehicle's revenue weight.
        realDrivingEmissions: The vehicle's Real Driving Emissions class.
        dateOfLastV5CIssued: Date of the last V5C issued.
        euroStatus: Euro Status of the vehicle.
        automatedVehicle: Whether the vehicle is an Automated Vehicle (AV).
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
        """Parses a 'YYYY-MM' string format to a date with the first day of the month."""
        if value:
            if isinstance(value, date):
                return value
            try:
                year, month = map(int, value.split("-"))
                return date(year, month, 1)
            except ValueError:
                raise ValueError(f"Invalid date format for 'YYYY-MM': {value}")
        return None
