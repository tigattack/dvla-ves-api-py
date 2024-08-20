"""Client for DVLA Vehicle Enquiry Service API"""

from typing import Any, Dict, Literal, Optional, Union

import aiohttp
from pydantic import ValidationError

from .api import BASE_URLS, VEHICLE_BY_REGISTRATION
from .models import ErrorDetail, ErrorResponse, Vehicle


class VehicleEnquiryAPI:
    """DVLA Vehicle Enquiry Service API client"""

    def __init__(
        self, api_key: str, environment: Literal["production", "test"] = "production"
    ) -> None:
        if environment not in BASE_URLS:
            raise ValueError("Invalid environment. Choose 'production' or 'test'.")
        self.api_key = api_key
        self.base_url = BASE_URLS[environment]

    async def _make_request(
        self, endpoint: str, data: Dict[str, Any], correlation_id: Optional[str] = None
    ) -> Union[Dict[str, Any], ErrorResponse]:
        """Makes a request to the API and returns the response"""
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        if correlation_id:
            headers["X-Correlation-Id"] = correlation_id

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}{endpoint}", json=data, headers=headers
            ) as response:
                response_json: Dict[str, Any] = await response.json()
                if response.status == 200:
                    return response_json
                else:
                    if response_json.get("message"):
                        return ErrorResponse(
                            errors=[
                                ErrorDetail(
                                    status=str(response.status),
                                    title=response_json["message"],
                                )
                            ]
                        )
                    elif response_json.get("errors"):
                        return ErrorResponse(
                            errors=[
                                ErrorDetail(**error)
                                for error in response_json.get("errors", [])
                            ]
                        )
                    elif isinstance(response_json, list):
                        return ErrorResponse(
                            errors=[ErrorDetail(**error) for error in response_json]
                        )
                    raise ValueError(
                        f"Unexpected error response format (HTTP {response.status}): {response_json}"
                    )

    async def get_vehicle(
        self, registration_number: str, correlation_id: Optional[str] = None
    ) -> Union[Vehicle, ErrorResponse]:
        """Fetches vehicle details by registration number"""
        data = {"registrationNumber": registration_number}
        response = await self._make_request(
            VEHICLE_BY_REGISTRATION, data, correlation_id
        )

        if isinstance(response, dict):
            try:
                return Vehicle(**response)
            except ValidationError as e:
                raise ValueError(f"Invalid response format: {e}")
        return response
