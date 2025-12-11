import json
from app.main import app

openapi_data = app.openapi()

with open("openapi.json", "w") as f:
    json.dump(openapi_data, f, indent=4)

print("✅ OpenAPI schema generated successfully!")