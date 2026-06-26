// Connect to the Python API endpoint we made in app.py
fetch('/api/churn-prediction')
    .then(response => response.json())
    .then(data => {
        const alertBox = document.getElementById('alert-box');
        
        // Dynamically update the HTML using the data from Python
        alertBox.innerHTML = `
            <h2>Client: ${data.customer_name}</h2>
            <p>Risk Score: <strong>${data.churn_risk}%</strong></p>
            <div class="badge emergency">${data.message}</div>
        `;
    })
    .catch(error => console.error('Error fetching data:', error));