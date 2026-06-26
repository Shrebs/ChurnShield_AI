// 1. Sliders & Elements
const ticketSlider = document.getElementById('input-tickets');
const clickSlider = document.getElementById('input-clicks');
const ticketVal = document.getElementById('val-tickets');
const clickVal = document.getElementById('val-clicks');

const updateAI = () => {
    const tickets = ticketSlider.value;
    const clicks = clickSlider.value;
    
    ticketVal.innerText = tickets;
    clickVal.innerText = clicks;

    // Fetch dynamic prediction based on slider values
    fetch(`/api/churn-prediction?tickets=${tickets}&clicks=${clicks}`)
        .then(res => res.json())
        .then(data => {
            const predictionPanel = document.getElementById('prediction-panel');
            const badgeClass = data.churn_risk > 50 ? 'danger' : 'stable';
            const riskColor = data.churn_risk > 50 ? 'var(--accent-red)' : 'var(--accent-green)';

            predictionPanel.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="margin:0;">Account Evaluation</h2>
                    <span class="badge ${badgeClass}">${data.status.toUpperCase()}</span>
                </div>
                <div class="metric-highlight" style="color: ${riskColor};">${data.churn_risk}%</div>
                <div class="badge ${badgeClass}" style="display:block; text-align:center;">${data.message}</div>
            `;
        });
};

// Listen for slider moves
ticketSlider.addEventListener('input', updateAI);
clickSlider.addEventListener('input', updateAI);

// Initial Load
updateAI();

// 2. Load User Profile from SQLite
fetch('/api/current-user')
    .then(res => res.json())
    .then(user => {
        document.getElementById('user-profile-tag').innerHTML = `👤 Operator: <strong>${user.name}</strong>`;
    });