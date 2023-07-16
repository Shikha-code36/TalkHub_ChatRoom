document.getElementById("registerForm").addEventListener("submit", registerUser);
document.getElementById("loginForm").addEventListener("submit", loginUser);

function registerUser(event) {
    event.preventDefault();

    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;

    // Make API request to register user
    // Replace the URL with your backend API endpoint
    fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        if(response.ok) {
          showMessage('Registered successfully!');
        } else {
          showMessage('Registration failed'); 
        }
    })
    .catch(error => {
        console.error("An error occurred during registration:", error);
    });
}

function loginUser(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    // Make API request to login user
    // Replace the URL with your backend API endpoint
    fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
    })
    .then(response => {
        if (response.ok) {
            showMessage("Login successful");
        } else {
            showMessage("Login failed");
        }
    })
    .catch(error => {
        console.error("An error occurred during login:", error);
    });
}

function showMessage(msg) {

    const popup = document.createElement('div');
    popup.classList.add('popup');
  
    popup.innerText = msg;
  
    document.body.appendChild(popup);
  
    setTimeout(() => {
      popup.remove();
    }, 2000);
  
  }