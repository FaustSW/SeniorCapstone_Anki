// card.js

document.addEventListener('DOMContentLoaded', () => {

    // ======================================================================
    // 1. ELEMENTS
    // ======================================================================
    const cardInner = document.getElementById('card-inner');
    const frontText = document.getElementById('front-text');
    const backText = document.getElementById('back-text');
    const frontSentence = document.getElementById('front-sentence');
    const backTranslation = document.getElementById('back-translation');
    const buttons = document.querySelectorAll('.card-btn');
    const currentStreakText = document.getElementById('current-streak');
    const maxStreakText = document.getElementById('max-streak');

    // ======================================================================
    // 2. STATE
    // ======================================================================
    let reviewStateId = typeof CURRENT_REVIEW_STATE_ID !== 'undefined' ? CURRENT_REVIEW_STATE_ID : null;
    let currentStreak = 0;
    let maxStreak = 0;
    let totalReviewed = 0;
    let reviewCounts = { again: 0, hard: 0, good: 0, easy: 0 };
    let isFlipping = false;  // prevent double-clicks during animation

    const RATING_NAMES = { 1: 'again', 2: 'hard', 3: 'good', 4: 'easy' };

    // ======================================================================
    // 3. FLIP LOGIC
    // ======================================================================
    function flipCard() {
        if (cardInner) cardInner.classList.toggle('is-flipped');
    }

    function flipToFront() {
        if (cardInner) cardInner.classList.remove('is-flipped');
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

    // ======================================================================
    // 4. RATING LOGIC
    // ======================================================================
    buttons.forEach((btn) => {
        btn.addEventListener('click', () => {
            if (isFlipping || !reviewStateId) return;
            isFlipping = true;

            const rating = parseInt(btn.dataset.action);
            const ratingName = RATING_NAMES[rating];

            // Update local counters
            reviewCounts[ratingName]++;
            totalReviewed++;
            updateProgressBar();
            updateStreaks(ratingName);

            // POST rating to backend
            fetch(RATE_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    review_state_id: reviewStateId,
                    rating: rating
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    console.error('Rating error:', data.error);
                    isFlipping = false;
                    return;
                }

                if (data.next_card) {
                    // Flip to front, then swap content
                    flipToFront();
                    setTimeout(() => {
                        frontText.textContent = data.next_card.term;
                        backText.textContent = data.next_card.english_gloss;

                        // Update sentence / translation
                        if (frontSentence) {
                            frontSentence.textContent = data.next_card.sentence || '';
                            frontSentence.style.display = data.next_card.sentence ? '' : 'none';
                        }
                        if (backTranslation) {
                            backTranslation.textContent = data.next_card.translation || '';
                            backTranslation.style.display = data.next_card.translation ? '' : 'none';
                        }

                        reviewStateId = data.next_card.review_state_id;
                        isFlipping = false;
                    }, 400);  // wait for flip animation
                } else {
                    // No more cards due
                    flipToFront();
                    setTimeout(() => {
                        frontText.textContent = '🎉 Done!';
                        backText.textContent = 'No more cards due.';
                        reviewStateId = null;
                        // Disable buttons
                        buttons.forEach(b => b.disabled = true);
                        isFlipping = false;
                    }, 400);
                }
            })
            .catch(err => {
                console.error('Card fetch error:', err);
                isFlipping = false;
            });
        });
    });

    // ======================================================================
    // 5. PROGRESS BAR
    // ======================================================================
    function updateProgressBar() {
        const total = Math.max(totalReviewed, 1);
        const segAgain = document.getElementById('segment-again');
        const segHard = document.getElementById('segment-hard');
        const segGood = document.getElementById('segment-good');
        const segEasy = document.getElementById('segment-easy');
        const cardsReviewed = document.getElementById('cards-reviewed');
        const totalCards = document.getElementById('total-cards');

        if (segAgain) segAgain.style.width = (reviewCounts.again / total) * 100 + '%';
        if (segHard) segHard.style.width = (reviewCounts.hard / total) * 100 + '%';
        if (segGood) segGood.style.width = (reviewCounts.good / total) * 100 + '%';
        if (segEasy) segEasy.style.width = (reviewCounts.easy / total) * 100 + '%';
        if (cardsReviewed) cardsReviewed.innerText = totalReviewed;
        if (totalCards) totalCards.innerText = totalReviewed;
    }

    // ======================================================================
    // 6. STREAKS
    // ======================================================================
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
});