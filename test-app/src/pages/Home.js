import React, { useState } from 'react';
import axios from 'axios';
import {Link} from 'react-router-dom';
import './../css/landingpage.css';
import './../css/background.css';


const HomePage = () => {
  const [profileData, setProfileData] = useState(null);

  const getData = () => {
    console.log("Button clicked, fetching data...");
    axios.get('/profile')
      .then((response) => {
        console.log("Response received:", response);
        const res = response.data;
        setProfileData({
          profile_name: res.name,
          about_me: res.about,
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  };

  return (
    <>
    <div className="split-content">
      <div className="area" >
        <ul className="circles">
          <li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>
        </ul>
      </div>
        <div className="page-content">
          <div>
            <h1>
              <span style={{fontStyle:'italic'}}>SaltCast </span> loading...
            </h1>
            <p style={{marginBottom: '30px'}}>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus imperdiet, nulla et dictum interdum, nisi lorem egestas odio, vitae scelerisque enim ligula venenatis dolor. Maecenas nisl est, ultrices nec congue eget, auctor vitae massa.</p>
            <p style={{fontStyle: 'italic', fontWeight: '800'}}>Meet the team on our <Link to="/Aboutus" style={{fontSize: 'larger'}}>Contact Us</Link> page.</p>
          </div>

          <img src="/images/SaltCastLogoGreen.svg"/>
          
        </div>

    <div className="bottom-content">
      <div style={{margin: '80px 100px 30px 100px'}}>
        <h1>Our Journey So Far...</h1>
        <p>Come check out some of our academic articles that helped shape the SaltCast journey.</p>
      </div>
      <div className="article-boxes">
          <div className="box-1">
            <img src="/images/article-icon.svg"/>
            <p>Article A: Name of Article and Details</p>
            <p id="article-description">A short description about the article, and how it fuelled the journey. A little bit more about the article and its content.</p>
            <button>Read Now</button>
          </div>
          <div className="box-2">
            <img src="/images/article-icon.svg"/>
            <p>Article B: Name of Article and Details</p>
            <p id="article-description">A short description about the article, and how it fuelled the journey. A little bit more about the article and its content.</p>
            <button>Read Now</button>
          </div>
          <div className="box-3">
            <img src="/images/article-icon.svg"/>
            <p>Article C: Name of Article and Details</p>
            <p id="article-description">A short description about the article, and how it fuelled the journey. A little bit more about the article and its content.</p>
            <button>Read Now</button>
          </div>
      </div>
    </div>
  </div>
    <div className="App">
      <p>To get your profile details: </p>
      <button onClick={getData}>Click me</button>
      {profileData && (
        <div>
          <p>Profile name: {profileData.profile_name}</p>
          <p>About me: {profileData.about_me}</p>
        </div>
      )}
    </div>
    </>
  );
};

export default HomePage;
