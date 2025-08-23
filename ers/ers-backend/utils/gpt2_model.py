from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import numpy as np
import logging

model_checkpoint = 'openai-community/gpt2'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint)

text_generator = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer
)

def convert_to_native(obj):
    if isinstance(obj, dict):
        return {k: convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_native(i) for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def openai_community_gpt2(prompt, max_new_tokens=30, num_return_sequences=5):
    try:
        generated_texts = text_generator(prompt, max_new_tokens=max_new_tokens, num_return_sequences=num_return_sequences)
        
        # Create a dictionary to store generated texts by their labels
        entity_groups = {}
        tagging = [] 
        
        for i, result in enumerate(generated_texts):
            label = f"Generated Text {i+1}"
            entity = {
                'text': result['generated_text'],
                'score': convert_to_native(result.get('score', 0.0)) 
            }
            if label not in entity_groups:
                entity_groups[label] = []
            entity_groups[label].append(entity)
        
            tagging.append({"text": result['generated_text'], "tag": label})
        
        native_entity_groups = convert_to_native(entity_groups)
        
        output = {
            "tagging": tagging,
            "entity_groups": list(native_entity_groups.keys())
        }
        
        return output

    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")
        return {"error": "The text generation pipeline encountered an error and could not process the prompt."}