// This function handles user registration
async function registerUser() {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const messageDiv = document.getElementById('registerFeedback');

    // Clear previous messages
    messageDiv.innerText = '';
    
    try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();
        messageDiv.className = 'message';
        messageDiv.innerText = result.message || result.error; // Display message
    } catch (error) {
        messageDiv.className = 'message';
        messageDiv.innerText = 'Registration failed! Please try again.';
    }
}

// This function handles user login
async function loginUser() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const messageDiv = document.getElementById('loginFeedback');

    // Clear previous messages
    messageDiv.innerText = '';

    try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();
        messageDiv.className = 'message';

        if (result.token) {
            sessionStorage.setItem('token', result.token); // Store the JWT in session storage
            window.location.href = 'main.html'; // Redirect to main.html after successful login
        } else {
            messageDiv.innerText = result.error || 'Login failed! Please check your credentials.';
        }
    } catch (error) {
        messageDiv.className = 'message';
        messageDiv.innerText = 'Login failed! Please try again.';
    }
}