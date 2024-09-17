"""Client for DVLA Vehicle Enquiry Service API"""

from typing import Any, Literal, Optional

import aiohttp
from pydantic import ValidationError

from .api import BASE_URLS, VEHICLE_BY_REGISTRATION
from .errors import VehicleEnquiryError
from .models import VehicleResponse


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
        self, endpoint: str, data: dict[str, Any], correlation_id: Optional[str] = None
    ) -> dict[str, Any]:
        """Makes a request to the API and raises errors for any non-200 status."""
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        if correlation_id:
            headers["X-Correlation-Id"] = correlation_id

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}{endpoint}", json=data, headers=headers
            ) as response:
                response_json: dict[str, Any] = await response.json()

                if response.status == 200:
                    return response_json

                if response_json.get("message"):
                    raise VehicleEnquiryError(
                        status=response.status,
                        title=response_json["message"],
                    )

                if response_json.get("errors"):
                    raise VehicleEnquiryError(
                        status=response.status,
                        title="Multiple errors occurred during API request"
                        if len(response_json["errors"]) > 1
                        else "Error occurred during API request",
                        errors=[error for error in response_json.get("errors", [])],
                    )

        raise VehicleEnquiryError(
            status=response.status, title="Unknown error during API request"
        )

    async def get_vehicle(
        self, registration_number: str, correlation_id: Optional[str] = None
    ) -> VehicleResponse:
        """Fetches vehicle details.

        Args:
            registration_number: The vehicle registration number
            correlation_id: The correlation ID to include in the request headers
        Returns:
            VehicleResponse
        Raises:
            VehicleEnquiryError
        """
        data = {"registrationNumber": registration_number}
        response = await self._make_request(
            VEHICLE_BY_REGISTRATION, data, correlation_id
        )

        try:
            return VehicleResponse(**response)
        except ValidationError as e:
            raise VehicleEnquiryError(
                title="Invalid response format", detail=str(e)
            ) from e
