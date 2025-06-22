from llama_cpp import Llama
import os

# Adjust path to your actual model
MODEL_PATH = os.path.join("models", "mistral-7b-instruct-v0.1.Q4_K_M.gguf")

# Init only once
llm = Llama(
    model_path="C:/Users/Prakhar Srivastava/Desktop/PROJECTS/BlindNav/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4,
    n_gpu_layers=0  # 0 if CPU-only
)

def generate_local_response(prompt: str) -> str:
    full_prompt = f"[INST] {prompt.strip()} [/INST]"
    
    response = llm(
        prompt=full_prompt,
        max_tokens=512,
        stop=["</s>"],
        echo=False,
        temperature=0.7,
        top_p=0.95
    )
    
    return response['choices'][0]['text'].strip()
