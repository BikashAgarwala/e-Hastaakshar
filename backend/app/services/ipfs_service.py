import json
import requests
from app.core.config import settings


class IPFSService:

    def __init__(self):
        self.base_url = "https://api.pinata.cloud/pinning"
        self.headers = {
            "pinata_api_key": settings.PINATA_API_KEY,
            "pinata_secret_api_key": settings.PINATA_SECRET_KEY
        }

    def upload_json_metadata(self, transaction_id: str, payload: dict) -> str:
        url = f"{self.base_url}/pinJSONToIPFS"
        body = {
            "pinataMetadata": {
                "name": f"Transaction_{transaction_id}",
                "keyvalues": {
                    "type": "e-hastaakshar-signature"
                }
            },
            "pinataContent": payload
        }

        try:
            response = requests.post(url, json=body, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            ipfs_hash = result.get("IpfsHash")

            print(f"[IPFS] Successfully pinned. CID: {ipfs_hash}")
            return ipfs_hash

        except requests.exceptions.RequestException as e:
            print(f"[IPFS ERROR] Failed to upload JSON: {str(e)}")
            return None

    def generate_public_url(self, cid: str) -> str:
        return f"https://gateway.pinata.cloud/ipfs/{cid}"


    def upload_file(self, file_bytes: bytes, filename: str) -> str:
        url = f"{self.base_url}/pinFileToIPFS"

        files = {
            'file': (filename, file_bytes)
        }

        metadata = json.dumps({"name": f"{filename}"})
        data = {"pinataMetadata": metadata}

        try:
            response = requests.post(url, files=files, data=data, headers=self.headers)
            response.raise_for_status()

            result = response.json()
            return result.get("IpfsHash")

        except requests.exceptions.RequestException as e:
            print(f"[IPFS FILE UPLOAD ERROR] {str(e)}")
            return None


ipfs_client = IPFSService()