// Theme Toggle Logic
const toggle = document.getElementById('theme-toggle');
const body = document.body;

toggle.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    body.setAttribute('data-theme', newTheme);
});

// Streak and Bar Logic
const buttons = document.querySelectorAll('.card-btn');
const currentStreakText = document.getElementById('current-streak');
const maxStreakText = document.getElementById('max-streak');

let currentStreak = 0;
let maxStreak = 0;

// Track heights for 4 bars
let barHeights = [0, 0, 0, 0];

buttons.forEach((btn, index) => {
    btn.addEventListener('click', () => {

        // Update streaks
        currentStreak++;
        if (currentStreak > maxStreak) {
            maxStreak = currentStreak;
        }

        // Increase corresponding bar
        barHeights[index] = Math.min(barHeights[index] + 10, 100);

        updateDisplay();
    });
});

function updateDisplay() {
    currentStreakText.innerText = currentStreak;
    maxStreakText.innerText = maxStreak;

    barHeights.forEach((height, i) => {
        const bar = document.getElementById(`bar-${i}`);
        if (bar) {
            bar.style.height = height + '%';
        }
    });
}
