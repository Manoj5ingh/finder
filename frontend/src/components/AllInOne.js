import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AllInOne = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('isLoggedIn') === 'true');
    const [showLogin, setShowLogin] = useState(true);
    const [showSignupSuccess, setShowSignupSuccess] = useState(false);
    const [showSearch, setShowSearch] = useState(false);
    const [searchResults, setSearchResults] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [showFlagButton, setShowFlagButton] = useState(false);
    const [loginFormData, setLoginFormData] = useState({
        username: '',
        password: '',
    });
    const [signupFormData, setSignupFormData] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        username: '',
    });

    const handleLoginChange = (e) => {
        setLoginFormData({ ...loginFormData, [e.target.name]: e.target.value });
    };

    const handleSignupChange = (e) => {
        setSignupFormData({ ...signupFormData, [e.target.name]: e.target.value });
    };

    useEffect(() => {
        // Fetch boolean flag after login
        const fetchFlag = async () => {
            try {
                const response = await axios.get('/api/configs', {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                });
                setShowFlagButton(!response.data.includes('gmail'));
            } catch (error) {
                console.error(error);
            }
        };

        if (isLoggedIn) {
            fetchFlag();
        }
    }, [isLoggedIn]);

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/users/login/', loginFormData);
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('isLoggedIn', true)
            window.location.reload()
        } catch (error) {
            console.error(error.response.data);
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/users/signup/', signupFormData);
            console.log(response.data);
            setShowSignupSuccess(true);
            setShowLogin(true);
        } catch (error) {
            console.error(error);
        }
    };

    const connectGmail = async () => {
        try {
           const headers = {
             Authorization: `Token ${localStorage.getItem('token')}`,
           };
           const response = await axios.get('/api/connect/gmail_auth/', { headers });
           window.location.href = response.data.redirectUrl;
        } catch (error) {
          console.error('Error fetching API:', error);
        }
      }

    const handleSearch = async () => {
        try {
            const response = await axios.get('/api/search?query=' + searchText, {
                headers: {
                    Authorization: `Token ${localStorage.getItem('token')}`,
                },
            });
            setSearchResults(response.data);
            setShowSearch(true);
        } catch (error) {
            console.error(error);
        }
    };

    const handleSearchBoxChange = (event) => {
        setSearchText(event.target.value);
    };

    const handleSearchButtonClick = () => {
        handleSearch();
    };

    const handleNewSearch = () => {
        setShowSearch(false);
    }

    return (
        <div>
            {isLoggedIn ? (
                showSearch ? (
                    <div>
                        <h1>Search Results    </h1> <button onClick={handleNewSearch}>New Search</button>
                        <ul>
                            {searchResults[0].gmail.map((result, index) => (
                                <li key={index}>
                                    <a href={result.target_url} target="_blank" rel="noopener noreferrer">
                                        {result.snippet}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                ) : (
                    <div>
                        <input
                            type="text"
                            placeholder="Enter search text"
                            value={searchText}
                            onChange={handleSearchBoxChange}
                        />
                        <button onClick={handleSearchButtonClick}>Search</button>
                    </div>
                )
            ) : showLogin ? (
                <div>
                    <h2>Login</h2>
                    <form onSubmit={handleLogin}>
                        <input type="text" name="username" placeholder="username" onChange={handleLoginChange}/>
                        <input type="password" name="password" placeholder="Password" onChange={handleLoginChange}/>
                        <button type="submit">Login</button>
                    </form>
                    <a onClick={() => setShowLogin(false)}>Signup here</a>
                </div>
            ) : (
                <div>
                    <h2>Signup</h2>
                    <form onSubmit={handleSignup}>
                        <input type="text" name="email" placeholder="Email" onChange={handleSignupChange} />
                        <input type="password" name="password" placeholder="Password" onChange={handleSignupChange} />
                        <input type="text" name="first_name" placeholder="First Name" onChange={handleSignupChange} />
                        <input type="text" name="last_name" placeholder="Last Name" onChange={handleSignupChange} />
                        <input type="text" name="username" placeholder="Username" onChange={handleSignupChange} />
                        <button type="submit">Sign Up</button>
                    </form>
                    <a onClick={() => setShowLogin(true)}>Login here</a>
                    {showSignupSuccess && <p>Signup successful! Now you can login.</p>}
                </div>
            )}
            {showFlagButton && <button onClick={connectGmail}>Connect Gmail</button>}
        </div>
    );
};

export default AllInOne;
