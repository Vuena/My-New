// Life Insurance Premium Calculator Logic

/**
 * Calculates the estimated monthly premium.
 *
 * @param {number} age - The applicant's age.
 * @param {string} gender - 'male' or 'female'.
 * @param {string} smoking - 'smoker' or 'non-smoker'.
 * @param {string} health - 'excellent', 'good', 'average', or 'fair'.
 * @param {number} coverage - The coverage amount (e.g., 100000).
 * @returns {number} The estimated monthly premium.
 */
function calculatePremium(age, gender, smoking, health, coverage) {
    let baseRate = 10;

    // Age Calculation
    // Base rate starts at age 20. If younger than 20, we can floor it to 20 or treat as 20 for simplicity
    // based on "Base rate starts at $10/month for age 20".
    // If older, increase by 7% for every year.
    let ageFactor = 0;
    if (age > 20) {
        ageFactor = age - 20;
    }
    // Using compound interest formula: Base * (1 + rate)^years
    let ageMultiplier = Math.pow(1.07, ageFactor);

    // Gender Multiplier
    let genderMultiplier = (gender === 'male') ? 1.1 : 1.0;

    // Smoking Multiplier
    let smokingMultiplier = (smoking === 'smoker') ? 2.5 : 1.0;

    // Health Multiplier
    let healthMultiplier = 1.0;
    switch (health) {
        case 'excellent':
            healthMultiplier = 0.9;
            break;
        case 'good':
            healthMultiplier = 1.0;
            break;
        case 'average':
            healthMultiplier = 1.2;
            break;
        case 'fair':
            healthMultiplier = 1.5;
            break;
        default:
            healthMultiplier = 1.0;
    }

    // Coverage Multiplier (Linear scaling based on 100k)
    // 100k -> 1x, 250k -> 2.5x, etc.
    let coverageMultiplier = coverage / 100000;

    // Final Calculation
    let estimatedPremium = baseRate * ageMultiplier * genderMultiplier * smokingMultiplier * healthMultiplier * coverageMultiplier;

    return estimatedPremium;
}

document.addEventListener('DOMContentLoaded', () => {
    const calculateBtn = document.getElementById('calculate-btn');
    const resultDisplay = document.getElementById('result-display');
    const premiumAmount = document.getElementById('premium-amount');

    if (calculateBtn) {
        calculateBtn.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent form submission if inside a form

            // Get Input Values
            const age = parseInt(document.getElementById('age').value);
            const gender = document.getElementById('gender').value;
            const smoking = document.getElementById('smoking').value;
            const health = document.getElementById('health').value;
            const coverage = parseInt(document.getElementById('coverage').value);

            // Basic Validation
            if (!age || age < 18 || age > 100) {
                alert("Please enter a valid age (18-100).");
                return;
            }

            // Calculate
            const premium = calculatePremium(age, gender, smoking, health, coverage);

            // Display Result
            // Formatting to 2 decimal places
            premiumAmount.textContent = `$${premium.toFixed(2)}`;
            resultDisplay.classList.remove('hidden');

            // Scroll to result (optional, good UX)
            resultDisplay.scrollIntoView({ behavior: 'smooth' });
        });
    }
});
