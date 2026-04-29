(function () {
    var board = document.getElementById('board');
    if (!board) return;
    var cards = Array.from(board.querySelectorAll('.memory-card'));
    var movesEl = document.getElementById('moves');
    var matchesEl = document.getElementById('matches');
    var timerEl = document.getElementById('timer');
    var winBox = document.getElementById('win-message');
    var winMoves = document.getElementById('win-moves');
    var winTime = document.getElementById('win-time');
    var totalPairs = cards.length / 2;
    var flipped = [];
    var matchedCount = 0;
    var moves = 0;
    var lock = false;
    var startTime = null;
    var timerInterval = null;

    function startTimer() {
        startTime = Date.now();
        timerInterval = setInterval(function() {
            var secs = Math.floor((Date.now() - startTime) / 1000);
            timerEl.textContent = secs + 's';
        }, 250);
    }
    function stopTimer() {
        if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    }
    function onCardClick(e) {
        var card = e.currentTarget;
        if (lock) return;
        if (card.classList.contains('flipped') || card.classList.contains('matched')) return;
        if (!startTime) startTimer();
        card.classList.add('flipped');
        flipped.push(card);
        if (flipped.length === 2) {
            moves += 1;
            movesEl.textContent = moves;
            var a = flipped[0]; var b = flipped[1];
            if (a.dataset.pair === b.dataset.pair) {
                a.classList.add('matched'); b.classList.add('matched');
                matchedCount += 1;
                matchesEl.textContent = matchedCount;
                flipped = [];
                if (matchedCount === totalPairs) { stopTimer(); showWin(); }
            } else {
                lock = true;
                setTimeout(function() {
                    a.classList.remove('flipped'); b.classList.remove('flipped');
                    flipped = []; lock = false;
                }, 850);
            }
        }
    }
    function showWin() {
        winMoves.textContent = moves;
        winTime.textContent = timerEl.textContent;
        winBox.hidden = false;
        winBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        var secs = Math.floor((Date.now() - startTime) / 1000);
        try {
            var entry = { type: 'memory', theme: board.dataset.theme || 'Memory', pairs: parseInt(board.dataset.pairs, 10) || totalPairs, moves: moves, timeSeconds: secs, date: new Date().toISOString() };
            var key = 'tws_history';
            var hist = JSON.parse(localStorage.getItem(key) || '[]');
            hist.push(entry);
            if (hist.length > 200) hist = hist.slice(-200);
            localStorage.setItem(key, JSON.stringify(hist));
        } catch (e) {}
        if (window.TWS) {
            var xpEarned = 20 + Math.max(0, totalPairs * 2 - Math.max(0, moves - totalPairs));
            TWS.awardXP(xpEarned);
            var xpBox = document.createElement('div');
            xpBox.className = 'xp-earned';
            xpBox.innerHTML = 'You earned <span class="xp-earned-amount">+' + xpEarned + '</span> XP!';
            winBox.appendChild(xpBox);
            TWS.renderHeaderBadge();
            var b = TWS.checkAndAwardBadges();
            if (b.new.length) setTimeout(function () { TWS.showBadgeToast(b.new); }, 800);
            setTimeout(function () { TWS.confetti({ count: 100 }); }, 200);
        }
    }
    cards.forEach(function(c) { c.addEventListener('click', onCardClick); });
})();
