import React, { useState } from 'react';
import axios from 'axios';

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
  );
};

export default HomePage;
