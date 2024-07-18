import React from 'react';
import PropTypes from 'prop-types';
import './../css/teamPage.css';

const Card = ({ person }) => {
  return (
    <div className="column">
      <div className="card">
        <div className="image-container">
          <img src={person.image} referrerPolicy="no-referrer" alt={person.name} style={{ width: '50%', height: '50%' }} />
        </div>
        <div className="mini-container">
          <h2>{person.name}</h2>
          <p className="title">{person.title}</p>
          <p>{person.description}</p>
        </div>
      </div>
    </div>
  );
};

Card.propTypes = {
  person: PropTypes.shape({
    image: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
  }).isRequired,
};

export default Card;
