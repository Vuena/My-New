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
                    alert("Please enter a valid zip code");
                    return;
                }
            }
            if (qStep === 2) {
                const age = document.getElementById('age').value;
                if(!age || age < 18 || age > 100) {
                    alert("Please enter a valid age (18-100)");
                    return;
                }
                const gender = document.querySelector('input[name="gender"]:checked');
                if(!gender) {
                    alert("Please select a gender");
                    return;
                }
            }
            if (qStep === 3) {
                 const smoking = document.querySelector('input[name="smoking"]:checked');
                 if(!smoking) {
                     alert("Please select nicotine use status");
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

    function calculatePremium(age, gender, smoking, health, coverage) {
        let baseRate = 10;

        let ageFactor = (age > 20) ? age - 20 : 0;
        let ageMultiplier = Math.pow(1.07, ageFactor);

        let genderMultiplier = (gender === 'male') ? 1.1 : 1.0;
        let smokingMultiplier = (smoking === 'smoker') ? 2.5 : 1.0;

        let healthMultiplier = 1.0;
        switch (health) {
            case 'excellent': healthMultiplier = 0.9; break;
            case 'good': healthMultiplier = 1.0; break;
            case 'average': healthMultiplier = 1.2; break;
            case 'fair': healthMultiplier = 1.5; break;
        }

        // Coverage is linear based on 100k
        let coverageMultiplier = coverage / 100000;

        return baseRate * ageMultiplier * genderMultiplier * smokingMultiplier * healthMultiplier * coverageMultiplier;
    }

    function showResults() {
        try {
            // Hide Quote Form
            document.querySelector('.lg\\:col-span-1').classList.add('hidden');

            // Show Matrix
            const matrix = document.getElementById('result-matrix');
            matrix.classList.remove('hidden');
            matrix.scrollIntoView({ behavior: 'smooth' });

            // Get Input Values for REAL Calculation
            const ageEl = document.getElementById('age');
            const age = ageEl ? parseInt(ageEl.value) : 30;

            const genderEl = document.querySelector('input[name="gender"]:checked');
            const gender = genderEl ? genderEl.value : 'female';

            const smokingEl = document.querySelector('input[name="smoking"]:checked');
            const smoking = smokingEl ? smokingEl.value : 'non-smoker';

            const healthEl = document.getElementById('health');
            const health = healthEl ? healthEl.value : 'good';

            // Use Recommended Coverage from Smart Calculator as the coverage amount
            // format: $1.02M -> 1020000 or $500k -> 500000
            let recText = recCoverage ? recCoverage.textContent.trim().replace('$','') : "100000";
            let coverageAmount = 100000; // Default fallback

            if(recText.includes('M')) {
                coverageAmount = parseFloat(recText.replace('M','')) * 1000000;
            } else if(recText.includes('k')) {
                coverageAmount = parseFloat(recText.replace('k','')) * 1000;
            } else {
                 // Try simple parse if no suffix
                 let parsed = parseFloat(recText.replace(/,/g, ''));
                 if(!isNaN(parsed)) coverageAmount = parsed;
            }

            // Safety check if parsing failed or resulted in 0
            if (!coverageAmount || coverageAmount <= 0) coverageAmount = 100000;

            // Calculate
            const premium = calculatePremium(age, gender, smoking, health, coverageAmount);

            document.getElementById('result-price-1').textContent = `$${premium.toFixed(2)}`;
            // Competitor price slightly higher
            document.getElementById('result-price-2').textContent = `$${(premium * 1.15).toFixed(2)}`;
        } catch (e) {
            console.error("Calculation Error:", e);
            alert("An error occurred during calculation.");
        }
    }

    // --- Cookie Consent Logic ---
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptCookiesBtn = document.getElementById('accept-cookies');

    if (!localStorage.getItem('cookiesAccepted')) {
        setTimeout(() => {
            cookieBanner.classList.remove('translate-y-[150%]');
        }, 1500);
    }

    if (acceptCookiesBtn) {
        acceptCookiesBtn.addEventListener('click', () => {
            localStorage.setItem('cookiesAccepted', 'true');
            cookieBanner.classList.add('translate-y-[150%]');
        });
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
