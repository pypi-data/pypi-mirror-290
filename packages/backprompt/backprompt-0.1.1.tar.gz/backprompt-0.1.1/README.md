# Backprompt: AI Integration, Simplified

Tailor LLM outputs to your exact needs, no datasets or finetuning required.

## Installation

```bash
pip install backprompt
```

## Usage
#### Step 1: Solve for an optimal prompt
```python
from backprompt import BackpromptClient

# Initialize the client
client = BackpromptClient(
    api_key='[your-api-key]', 
    api_url='[your-api-url]'
)


input_text = "The new smartphone boasts a 108MP camera and 5G capability."
desired_output = """
🌟 Tech Specs Breakdown 🌟
📸 Camera: 108MP (Ultra High-Res)
📡 Connectivity: 5G-enabled
💡 Key Benefit: Pro-level photography with lightning-fast uploads
"""

optimal_prompt = client.solve_prompt(input_text, desired_output)
print(f"Optimal prompt: {optimal_prompt}")
```

#### Step 2: Deploy the optimal prompt
```python
optimal_prompt.deploy(client)
```

#### Step 3: Generate using the deployed prompt
```python
prompt_vars = {"input_data": "The latest smartwatch features a 1.4-inch AMOLED display and 7-day battery life."}
completion = optimal_prompt.run(client, prompt_vars)

print(f"Generated response: {completion}")
```

## Key Features

1. **Prompt Optimization**: Generate optimal prompts based on input-output pairs.
2. **Prompt Deployment**: Deploy optimized prompts for quick access.
3. **Response Generation**: Generate responses using deployed prompts.

## Backprompt's Edge for Developers

- Prompt Engineering, Automated
- Rapid Iteration Cycle
- Model-Agnostic Customization
- Resource Efficiency

## Backprompt Across Domains

- Nuanced Sentiment Extraction
- Specialized Knowledge Base Q&A
- Consistent Code Snippet Generation

For more information, visit [backprompt.ai](https://backprompt.ai)

© 2024 backprompt