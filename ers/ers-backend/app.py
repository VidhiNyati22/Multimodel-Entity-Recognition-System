from flask import Flask, request, jsonify, session
from flask_cors import CORS

from utils.chemical_disease_model import ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased
from utils.jsylee_scibert_model import jsylee_scibert_scivocab_uncased_finetuned_ner
from utils.keyphrase_model import extractor
from utils.gliner_model import EmergentMethods_gliner_medium_news_v2_1
from utils.fran_scibert_model import fran_martinez_scibert_scivocab_cased_ner_jnlpba
from utils.gpt2_model import openai_community_gpt2
from utils.dmis_biobert_model import dmis_lab_biobert_v1_1
from utils.bert_base_NER_model import dslim_bert_base_NER
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt, verify_jwt_in_request
from datetime import timedelta
from functools import wraps
import numpy as np
import logging
import secrets
import string

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Needed for session management
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
blacklist = set()

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

users = {}

def generate_random_string(length = 8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "An unexpected error occurred"}), 500

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def handle_400(e):
    logging.info(f"Bad request: {str(e)}")
    return jsonify({"error": "Bad request"}), 400

@app.route('/register', methods=['POST'])
def register():
    username = generate_random_string()
    password = generate_random_string()
    users[username] = password
    session['login_attempts'] = 0
    return jsonify({"username": username, "password": password}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    if users.get(username) == password:
        session['login_attempts'] = 0  # Reset the counter on successful login
        ip_address = request.remote_addr
        logger.info(f"Login IP: {ip_address}")
        additional_claims = {"ip": ip_address}
        access_token = create_access_token(identity=username, additional_claims=additional_claims)
        return jsonify(access_token=access_token)

    session['login_attempts'] += 1

    if session['login_attempts'] >= 3:
        return jsonify({"msg": "Please log in again"}), 401

    return jsonify({"msg": "Incorrect username or password"}), 401

def ip_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        #print(get_jwt())
        token_ip = get_jwt()["ip"]
        print(token_ip)
        request_ip = request.remote_addr
        logger.info(f"Token IP: {token_ip}, Request IP: {request_ip}")
        if token_ip != request_ip:
            logger.warning("IP address mismatch. Logging out.")
            response = jsonify({"msg": "Token does not match. Logged out."})
            unset_jwt_cookies(response)
            return response, 401
        return fn(*args, **kwargs)
    return wrapper

@app.route('/protected', methods=['GET'])
@jwt_required()
@ip_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
@ip_required
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    response = jsonify({"msg": "Logged out successfully"})
    unset_jwt_cookies(response)
    return response, 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

# Custom error handlers for JWT errors
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({"error": "Invalid token"}), 401

@jwt.invalid_token_loader
def invalid_token_response(callback):
    return jsonify({"msg" : "Invalid token"}), 401

@app.route("/ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased", methods=['POST', 'GET'])
@jwt_required()
@ip_required
def ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased_endpoint():
    try:
        text = request.get_json().get("text")
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        entities = ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased(text)
        print('entities:', entities)  # Log response for debugging
        return jsonify(entities)
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error processing text: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased has run")

@app.route('/jsylee_scibert_scivocab_uncased_finetuned_ner', methods=['POST'])
@jwt_required()
@ip_required
def jsylee_scibert_scivocab_uncased_finetuned_ner_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        entities = jsylee_scibert_scivocab_uncased_finetuned_ner(text)
        native_entities = convert_to_native(entities)
        return jsonify(native_entities)
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error processing text: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model jsylee_scibert_scivocab_uncased_finetuned_ner has run")

@app.route('/ml6team_keyphrase_extraction_kbir_inspec', methods=['POST'])
@jwt_required()
@ip_required
def ml6team_keyphrase_extraction_kbir_inspec_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        keyphrases = extractor.ml6team_keyphrase_extraction_kbir_inspec(text)
        return jsonify(convert_to_native(keyphrases))
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error extracting keyphrases: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model ml6team_keyphrase_extraction_kbir_inspec has run")

@app.route('/EmergentMethods_gliner_medium_news_v2_1', methods=['POST'])
@jwt_required()
@ip_required
def EmergentMethods_gliner_medium_news_v2_1_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        entities = EmergentMethods_gliner_medium_news_v2_1(text)
        return jsonify(convert_to_native(entities))
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error extracting terms: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model EmergentMethods_gliner_medium_news_v2_1 has run")

@app.route('/fran_martinez_scibert_scivocab_cased_ner_jnlpba', methods=['POST'])
@jwt_required()
@ip_required
def fran_martinez_scibert_scivocab_cased_ner_jnlpba_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        entities = fran_martinez_scibert_scivocab_cased_ner_jnlpba(text)
        return jsonify(convert_to_native(entities))
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error extracting entities: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model fran_martinez_scibert_scivocab_cased_ner_jnlpba has run")

@app.route('/openai_community_gpt2', methods=['POST'])
@jwt_required()
@ip_required
def openai_community_gpt2_endpoint():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        if not prompt:
            raise ValueError("Invalid input: 'prompt' field is required")
        generated_texts = openai_community_gpt2(prompt)
        return jsonify(convert_to_native(generated_texts))
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error generating text: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model openai_community_gpt2 has run")

@app.route('/dmis_lab_biobert_v1_1', methods=['POST'])
@jwt_required()
@ip_required
def dmis_lab_biobert_v1_1_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        entities = dmis_lab_biobert_v1_1(text)
        return jsonify(convert_to_native(entities))
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error extracting BioBERT entities: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model dmis_lab_biobert_v1_1 has run") 

@app.route('/dslim_bert_base_NER', methods=['POST'])
@jwt_required()
@ip_required
def dslim_bert_base_NER_endpoint():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            raise ValueError("Invalid input: 'text' field is required")
        entities = dslim_bert_base_NER(text)
        return jsonify(convert_to_native(entities))
    except ValueError as e:
        logging.info(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error extracting medical entities: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        logging.info("Model dslim_bert_base_NER has run") 

if __name__ == "__main__":
    app.run(debug=True)