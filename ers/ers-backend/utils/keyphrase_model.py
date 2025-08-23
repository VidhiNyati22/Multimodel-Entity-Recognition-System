from transformers import (
    pipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)
import numpy as np
import logging
#TODO

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

model_checkpoint = "ml6team/keyphrase-extraction-kbir-inspec"
label_mapping = {
    "B-PER": "Person",
    "I-PER": "Person",
    "B-DISEASE": "Medical Conditions",
    "I-DISEASE": "Medical Conditions",
    "B-LOC": "Location",
    "I-LOC": "Location",
    "B-ORG": "Organization",
    "I-ORG": "Organization",
    "B-DRUG": "Drug",
    "I-DRUG": "Drug",
    "B-ADVERSE_EFFECT": "Adverse Effect",
    "I-ADVERSE_EFFECT": "Adverse Effect",
    "B-MISC": "Miscellaneous",
    "I-MISC": "Miscellaneous",
    "B-KEY": "Keyphrase",
    "I-KEY": "Keyphrase"
}

class KeyphraseExtractionPipeline:
    def __init__(self, model):
        self.model = AutoModelForTokenClassification.from_pretrained(model)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.pipeline = pipeline(
            task="ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple"
        )

    def ml6team_keyphrase_extraction_kbir_inspec(self, text):  
        try:
            results = self.pipeline(text)
            
            # Create a dictionary to store tagging by their groups
            entity_groups = []
            tagging = [] 
            
            for result in results:
                label = label_mapping.get(result.get('entity'), 'Keyphrase')
                entity = {
                    'word': result.get('word', ''),
                    'score': convert_to_native(result.get('score', 0.0)),
                    'start': result.get('start', 0),
                    'end': result.get('end', 0)
                }
                if label not in entity_groups:
                    entity_groups[label] = []
                entity_groups[label].append(entity)
                
                # Add tagging information
                tagging.append({"text": result.get('word', ''), "tag": label})
                # convertpython arrayto json to send through response
                return {"tagging": tagging, "entity_groups": entity_groups}
            
            native_entity_groups = convert_to_native(entity_groups)
            
            entity_groups.append("keyphrase")
            output = {
                "entities": tagging,
                "entity_groups": entity_groups# list(native_entity_groups.keys())
            }
            
            return output
        except Exception as e:
            logging.error(f"Pipeline error: {str(e)}")
            return {"error": "The keyphrase extraction pipeline encountered an error and could not process the text."}

# Define keyphrase extraction pipeline
extractor = KeyphraseExtractionPipeline(model=model_checkpoint)