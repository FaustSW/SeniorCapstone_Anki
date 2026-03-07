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
    // 2. STATE — initialize from server-provided stats
    // ======================================================================
    const initial = (typeof INITIAL_STATS !== 'undefined') ? INITIAL_STATS : {};
    let reviewStateId = typeof CURRENT_REVIEW_STATE_ID !== 'undefined' ? CURRENT_REVIEW_STATE_ID : null;
    let currentStreak = initial.current_streak || 0;
    let maxStreak = initial.max_streak || 0;
    let totalReviewed = initial.total_reviewed || 0;
    let reviewCounts = {
        again: (initial.counts && initial.counts.again) || 0,
        hard:  (initial.counts && initial.counts.hard)  || 0,
        good:  (initial.counts && initial.counts.good)  || 0,
        easy:  (initial.counts && initial.counts.easy)  || 0,
    };
    let isFlipping = false;

    const RATING_NAMES = { 1: 'again', 2: 'hard', 3: 'good', 4: 'easy' };

    // Render initial stats on page load
    updateProgressBar();
    if (currentStreakText) currentStreakText.innerText = currentStreak;
    if (maxStreakText) maxStreakText.innerText = maxStreak;

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

                // Sync stats from server (source of truth)
                if (data.stats) {
                    syncStats(data.stats);
                }

                if (data.next_card) {
                    flipToFront();
                    setTimeout(() => {
                        frontText.textContent = data.next_card.term;
                        backText.textContent = data.next_card.english_gloss;

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
                    }, 400);
                } else {
                    flipToFront();
                    setTimeout(() => {
                        frontText.textContent = '🎉 Done!';
                        backText.textContent = 'No more cards due.';
                        if (frontSentence) frontSentence.style.display = 'none';
                        if (backTranslation) backTranslation.style.display = 'none';
                        reviewStateId = null;
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
    // 5. SYNC STATS FROM SERVER
    // ======================================================================
    function syncStats(stats) {
        totalReviewed = stats.total_reviewed || 0;
        currentStreak = stats.current_streak || 0;
        maxStreak = stats.max_streak || 0;
        reviewCounts = {
            again: (stats.counts && stats.counts.again) || 0,
            hard:  (stats.counts && stats.counts.hard)  || 0,
            good:  (stats.counts && stats.counts.good)  || 0,
            easy:  (stats.counts && stats.counts.easy)  || 0,
        };

        if (currentStreakText) currentStreakText.innerText = currentStreak;
        if (maxStreakText) maxStreakText.innerText = maxStreak;
        updateProgressBar();
    }

    // ======================================================================
    // 6. PROGRESS BAR
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
});