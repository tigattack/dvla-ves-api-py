from datetime import date
from os import environ

import pytest
from dateutil.relativedelta import relativedelta

from dvla_vehicle_enquiry_service import (
    ErrorResponse,
    MotStatus,
    TaxStatus,
    Vehicle,
    VehicleEnquiryAPI,
)


# Test with a known successful VRN
@pytest.mark.asyncio
async def test_get_vehicle_success() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    expected_vehicle = Vehicle(
        registrationNumber="AA19AAA",
        taxStatus=TaxStatus.TAXED,
        taxDueDate=date.today() + relativedelta(years=1),
        artEndDate=date(2025, 3, 30),
        motStatus=MotStatus.NO_DETAILS_HELD,
        make="FORD",
        monthOfFirstDvlaRegistration="2019-03",  # type: ignore
        monthOfFirstRegistration="2019-03",  # type: ignore
        yearOfManufacture=2019,
        engineCapacity=2000,
        co2Emissions=300,
        fuelType="PETROL",
        markedForExport=False,
        colour="RED",
        typeApproval="M1",
        wheelplan="2 AXLE RIGID BODY",
        revenueWeight=0,
        realDrivingEmissions="1",
        dateOfLastV5CIssued=date(2019, 5, 20),
        euroStatus="EURO1",
    )

    vehicle = await api.get_vehicle("AA19AAA")

    assert isinstance(vehicle, Vehicle)
    assert vehicle == expected_vehicle


# Test with a VRN that has a valid MOT
@pytest.mark.asyncio
async def test_get_vehicle_with_valid_mot() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    vehicle = await api.get_vehicle("AA19MOT")

    assert isinstance(vehicle, Vehicle)
    assert vehicle.motStatus == MotStatus.VALID
    assert vehicle.motExpiryDate == date.today() + relativedelta(years=1)


# Test with a VRN that has SORN status
@pytest.mark.asyncio
async def test_get_vehicle_with_sorn() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    vehicle = await api.get_vehicle("AA19SRN")

    assert isinstance(vehicle, Vehicle)
    assert vehicle.taxStatus == TaxStatus.SORN
    assert vehicle.taxDueDate is None


# Test with a VRN that is untaxed and nonstandard format
@pytest.mark.asyncio
async def test_get_vehicle_with_untaxed() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    vehicle = await api.get_vehicle("L2WPS")

    assert isinstance(vehicle, Vehicle)
    assert vehicle.registrationNumber == "L2WPS"
    assert vehicle.taxStatus == TaxStatus.UNTAXED
    assert vehicle.taxDueDate is not None
    assert vehicle.taxDueDate < date.today()


# Test with a VRN that should be rejected as invalid
@pytest.mark.asyncio
async def test_get_vehicle_bad_request() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    response = await api.get_vehicle("ER19BAD")

    assert isinstance(response, ErrorResponse)
    assert len(response.errors) == 1
    assert response.errors[0].status == "400"
    assert response.errors[0].title == "Bad Request"
    assert response.errors[0].detail is not None
    assert "Invalid format" in response.errors[0].detail


# Test with a VRN that should return a 404 error
@pytest.mark.asyncio
async def test_get_vehicle_not_found() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    response = await api.get_vehicle("ER19NFD")

    assert isinstance(response, ErrorResponse)
    assert len(response.errors) == 1
    assert response.errors[0].status == "404"
    assert response.errors[0].title == "Vehicle Not Found"


# Test with a VRN that should return a 429 error
@pytest.mark.asyncio
async def test_get_vehicle_too_many_requests() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    response = await api.get_vehicle("ER19THR")

    assert isinstance(response, ErrorResponse)
    assert len(response.errors) == 1
    assert response.errors[0].status == "429"
    assert response.errors[0].title == "Too Many Requests"


# Test with a VRN that should return a 500 error
@pytest.mark.asyncio
async def test_get_vehicle_internal_server_error() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    response = await api.get_vehicle("ER19ERR")

    assert isinstance(response, ErrorResponse)
    assert len(response.errors) == 1
    assert response.errors[0].status == "500"
    assert response.errors[0].title == "Internal Server Error"


# Test with a VRN that should return a 503 error
@pytest.mark.asyncio
async def test_get_vehicle_service_unavailable() -> None:
    api_key = environ.get("TEST_API_KEY")
    assert api_key is not None

    api = VehicleEnquiryAPI(api_key=api_key, environment="test")

    response = await api.get_vehicle("ER19MNT")

    assert isinstance(response, ErrorResponse)
    assert len(response.errors) == 1
    assert response.errors[0].status == "503"
    assert response.errors[0].title == "System currently down for maintenance"
