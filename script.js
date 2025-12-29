// Apple-Style Multi-Step Calculator Logic

document.addEventListener('DOMContentLoaded', () => {
    // --- Multi-Step Navigation Logic ---
    let currentStep = 1;
    const totalSteps = 5;

    const btnNextList = document.querySelectorAll('.btn-next');
    const btnBackList = document.querySelectorAll('.btn-back');
    const progressDots = document.getElementById('progress-dots').children;

    // Initialize State
    updateUI(currentStep);

    // Next Button Handlers
    btnNextList.forEach(btn => {
        btn.addEventListener('click', () => {
            if (validateStep(currentStep)) {
                if (currentStep < totalSteps) {
                    currentStep++;
                    updateUI(currentStep);
                }
            }
        });
    });

    // Back Button Handlers
    btnBackList.forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentStep > 1) {
                currentStep--;
                updateUI(currentStep);
            }
        });
    });

    // Calculate Button Handler (Final Step)
    const calculateFinalBtn = document.getElementById('calculate-final-btn');
    if (calculateFinalBtn) {
        calculateFinalBtn.addEventListener('click', () => {
            calculateAndShowResult();
        });
    }

    // Restart Handler
    const restartBtn = document.getElementById('restart-btn');
    if (restartBtn) {
        restartBtn.addEventListener('click', () => {
            // Reset Form
            document.getElementById('calculator-form').reset();
            // Reset State
            currentStep = 1;
            // Hide Result
            document.getElementById('result-section').classList.add('hidden');
            document.getElementById('step-5').classList.remove('hidden'); // Show last step container if needed or just go to 1
            // Actually better UX to just reload or go to step 1
            updateUI(1);
        });
    }

    // Coverage Slider Real-time Update
    const coverageInput = document.getElementById('coverage');
    const coverageDisplay = document.getElementById('coverage-display');
    if (coverageInput && coverageDisplay) {
        coverageInput.addEventListener('input', (e) => {
            const val = parseInt(e.target.value);
            coverageDisplay.textContent = `$${val.toLocaleString()}`;
        });
    }


    // --- Helper Functions ---

    function updateUI(step) {
        // Hide all steps
        document.querySelectorAll('.step-content').forEach(el => {
            el.classList.remove('active');
        });

        // Show current step
        const currentEl = document.getElementById(`step-${step}`);
        if (currentEl) {
            currentEl.classList.add('active');
        }

        // Update Progress Dots
        for (let i = 0; i < progressDots.length; i++) {
            if (i < step) {
                progressDots[i].classList.remove('bg-gray-300');
                progressDots[i].classList.add('bg-appleBlue');
            } else {
                progressDots[i].classList.remove('bg-appleBlue');
                progressDots[i].classList.add('bg-gray-300');
            }
        }
    }

    function validateStep(step) {
        if (step === 1) {
            const ageInput = document.getElementById('age');
            const age = parseInt(ageInput.value);
            if (!age || age < 18 || age > 100) {
                alert("Please enter a valid age between 18 and 100.");
                ageInput.focus();
                return false;
            }
        }
        // Other steps (Radio buttons) generally have a default checked, so no validation needed unless removed.
        return true;
    }

    // --- Calculation Logic ---
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

        let coverageMultiplier = coverage / 100000;

        return baseRate * ageMultiplier * genderMultiplier * smokingMultiplier * healthMultiplier * coverageMultiplier;
    }

    function calculateAndShowResult() {
        const age = parseInt(document.getElementById('age').value);

        // Get Radio Values
        const gender = document.querySelector('input[name="gender"]:checked').value;
        const smoking = document.querySelector('input[name="smoking"]:checked').value;
        const health = document.querySelector('input[name="health"]:checked').value;
        const coverage = parseInt(document.getElementById('coverage').value);

        const premium = calculatePremium(age, gender, smoking, health, coverage);

        // Update Result Text
        document.getElementById('premium-amount').textContent = `$${premium.toFixed(2)}`;

        // Transition UI: Hide Form Steps, Show Result
        // We can hide the step container wrapper or just the current step
        document.getElementById(`step-${currentStep}`).classList.remove('active');

        // Ensure result section is visible
        const resultSection = document.getElementById('result-section');
        resultSection.classList.remove('hidden');

        // Hide progress dots on result screen for cleaner look
        document.getElementById('progress-dots').style.opacity = '0';
    }


    // --- Cookie Consent Logic ---
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptCookiesBtn = document.getElementById('accept-cookies');

    if (!localStorage.getItem('cookiesAccepted')) {
        setTimeout(() => {
            cookieBanner.classList.remove('translate-y-[150%]');
        }, 1500); // Slight delay
    }

    if (acceptCookiesBtn) {
        acceptCookiesBtn.addEventListener('click', () => {
            localStorage.setItem('cookiesAccepted', 'true');
            cookieBanner.classList.add('translate-y-[150%]');
        });
    }
});
