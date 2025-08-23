from transformers import pipeline
import numpy as np
import logging
# TODO

ner_model = pipeline("ner", model="dmis-lab/biobert-v1.1")

label_mapping = {
    "B-PER": "Person",
    "I-PER": "Person",
    "B-LOC": "Location",
    "I-LOC": "Location",
    "B-ORG": "Organization",
    "I-ORG": "Organization",
    "B-MISC": "Miscellaneous",
    "I-MISC": "Miscellaneous",
    "B-DISEASE": "Disease",
    "I-DISEASE": "Disease",
    "B-DRUG": "Drug",
    "I-DRUG": "Drug",
    "B-AE": "Adverse Effect",
    "I-AE": "Adverse Effect"
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

def dmis_lab_biobert_v1_1(text):
    try:
        predictions = ner_model(text)
        entity_groups = {}
        tagging = [] 
        
        for prediction in predictions:
            label = label_mapping.get(prediction['entity'], prediction['entity'])
            entity = {
                'entity': label,
                'score': convert_to_native(prediction['score']),
                'index': prediction['index'],
                'start': prediction['start'],
                'end': prediction['end'],
                'word': prediction['word']
            }
            if label not in entity_groups:
                entity_groups[label] = []
            entity_groups[label].append(entity)
            
            tagging.append({"text": prediction['word'], "tag": label})
        
        native_entity_groups = convert_to_native(entity_groups)
        
        output = {
            "entities": tagging,
            "entity_groups": list(native_entity_groups.keys())
        }
        
        return output

    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")
        return {"error": "The BioBERT NER pipeline encountered an error and could not process the text."}