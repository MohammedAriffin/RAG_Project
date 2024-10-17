from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Load the LLaMA 2 7B model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,  # Use float16 to save memory
    device_map="auto"  # Automatically distribute the model across available GPUs
).to("cuda")

# Example input text
input_text = "Once upon a time"

# Tokenize the input text
input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cuda")

# Generate output using the model
with torch.no_grad():
    output = model.generate(input_ids, max_length=50)

# Decode and print the output
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
