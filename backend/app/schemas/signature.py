from pydantic import BaseModel, Field, IPvAnyAddress, field_validator
from typing import Optional
from datetime import datetime
import re


class GeoLocation(BaseModel):
    latitude: float = Field(..., description="GPS Latitude")
    longitude: float = Field(..., description="GPS Longitude")
    accuracy: float = Field(..., description="Accuracy radius in meters")
    altitude: Optional[float] = None


class DeviceMetadata(BaseModel):
    device_id: str = Field(..., description="Unique hardware ID from the Android device")
    mac_address: str = Field(..., description="MAC Address for hardware binding checks")
    ip_address: IPvAnyAddress = Field(..., description="Client IP address")
    os_version: str = Field(..., example="Android 14")
    is_rooted: bool = Field(False, description="Security flag: is the device rooted?")

    @field_validator('mac_address')
    @classmethod
    def validate_mac_address(cls, v: str) -> str:
        # Regex to validate standard MAC address format (00:1A:2B:3C:4D:5E)
        if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", v):
            raise ValueError('Invalid MAC address format')
        return v


class BiometricEvidence(BaseModel):

    signature_image_b64: str = Field(..., description="Base64 encoded PNG/JPG of the signature")
    front_camera_image_b64: str = Field(..., description="Base64 encoded selfie taken at moment of signing")
    fingerprint_hash: Optional[str] = None


class SignatureSubmission(BaseModel):
    user_id: str = Field(..., description="UUID of the registered user")
    document_id: str = Field(..., description="ID of the document being signed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: GeoLocation
    device_info: DeviceMetadata
    evidence: BiometricEvidence

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "user_123456",
                "document_id": "doc_987654",
                "timestamp": "2025-10-24T10:00:00Z",
                "location": {
                    "latitude": 28.6139,
                    "longitude": 77.2090,
                    "accuracy": 10.5
                },
                "device_info": {
                    "device_id": "android_secure_id_xyz",
                    "mac_address": "00:1B:44:11:3A:B7",
                    "ip_address": "192.168.1.5",
                    "os_version": "Android 14",
                    "is_rooted": False
                },
                "evidence": {
                    "signature_image_b64": "iVBORw0KGgoAAAANSUhEUgAA...",
                    "front_camera_image_b64": "/9j/4AAQSkZJRgABAQ..."
                }
            }
        }
    }


class SignatureResponse(BaseModel):
    transaction_id: str
    status: str = Field(..., example="PENDING_VERIFICATION")
    message: str
    estimated_wait_time_seconds: int = 5