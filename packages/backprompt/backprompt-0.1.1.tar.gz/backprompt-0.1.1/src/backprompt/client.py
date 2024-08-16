import httpx
from .prompt import Prompt

class BackpromptClient:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json',
        }

    def __repr__(self):
        return (
            f"<BackpromptClient(api_key=\{self.api_key[:5]}...\, api_url={self.api_url})>"
        )
    
    def _post(self, endpoint_id, data):
        url = f"{self.api_url}/{endpoint_id}"
        
        with httpx.Client() as client:
            response = client.post(url, json=data, headers=self.headers, follow_redirects=True, timeout=600)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    def _put(self, endpoint_id, data):
        url = f"{self.api_url}/{endpoint_id}"
        
        with httpx.Client() as client:
            response = client.put(url, json=data, headers=self.headers, follow_redirects=True, timeout=600)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    def _get(self, endpoint_id):
        url = f"{self.api_url}/{endpoint_id}"
        
        with httpx.Client() as client:
            response = client.get(url, headers=self.headers, follow_redirects=True, timeout=600)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
        
    def create_completion(self, prompt, prompt_vars):
        data = {
            'prompt_vars': prompt_vars
        }
        return self._post(f"prompts/{prompt.key}/completion", data)

    def solve_prompt(self, input_data, desired_output):
        data = {
            'input': input_data,
            'output': desired_output
        }
        response = self._post("prompts/solve", data)
        print(response)
        return Prompt(**response.get("prompt"))
    
    def deploy_prompt(self, prompt: Prompt) -> dict:
        response = self._post(f"prompts/{prompt.id}/deploy", {})
        prompt.endpoint_url = response.get("endpoint")
        return prompt
    
    def undeploy_prompt(self, prompt: Prompt) -> dict:
        self._post(f"prompts/{prompt.key}/undeploy", {})
        prompt.endpoint_url = None
        return prompt
    
    def list_versions(self, prompt: Prompt) -> dict:
        return self._get(f"prompts/{prompt.key}/list")
    
    def uptate_prompt(self, prompt: Prompt) -> dict:
        response = self._put(f"prompts/{prompt.id}", prompt.to_dict())
        return response
