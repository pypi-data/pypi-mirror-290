from pydantic import Field, BaseModel
import requests

headers={
    "Content-Type": "application/json",
    }

def pack_gen(url, payload, request):
    payload.update({"prompt": request})
    url = f"{url}/api/generate"
    return url, payload

def pack_em(url, payload, request):
    payload.update({"input": request})
    url = f"{url}/api/embed"
    return url, payload

def pack_chat(url, payload, request):
    """\
    "messages": [
        {
            "role": "user",
            "content": "why is the sky blue?"
        },
        {
            "role": "assistant",
            "content": "due to rayleigh scattering."
        },
        {
            "role": "user",
            "content": "how is that different than mie scattering?"
        }
    ]
    """
    payload.update({"messages": request})
    url = f"{url}/api/chat"
    return url, payload



class OllamaLLM(BaseModel):
    """
    Ref1: https://dev.to/jayantaadhikary/using-the-ollama-api-to-run-llms-and-generate-responses-locally-18b7
    
    Ref2: https://medium.com/@shmilysyg/setup-rest-api-service-of-ai-by-using-local-llms-with-ollama-eb4b62c13b71

    Ref3: https://github.com/ollama/ollama/blob/main/docs/api.md
    """
    base_url:str = Field(default="http://localhost:11434", description="end point")
    model:str = Field(default="llama3.1", description="model name")
    stream:bool = Field(default=False)
    temperature:float = Field(default=0)
    type:str = Field(default="gen", description="gen, chat, embeddings")

    def __call__(self, request):
        return self.forward(request)
    
    def forward(self, request):
        payload = {
            "model": self.model,
            "stream": self.stream,
            "options": {
                "temperature": self.temperature
            },
        }
        url = self.base_url
        if self.type=="gen":
            url, payload= pack_gen(url=url, payload=payload, request=request)
        elif self.type=="embeddings":
            url, payload= pack_em(url=url, payload=payload, request=request)
        elif self.type=="chat":
            url, payload= pack_chat(url=url, payload=payload, request=request)
        else:
            raise ValueError("Other type of models are not implmented yet.")
        
        response = requests.post(url=url, headers=headers, json=payload)
        response = response.json()
        
        if self.type=="gen":
            return response["response"] 
        elif self.type=="embeddings":
            return response["embeddings"]
        else:
            raise ValueError("Other type of models are not implmented yet.")