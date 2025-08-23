import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './output.css';
import logo from './logo.svg';

const Output = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { text = '', entities = [], entity_groups = [] } = location.state || {};
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [highlightedText, setHighlightedText] = useState(' ');

  useEffect(() => {
    // console.log('Text:', text);
    // console.log('entities:', entities);
    // console.log('Entity Groups:', entity_groups);
    if (entities) {
      highlightEntities();
    }
  }, [text, entities, selectedEntity]);

  const highlightEntities = () => {
    // console.log('Highlighting entities...');
    let result = text;
    let offset = 0;

    entities.forEach((entity) => {
      console.log(entity) //TODO
      const { text: entityText, tag } = entity;
      

      if (tag) {
      const color = getColorForEntity(tag);

      // if (!selectedEntity || selectedEntity === tag) {
        const cleanedEntityText = entityText.replace(/^##/, '');
        let index = result.indexOf(cleanedEntityText, offset);

      //   while (index !== -1) {
      //     const before = result.slice(0, index);
      //     console.log(entity)
      //     continue;
      //     const after = result.slice(index + cleanedEntityText.length);
      //     result = `${before}<span class="highlight" style="background-color: ${color};">${cleanedEntityText}</span>${after}`;
      //     offset = index + cleanedEntityText.length + 39; // 39 is the length of the span tag
      //     index = result.indexOf(cleanedEntityText, offset);
      // }
    }
    });
   setHighlightedText(result);
  };

  
  const getColorForEntity = (tag) => {
    // console.log(typeof(entity))
   // if (typeof(entity) === 'string') { 

    switch (tag) {
      case 'B-Chemical': return '#dbba7c';
      case 'I-Chemical': return '#ffa500'; // Orange
      case 'B-Disease':  return '#87cefa';
      case 'I-Disease': return '#457ea1ea'; // Light Blue
      case 'DRUG': return '#90ee90'; // Light Green
      case 'Keyphrase': return '#ff69b4'; // Hot Pink
      case 'PERSON': return '#ffd700'; // Gold
      case 'ORGANIZATION': return '#ff4500'; // OrangeRed
      case 'LOCATION': return '#1e90ff'; // Dodger Blue
      case 'ADVERSE EFFECT': return '#8f5d548f'; // Tomato
      case 'LABEL_1': return '#d3d3d3'
      case 'LABEL_0': return '#cea8a8'
      case 'Miscellaneous': return '#927878'; // Light Gray
      default: return '#c5c5c5'; // Default Color
    }
   
 };

  const handleEntityClick = (entity) => {
    setSelectedEntity(selectedEntity === entity ? null : entity);
  };
  
  const getEntityDisplayName = (tag) => {
    if (typeof tag === 'string') {
    const parts = tag.split('-');
    return parts[parts.length - 1];
    
  }
  return '';
 };


  return (
    <div className="container">
      <div className="header">
        <div className="logo-container">
          <img src={logo} className="logo" alt="logo" />
          <div className="company-name">EVERSANA</div>
        </div>
      </div>
      <div className="content">
        <div className="output-box">
          <h3>Output</h3>
          <div 
            className="text-output" 
            dangerouslySetInnerHTML={{ __html: highlightedText }}
          />
        </div>
        <div className="entity-list-container">
        <div className="entity-list">
          <h2>ENTITY LIST</h2>
          <ul>
          {entity_groups.map((group, index) => (
              <li 
                key={index} 
                onClick={() => handleEntityClick(group)}
                style={{ cursor: 'pointer', fontWeight: selectedEntity === group ? 'bold' : 'normal' }}
              >
                <span className="dot" style={{ backgroundColor: getColorForEntity(group) }}></span>
                <span>{getEntityDisplayName(group)}</span>
              </li>
            ))}
          </ul>
        </div>
        </div>
        <button className="back-button" onClick={() => navigate('/')}>Back to Home</button>
      </div>
    </div>
  );
};

export default Output;