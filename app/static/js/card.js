// card.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. SELECT ELEMENTS
    const cardInner = document.getElementById('card-inner');
    const buttons = document.querySelectorAll('.card-btn');
    const currentStreakText = document.getElementById('current-streak');
    const maxStreakText = document.getElementById('max-streak');

    // 2. STATE
    let currentStreak = 0;
    let maxStreak = 0;
    const TOTAL_CARDS = 20;
    let reviewCounts = { again: 0, hard: TOTAL_CARDS, good: 0, easy: 0 };
    let totalReviewed = 0;

    // 3. FLIP LOGIC
    function flipCard() {
        if (cardInner) cardInner.classList.toggle('is-flipped');
    }

    window.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            e.preventDefault();
            flipCard();
        }
    });

    if (cardInner) {
        cardInner.addEventListener('click', (e) => {
            if (e.target.closest('.card-btn')) return;
            const rect = cardInner.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const cardWidth = rect.width;
            if (x < cardWidth * 0.2 || x > cardWidth * 0.8) {
                flipCard();
            }
        });
    }

    // 4. RATING LOGIC
    buttons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;

            if (reviewCounts.hard > 0) {
                reviewCounts.hard--;
            }
            reviewCounts[action]++;
            totalReviewed++;

            updateProgressBar();
            updateStreaks(action);

            setTimeout(flipCard, 200);

            // Send to backend
            if (typeof HANDLE_CARD_URL !== 'undefined') {
                fetch(HANDLE_CARD_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: action })
                })
                .then(res => res.json())
                .then(data => console.log(data.message))
                .catch(err => console.error('Card fetch error:', err));
            }
        });
    });

    // 5. PROGRESS BAR
    function updateProgressBar() {
        const segAgain = document.getElementById('segment-again');
        const segHard = document.getElementById('segment-hard');
        const segGood = document.getElementById('segment-good');
        const segEasy = document.getElementById('segment-easy');
        const cardsReviewed = document.getElementById('cards-reviewed');

        if (segAgain) segAgain.style.width = (reviewCounts.again / TOTAL_CARDS) * 100 + '%';
        if (segHard) segHard.style.width = (reviewCounts.hard / TOTAL_CARDS) * 100 + '%';
        if (segGood) segGood.style.width = (reviewCounts.good / TOTAL_CARDS) * 100 + '%';
        if (segEasy) segEasy.style.width = (reviewCounts.easy / TOTAL_CARDS) * 100 + '%';
        if (cardsReviewed) cardsReviewed.innerText = totalReviewed;
    }

    // 6. STREAKS
    function updateStreaks(action) {
        if (action === 'good' || action === 'easy') {
            currentStreak++;
            if (currentStreak > maxStreak) maxStreak = currentStreak;
        } else {
            currentStreak = 0;
        }
        if (currentStreakText) currentStreakText.innerText = currentStreak;
        if (maxStreakText) maxStreakText.innerText = maxStreak;
    }

    // Initialize
    updateProgressBar();
});