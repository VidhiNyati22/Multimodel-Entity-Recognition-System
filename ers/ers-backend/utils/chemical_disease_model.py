from transformers import pipeline
import numpy as np
import logging


model_checkpoint = "ghadeermobasher/BC5CDR-Chemical-Disease-balanced-scibert_scivocab_cased"
label_mapping = {
    "CHEMICAL": "Chemical Substances",
    "DISEASE": "Medical Conditions",
    "PER": "Person",
    "LOC": "Location",
    "MISC" : "Miscellaneous",
    "PERSON": "Person",
    "ORG": "Organization"
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

def ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased(text):
    try:
        ner_pipeline = pipeline(task="ner", model=model_checkpoint)
        results = ner_pipeline(text)
        
        entity_groups = {}
        tagging = []  
        
        for result in results:
            label = label_mapping.get(result["entity"], result["entity"])
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