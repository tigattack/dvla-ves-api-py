"""API Endpoints for the DVLA Vehicle Enquiry Service"""

BASE_URLS = {
    "production": "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry",
    "test": "https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry",
}

VEHICLE_BY_REGISTRATION = "/v1/vehicles"
