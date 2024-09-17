# DVLA Vehicle Enquiry Service Python SDK

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tigattack/dvla-ves-api-py/test.yml?branch=main&style=for-the-badge&logo=github&label=test)
![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/dvla-vehicle-enquiry-service?style=for-the-badge&logo=python&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdvla-vehicle-enquiry-service)
![PyPI - Version](https://img.shields.io/pypi/v/dvla-vehicle-enquiry-service?style=for-the-badge&logo=python&link=https%3A%2F%2Fpypi.org%2Fproject%2Fdvla-vehicle-enquiry-service)

`dvla_vehicle_enquiry_service` is a Python SDK providing a simple interface for interacting with the DVLA (Driver and Vehicle Licensing Agency) Vehicle Enquiry Service API. It allows retrieval of detailed vehicle information based on the registration number, including tax status, MOT status, and more.

## Installation

Install the package using pip:

```
pip install dvla_vehicle_enquiry_service
```

## Usage

### Initialisation

To use the `VehicleEnquiryAPI` class, you'll need an API key provided by the DVLA service. You can also specify the environment as either `production` or `test` (default is `production`).

```python
from dvla_vehicle_enquiry_service import VehicleEnquiryAPI

api_key = "your_api_key"

# Initialise client using the default ('production') API
client = VehicleEnquiryAPI(api_key)

# Or initialise client using the test API
client = VehicleEnquiryAPI(api_key, environment="test")
```

### Fetch Vehicle Details by Registration

To fetch vehicle details using its registration number:

```python
import asyncio
from dvla_vehicle_enquiry_service import VehicleResponse, VehicleEnquiryError

async def get_vehicle_details():
    response = await api.get_vehicle("AA19MOT")
    mot_status = response.motStatus.value if response.motStatus else "Unknown"
    print(f"Vehicle Make: {response.make}, MOT Status: {mot_status}")

asyncio.run(get_vehicle_details())
```

If the request is successful, this example will print something such as: `Vehicle Make: AUDI, MOT Status: Valid`.

### Error Handling

Errors are raised as `VehicleEnquiryError` exceptions. You can catch and handle these exceptions to access detailed error information.

```python
try:
    response = await client.get_vehicle("ER19NFD")
except VehicleEnquiryError as e:
    print(f"Error {e.status}: {e.title} - {e.detail}")
```

## Classes and Data Structures

### Vehicle Class

- `VehicleResponse`: Represents detailed information about a vehicle, including tax status, MOT status, make, model, and various other attributes.

### Error Handling Classes

- `VehicleEnquiryError`: Exception class that encapsulates error information, including status codes and error details.

### Enum Classes

- `TaxStatus`: Enumerates possible tax statuses of a vehicle (`TAXED`, `UNTAXED`, `SORN`, etc.).
- `MotStatus`: Enumerates possible MOT statuses of a vehicle (`VALID`, `NOT_VALID`, `NO_DETAILS_HELD`, etc.).

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
