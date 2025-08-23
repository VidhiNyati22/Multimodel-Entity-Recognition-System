import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css';
import logo from './logo.svg'; 
import axios from 'axios';


const Home = () => {
  const [inputText, setInputText] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleGetOutput = async () => {
    try {
      setError(null);
      setIsLoading(true);
    
      const response = await axios.post(`http://localhost:5000/${selectedModel}`, {
        text: inputText
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      const data = response.data;
      

      console.log('API Response:', data);

      // Adjust based on your API response structure
    navigate('/output', { 
      state: { 
        text: inputText,
        entities: data.tagging , // Adjust according to response
        entity_groups: data.entity_groups || [] // Adjust according to response
        } 
      });
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while processing your request. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <div className="logo-container">
          <img src={logo} className="logo" alt="logo" />
          <div className="company-name">EVERSANA</div>
        </div>
        <button className="sign-up">SIGN UP</button>
      </header>
      <main className="main-content">
        <div className="content-wrapper">
          <div className="left-side">
            <h3>Enter Text Here</h3>
            <textarea 
              className="text-input" 
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
          </div>
          <div className="right-side">
            <div className="model-list-container">
            <div className="model-list">
              <h3>MODEL LIST</h3>
              <div className="model-options">
              <select 
                  value={selectedModel} 
                  onChange={(e) => setSelectedModel(e.target.value)}
                >
                  <option value="">Select a model</option>
                  <option value="ghadeermobasher_BC5CDR_Chemical_Disease_balanced_scibert_scivocab_cased">Chemical Disease Model</option>
                  <option value="jsylee_scibert_scivocab_uncased_finetuned_ner">SciBERT NER</option>
                  <option value="ml6team_keyphrase_extraction_kbir_inspec">Keyphrase Extraction</option>
                  <option value="EmergentMethods_gliner_medium_news_v2_1">gliner_model</option>
                  <option value="fran_martinez_scibert_scivocab_cased_ner_jnlpba">SciBERT NER JNLPBA</option>
                  <option value="openai_community_gpt2">GPT-2</option>
                  <option value="dmis_lab_biobert_v1_1">BioBERT</option>
                  <option value="dslim_bert_base_NER">BERT Base NER</option>
                </select>
                {error && <div className="error-message">{error}
              </div>}
              {isLoading && <div className="loading-message">Processing your request...
            </div>}
            </div>
            <button 
              className="get-output" 
              onClick={handleGetOutput}
              disabled={!inputText || !selectedModel}
            >
             {isLoading ? 'Processing...' : 'Get Output'}
            </button>
            </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;