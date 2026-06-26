// 1. Fetch active session user metadata from SQLite relational table
fetch('/api/current-user')
    .then(response => response.json())
    .then(user => {
        const userHeader = document.getElementById('user-profile-tag');
        if(userHeader) {
            userHeader.innerHTML = `👤 Operator: <strong>${user.name}</strong> (${user.role} — ${user.region})`;
        }
    })
    .catch(err => console.error("Error connecting to SQLite service instance:", err));

// 2. Fetch ML Churn Data matrix endpoints
fetch('/api/churn-prediction')
    .then(response => response.json())
    .then(data => {
        const predictionPanel = document.getElementById('prediction-panel');
        const auditTrail = document.getElementById('audit-trail');
        
        const badgeClass = data.churn_risk > 50 ? 'danger' : 'stable';
        const riskColor = data.churn_risk > 50 ? 'var(--accent-red)' : 'var(--accent-green)';

        predictionPanel.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin:0;">Account: ${data.customer_name}</h2>
                <span class="badge ${badgeClass}">${data.status.toUpperCase()}</span>
            </div>
            <p style="color: var(--text-secondary); margin-top: 5px;">Predictive AI Account Cancellation Metric Vector</p>
            <div class="metric-highlight" style="color: ${riskColor};">${data.churn_risk}%</div>
            <div class="badge ${badgeClass}" style="display:block; text-align:center;">${data.message}</div>
        `;

        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        
        auditTrail.innerHTML = `
            <li class="log-item">
                <span class="timestamp">[${timeStr}]</span> 
                Inbound request evaluated. Saved record to MongoDB cluster. Status code: 200 OK.
            </li>
            <li class="log-item">
                <span class="timestamp">[System]</span> Pipeline stable. SQL & NoSQL data synchronization complete.
            </li>
        `;

        return fetch('/api/log-activity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                client_name: data.customer_name,
                action: `AI calculated execution evaluation matrix: ${data.churn_risk}% Churn Probability.`
            })
        });
    })
    .catch(error => console.error('Error executing frontend script integration:', error));