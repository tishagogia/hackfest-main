import os
import jwt
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Load environment variables like SNOWFLAKE_ACCOUNT etc.
load_dotenv()

class SnowflakeCortexClient:
    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = os.getenv("SNOWFLAKE_USER")
        self.base_url = f"https://{self.account}.snowflakecomputing.com"
        self.private_key_path = os.getenv("PRIVATE_KEY_PATH")
        self.private_key = self._load_private_key()

    def _load_private_key(self):
        with open(self.private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    def _generate_jwt_token(self):
        now = datetime.utcnow()
        payload = {
            "iss": f"{self.account.upper()}.{self.user.upper()}",
            "sub": self.user.upper(),
            "iat": now,
            "exp": now + timedelta(hours=1),
        }
        token = jwt.encode(payload, self.private_key, algorithm="RS256")
        return token

    def complete(self, model, messages, temperature=0.0, max_tokens=1024):
        token = self._generate_jwt_token()
        url = f"{self.base_url}/api/v2/cortex/inference:complete"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

# Example usage when run as main
if __name__ == "__main__":
    client = SnowflakeCortexClient()
    prompt = [{"role": "user", "content": "Say 'Hello from Snowflake Cortex!'"}]
    print(client.complete("claude-4-sonnet", prompt))
