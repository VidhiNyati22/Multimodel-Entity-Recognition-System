from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import numpy as np
import logging
#TODO
model_checkpoint = 'fran-martinez/scibert_scivocab_cased_ner_jnlpba'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForTokenClassification.from_pretrained(model_checkpoint)

# Update tokenizer configuration
tokenizer.model_max_length = 512  
tokenizer.truncation = True       

nlp_ner = pipeline(
    task="ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

label_mapping = {
    "PER": "Person",
    "LOC": "Location",
    "ORG": "Organization",
    "DISEASE": "Medical Conditions",
    "DRUG": "Drug",
    "AE": "Adverse Effect",
    "CHEMICAL": "Chemical Substances",
    "DATE": "Date",
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

def fran_martinez_scibert_scivocab_cased_ner_jnlpba(text):
    try:
        lines = text.splitlines()
        tagging = []
        for line in lines:
            result = nlp_ner(line)
            for entity in result:
                tagging.append(entity)
        
        # Create a dictionary to store tagging by their groups
        entity_groups = {}
        tagging = [] 
        
        for entity in tagging:
            label = label_mapping.get(entity["entity_group"], entity["entity_group"])
            entity_info = {
                "text": entity["word"],
                "score": entity["score"]
            }
            if "index" in entity:
                entity_info["index"] = entity["index"]
            if label not in entity_groups:
                entity_groups[label] = []
            entity_groups[label].append(entity_info)
            
            tagging.append({"text": entity["word"], "tag": label})
        
        native_entity_groups = convert_to_native(entity_groups)
        
        output = {
            "entities": tagging,
            "entity_groups": list(native_entity_groups.keys())
        }
        
        return output
    
    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")
        return {"error": "The NER pipeline encountered an error and could not process the text."}
