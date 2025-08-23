from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import numpy as np
import logging

model_checkpoint = "jsylee/scibert_scivocab_uncased-finetuned-ner"
label_mapping = {
    "DRUG": "Chemical Substances",
    "ADVERSE EFFECT": "Medical Conditions",
    "PER": "Person",
    "LOC": "Location",
    "DATE": "Date",
    "ORG": "Organization",
    "CHEMICAL": "Chemical",
    "DISEASE": "Disease",
    "MISC": "Miscellaneous"
}

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

def jsylee_scibert_scivocab_uncased_finetuned_ner(text):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=5, id2label={0: 'O', 1: 'DRUG', 2: 'DRUG', 3: 'ADVERSE EFFECT', 4: 'ADVERSE EFFECT'})
        ner_pipeline = pipeline(task="ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
        
        results = ner_pipeline(text)
        entity_groups = {}
        tagging = []  # Initialize the tagging list
        
        for result in results:
            label = model.config.id2label.get(result["entity_group"], result["entity_group"])
            entity = {
                "text": result["word"],
                "score": result["score"]
            }
            if "index" in result:
                entity["index"] = result["index"]
            if label not in entity_groups:
                entity_groups[label] = []
            entity_groups[label].append(entity)
            
            # Add tagging information
            tagging.append({"text": result["word"], "tag": label})
        
        native_entity_groups = convert_to_native(entity_groups)
        
        output = {
            "entities": tagging,
            "entity_groups": list(native_entity_groups.keys())
        }
        
        return output

    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")
        return {"error": "The NER pipeline encountered an error and could not process the text."}

