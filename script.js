// Fintech Minimalist Logic & Interactions

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Smart Coverage Calculator Logic ---
    const mortgageInput = document.getElementById('mortgage');
    const debtInput = document.getElementById('debt');
    const incomeInput = document.getElementById('income');
    const incomeYearsInput = document.getElementById('income-years');

    const mortgageVal = document.getElementById('mortgage-val');
    const debtVal = document.getElementById('debt-val');
    const incomeVal = document.getElementById('income-val');
    const incomeYearsVal = document.getElementById('income-years-val');
    const recCoverage = document.getElementById('recommended-coverage');

    // Chart.js Setup
    const ctx = document.getElementById('coverageChart').getContext('2d');
    let coverageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Year 0', 'Year 5', 'Year 10', 'Year 15', 'Year 20'],
            datasets: [{
                label: 'Coverage Need',
                data: [1000000, 800000, 600000, 400000, 200000],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false }, ticks: { font: { size: 10 } } },
                y: { display: false }
            }
        }
    });

    function updateCalculator() {
        const m = parseInt(mortgageInput.value);
        const d = parseInt(debtInput.value);
        const i = parseInt(incomeInput.value);
        const y = parseInt(incomeYearsInput.value);

        // Update Labels
        mortgageVal.textContent = `$${(m/1000).toFixed(0)}k`;
        debtVal.textContent = `$${(d/1000).toFixed(0)}k`;
        incomeVal.textContent = `$${(i/1000).toFixed(0)}k`;
        incomeYearsVal.textContent = `${y} Years`;

        // Calculate Total Need
        const total = m + d + (i * y);
        recCoverage.textContent = `$${(total/1000000).toFixed(2)}M`;

        // Update Chart Data (Simple linear depreciation simulation)
        const depreciation = total / 5;
        const newData = [
            total,
            Math.max(0, total - depreciation),
            Math.max(0, total - (depreciation * 2)),
            Math.max(0, total - (depreciation * 3)),
            Math.max(0, total - (depreciation * 4))
        ];
        coverageChart.data.datasets[0].data = newData;
        coverageChart.update();
    }

    [mortgageInput, debtInput, incomeInput, incomeYearsInput].forEach(input => {
        if(input) input.addEventListener('input', updateCalculator);
    });

    // Initial Call
    if(mortgageInput) updateCalculator();


    // --- 2. Progressive Quote Flow Logic ---
    let qStep = 1;
    const maxQSteps = 3;
    const nextBtn = document.getElementById('next-btn');
    const mobileNextBtn = document.getElementById('mobile-next-btn');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    function updateQuoteUI() {
        // Hide all steps
        document.querySelectorAll('#quote-form .step-content').forEach(el => el.classList.remove('active'));
        document.getElementById(`q-step-${qStep}`).classList.add('active');

        // Update Progress
        const percent = (qStep / maxQSteps) * 100;
        progressBar.style.width = `${percent}%`;

        if (qStep === 1) progressText.textContent = "Location";
        else if (qStep === 2) progressText.textContent = "Demographics";
        else if (qStep === 3) progressText.textContent = "Almost done...";
        else progressText.textContent = "Results";

        // Button Text
        const btnText = qStep === maxQSteps ? "Get Rates" : "Next";
        nextBtn.textContent = btnText;
        mobileNextBtn.textContent = btnText;
    }

    function handleNext() {
        if (qStep < maxQSteps) {
            // Validation
            if (qStep === 1) {
                const zip = document.getElementById('zipcode').value;
                if(zip.length < 5) {
                    alert("Please enter a valid zip code"); // Simple alert for MVP
                    return;
                }
            }
            qStep++;
            updateQuoteUI();
        } else {
            // Final Step - Show Results
            showResults();
        }
    }

    if(nextBtn) nextBtn.addEventListener('click', handleNext);
    if(mobileNextBtn) mobileNextBtn.addEventListener('click', handleNext);

    function showResults() {
        // Hide Quote Form
        document.querySelector('.lg\\:col-span-1').classList.add('hidden');
        // Expand Calculator Col to full width (optional UX choice, or replace quote form with result)
        // For simplicity, let's replace the calculator content or scroll to a result section

        // Show Matrix
        const matrix = document.getElementById('result-matrix');
        matrix.classList.remove('hidden');
        matrix.scrollIntoView({ behavior: 'smooth' });

        // Update Dummy Prices based on Calculator Input logic (Just for show)
        const recAmount = parseFloat(recCoverage.textContent.replace('$','').replace('M','')) * 1000000;
        const basePrice = (recAmount / 100000) * 12; // Dummy math
        document.getElementById('result-price-1').textContent = `$${basePrice.toFixed(2)}`;
        document.getElementById('result-price-2').textContent = `$${(basePrice * 1.1).toFixed(2)}`;
    }


    // --- 3. AI Chat Widget Logic ---
    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const closeChat = document.getElementById('close-chat');

    function toggleChat() {
        chatWidget.classList.toggle('open');
    }

    if(chatToggle) chatToggle.addEventListener('click', toggleChat);
    if(closeChat) closeChat.addEventListener('click', toggleChat);

});
