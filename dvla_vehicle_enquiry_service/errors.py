"""Errors for the DVLA Vehicle Enquiry Service API"""

from typing import Any, Optional


class VehicleEnquiryError(Exception):
    """Custom exception for vehicle enquiry errors, encapsulating error details."""

    def __init__(
        self,
        title: str,
        status: Optional[int] = None,
        code: Optional[str] = None,
        detail: Optional[str] = None,
        errors: Optional[list[dict[str, Any]]] = None,
    ):
        # Support both error dict and list[dict] of errors
        if errors:
            # Convert multiple error details into a string
            error_messages = " ; ".join(
                f"[{error.get('status')}] {error.get('title')}: {error.get('detail') or 'No details'}"
                for error in errors
            )
            super().__init__(f"Multiple errors occurred: {error_messages}")
        else:
            # Handle a single error
            super().__init__(f"[{status}] {title}: {detail or 'No details'}")

        self.title = title
        self.status = status
        self.code = code
        self.detail = detail
        self.errors = errors or []
