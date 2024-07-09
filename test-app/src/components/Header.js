import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
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
                    <h1>SaltCast</h1>
                    <Link to="/Map"><i className="fas fa-home"></i>Map</Link>
                    <Link to="/Profile"><i className="fas fa-user-circle"></i>Profile</Link>
                    {loggedIn? (
                        <>
                            <Link to="/logout"><i className="fas fa-sign-out-alt"></i>Logout</Link>
                        </>
                    ) : (
                        <>
                            <Link to="/Login"><i className="fas fa-sign-in-alt"></i>Login</Link>
                        </>
                    )}
                </div>
            </nav>
            <div className="content">
                
            </div>
        </header>
    );
};


export default Header;