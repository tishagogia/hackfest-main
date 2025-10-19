import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class SnowflakeCortexClient:
    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT").lower().strip()
        self.user = os.getenv("SNOWFLAKE_USER")
        self.pat_token = os.getenv("PERSONAL_ACCESS_TOKEN")
        
        self.base_url = f"https://{self.account}.snowflakecomputing.com"
        
        if not self.pat_token:
            raise ValueError("PERSONAL_ACCESS_TOKEN not set in .env file")

    def complete(self, model, messages, temperature=0.0, max_tokens=1024):
        """Call Cortex LLM inference endpoint - handles streaming SSE responses"""
        url = f"{self.base_url}/api/v2/cortex/inference:complete"
        
        headers = {
            "Authorization": f"Bearer {self.pat_token}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        response = requests.post(url, headers=headers, json=payload, stream=True)
        
        if response.status_code == 400:
            try:
                error_msg = response.json().get("message", response.text)
            except:
                error_msg = response.text
            if "unavailable in your region" in error_msg:
                raise Exception(f"Model unavailable. Enable cross-region inference in Snowflake: {error_msg}")
            raise Exception(f"400 Bad Request: {error_msg}")
        elif response.status_code == 401:
            raise Exception("401 Unauthorized: Check your Personal Access Token")
        elif response.status_code == 403:
            raise Exception("403 Forbidden: Check your token permissions")
        elif response.status_code == 404:
            raise Exception(f"404 Not Found: Check account identifier")
        elif response.status_code == 500:
            raise Exception(f"500 Server Error: {response.text}")
        elif response.status_code == 503:
            raise Exception("503 Service Unavailable: Snowflake Cortex service temporarily down")
        
        response.raise_for_status()
        
        # Parse Server-Sent Events (SSE) streaming response
        content = ""
        try:
            for line in response.iter_lines():
                if not line:
                    continue
                
                line = line.decode('utf-8') if isinstance(line, bytes) else line
                
                # SSE format: data: {...json...}
                if line.startswith('data: '):
                    json_str = line[6:]  # Remove 'data: ' prefix
                    try:
                        chunk = json.loads(json_str)
                        # Extract content from delta
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                content += delta["content"]
                    except json.JSONDecodeError:
                        pass
            
            return content
        except Exception as e:
            raise Exception(f"Error parsing streaming response: {str(e)}")

if __name__ == "__main__":
    client = SnowflakeCortexClient()
    result = client.complete("mistral-large2", [{"role": "user", "content": "test"}])
    print(result)