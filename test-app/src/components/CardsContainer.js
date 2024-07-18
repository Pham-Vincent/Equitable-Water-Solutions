import React, { useEffect, useState } from 'react';
import Card from './Card';
import './../css/teamPage.css';

const CardsContainer = () => {
  const [persons, setPersons] = useState([]);

  useEffect(() => {
    fetch('json/persons.json')
      .then(response => response.json())
      .then(json => setPersons(json))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const renderCards = () => {
    const columns = 3;
    const rows = [];

    for (let i = 0; i < persons.length; i += columns) {
      const columnsHtml = [];
      for (let j = i; j < i + columns && j < persons.length; j++) {
        const person = persons[j];
        columnsHtml.push(<Card key={j} person={person} />);
      }
      rows.push(<div className="row" key={i}>{columnsHtml}</div>);
    }

    return rows;
  };

  return (
    <div className="container-aboutUs" id="cards-container">
      {persons.length > 0 ? renderCards() : <p>Loading...</p>}
    </div>
  );
};

export default CardsContainer;
