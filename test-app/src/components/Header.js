import React, { useState, useEffect } from 'react';
import {NavLink, Link} from 'react-router-dom';
import './../css/navbar.css';
import './../css/register.css';


const Header = () => {
    const [loggedIn, setLoggedIn] = useState(false);

    useEffect(() => {
        const fetchSessionData = async () => {
            try {
                // /api/session is an endpoint used for Flask to obtain session variables
                const response = await fetch('/api/session');
                if(response.ok){
                    const sessionData = await response.json();
                    setLoggedIn(sessionData.loggedin);
                }
                else {
                    console.error('Failed to fetch session data');
                }
            } catch (error) {
                console.error('Error: ', error);
            }
        };

        fetchSessionData();
    }, []);//empty dependency array ensures this only runs once

    return(
        <header className={loggedIn?'loggedin':'loggedout'}>
            <nav className="navtop">
                <div>
                    <h1><Link to="/"><img src="images/SaltCastGreenText.svg" alt="logo" style={{ width:'6.2em', height:'1.8em' }}/></Link></h1>

                    <div className="nav-options">
                        <NavLink exact to="/"><span>Home</span></NavLink>
                        <Link><span>Dashboard</span></Link>
                        <NavLink to="/Map" activeClassName="active"><span>Salinity Map Tool</span></NavLink>
                        <NavLink to="/Aboutus" activeClassName="active"><span>Contact Us</span></NavLink>
                    </div>

                    <div className="login-logout">
                        {loggedIn ? (
                        <Link to="{{ url_for('logout') }}"><span>Logout</span></Link>
                        ) : (
                        <NavLink to="{{ url_for('login') }}" activeClassName="active" ><span>Login</span></NavLink>
                        )}
                        <NavLink to="{{ url_for('profile') }}" activeClassName="active" id="profile-link"><img src="images/profile.png" alt="profile" id="profile-icon"/></NavLink>
                        <img src="images/WCAG-icon.png" alt="WCAG" id="WCAG-icon"/>
                    </div>

                </div>
            </nav>
            <div className="content">
                
            </div>
        </header>
    );
};


export default Header;