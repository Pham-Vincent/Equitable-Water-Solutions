import React from 'react';
import './../css/teamPage.css';
import './../css/navbar.css';
import CardsContainer from '../components/CardsContainer.js';

const AboutUs = () => {
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
        <CardsContainer />
        </div>
    );
};

export default AboutUs;
