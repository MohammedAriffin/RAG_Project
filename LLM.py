from transformers import LlamaForCausalLM, LlamaTokenizer

model_path = "meta-llama/Llama-3.2-3B"
tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(model_path, device_map="auto", load_in_8bit=True)  # Optimized loading

# Example input
input_text = "What are the benefits of using AI for document retrieval?"

# Tokenize input
inputs = tokenizer(input_text, return_tensors="pt").to('cuda')
outputs = model.generate(inputs['input_ids'], max_length=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
