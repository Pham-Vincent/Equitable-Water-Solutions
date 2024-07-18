import React, { useEffect, useState } from 'react';
import './../css/teamPage.css';
import './../css/navbar.css'

const AboutUs = () => {
    const [persons, setPersons] = useState ([]);

    useEffect(() => {
        fetch('json/persons.json')
        .then(response => response.json())
        .then(json => setPersons(json))
        .catch(error => console.error('Error fetching data:', error));
    }, []);

    const returnCards = (persons) => {
        const columns = 3;
        const rows = [];

        for(let i = 0; i<persons.length; i+=columns) {
            const columnsHtml = [];
            for(let j = i; j < i + columns && j < persons.length; j++){
                const person = persons[j];
                columnsHtml.push(
                    <div className="column" key={j}>
                        <div className = "card">
                            <div className="image-container">
                                <img src={person.image} referrerPolicy="no-referrer" alt={person.name} style={{width: '50%', height: '50%'}}/>
                            </div>
                            <div className="mini-container">
                                <h2>{person.name}</h2>
                                <p className="title">{person.title}</p>
                                <p>{person.description}</p>
                            </div>
                        </div>
                    </div>
                );
            }
            rows.push(<div className="row" key={i}>{columnsHtml}</div>);
        }

        return rows;
    };

    return (
        <div className="contact-split-container">

        <div className="contact-top-content">
            <div className="top-content-text">
                <h1 id="line-1">Contact Us</h1>
                <p id="line-2">We would love to hear from you!</p>
                <p id="line-3">Please email us at emailaddress@gmail.com with any questions or concerns.</p>
            </div>
        </div>

        <div id="team-header">
            <h1>Meet The Team</h1>
        </div>
        <div className="container-aboutUs" id="cards-container">
            {returnCards(persons)}
        </div>
        </div>
    );
};

export default AboutUs;
