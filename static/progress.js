(function () {
    var NAME_KEY = 'tws_student_name';
    var HIST_KEY = 'tws_history';
    var AVATARS = ['🦊','🐼','🐯','🦁','🐶','🐱','🐰','🐻','🐸','🐵','🐧','🦉','🐢','🐬','🦄','🐲','🐺','🐨','🐹','🦄','🐙','🦋'];

    var nameInput = document.getElementById('student-name');
    var saveBtn = document.getElementById('save-name');
    var clearBtn = document.getElementById('clear-history');
    var listEl = document.getElementById('history-list');
    var emptyEl = document.getElementById('history-empty');
    var picker = document.getElementById('avatar-picker');

    nameInput.value = localStorage.getItem(NAME_KEY) || '';

    saveBtn.addEventListener('click', function () {
        localStorage.setItem(NAME_KEY, nameInput.value.trim());
        saveBtn.textContent = 'Saved ✓';
        if (window.TWS) TWS.renderHeaderBadge();
        setTimeout(function () { saveBtn.textContent = 'Save'; }, 1500);
    });

    clearBtn.addEventListener('click', function () {
        if (!confirm('Clear all activity history? This cannot be undone.')) return;
        localStorage.removeItem(HIST_KEY); render();
    });

    function buildAvatars() {
        var current = (window.TWS && TWS.getAvatar()) || '🦊';
        picker.innerHTML = AVATARS.map(function (e) {
            return '<button type="button" class="avatar-option' + (e === current ? ' selected' : '') + '" data-emoji="' + e + '">' + e + '</button>';
        }).join('');
        picker.querySelectorAll('.avatar-option').forEach(function (b) {
            b.addEventListener('click', function () {
                if (window.TWS) TWS.setAvatar(b.dataset.emoji);
                buildAvatars();
                if (window.TWS) TWS.renderHeaderBadge();
            });
        });
    }

    function fmtDate(iso) {
        try {
            var d = new Date(iso);
            return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) + ' · ' + d.toLocaleTimeString(undefined, { hour: 'numeric', minute: '2-digit' });
        } catch (e) { return iso; }
    }
    function fmtTime(secs) {
        if (typeof secs !== 'number') return '—';
        if (secs < 60) return secs + 's';
        var m = Math.floor(secs / 60); var s = secs % 60; return m + 'm ' + s + 's';
    }

    function renderBadges() {
        var grid = document.getElementById('badges-grid');
        if (!grid || !window.TWS) return;
        var earned = TWS.getBadges();
        grid.innerHTML = TWS.BADGES.map(function (b) {
            var unlocked = earned.indexOf(b.id) !== -1;
            return '<div class="badge-card ' + (unlocked ? 'unlocked' : 'locked') + '">' +
                '<div class="badge-emoji">' + b.emoji + '</div>' +
                '<div class="badge-name">' + b.name + '</div>' +
                '<div class="badge-desc">' + b.desc + '</div></div>';
        }).join('');
        document.getElementById('stat-badges').textContent = earned.length + ' / ' + TWS.BADGES.length;
    }

    function escape(s) {
        return String(s).replace(/[&<>"']/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
        });
    }

    function render() {
        var hist = [];
        try { hist = JSON.parse(localStorage.getItem(HIST_KEY) || '[]'); } catch (e) {}
        var quizzes = hist.filter(function (h) { return h.type === 'quiz'; });
        var games = hist.filter(function (h) { return h.type === 'memory'; });
        if (window.TWS) {
            var xp = TWS.getXP();
            document.getElementById('stat-level').textContent = TWS.levelFromXP(xp) + ' · ' + TWS.levelName(TWS.levelFromXP(xp));
            document.getElementById('stat-xp').textContent = xp;
            document.getElementById('stat-streak').textContent = TWS.getStreak().count;
        }
        document.getElementById('stat-quizzes').textContent = quizzes.length;
        document.getElementById('stat-memory').textContent = games.length;
        if (quizzes.length) {
            var totalPct = quizzes.reduce(function (sum, q) { return sum + (q.total ? (q.score / q.total) * 100 : 0); }, 0);
            document.getElementById('stat-avg').textContent = Math.round(totalPct / quizzes.length) + '%';
        } else { document.getElementById('stat-avg').textContent = '—'; }
        if (games.length) {
            var best = games.reduce(function (b, g) { if (typeof g.timeSeconds !== 'number') return b; return (b === null || g.timeSeconds < b) ? g.timeSeconds : b; }, null);
            document.getElementById('stat-best-time').textContent = best === null ? '—' : fmtTime(best);
        } else { document.getElementById('stat-best-time').textContent = '—'; }
        renderBadges();
        if (!hist.length) { listEl.innerHTML = ''; emptyEl.hidden = false; return; }
        emptyEl.hidden = true;
        var sorted = hist.slice().reverse();
        listEl.innerHTML = sorted.map(function (h) {
            if (h.type === 'quiz') {
                var pct = h.total ? Math.round((h.score / h.total) * 100) : 0;
                var cls = pct >= 70 ? 'good' : (pct >= 40 ? 'ok' : 'low');
                return '<div class="history-item"><div class="history-icon quiz">Q</div>' +
                    '<div class="history-main"><div class="history-title">' + escape(h.topic) + ' · Grade ' + h.grade + '</div>' +
                    '<div class="history-sub">' + fmtDate(h.date) + '</div></div>' +
                    '<div class="history-result ' + cls + '">' + h.score + ' / ' + h.total + '</div></div>';
            }
            if (h.type === 'memory') {
                return '<div class="history-item"><div class="history-icon memory">M</div>' +
                    '<div class="history-main"><div class="history-title">Memory: ' + escape(h.theme) + ' · ' + h.pairs + ' pairs</div>' +
                    '<div class="history-sub">' + fmtDate(h.date) + ' · ' + h.moves + ' moves</div></div>' +
                    '<div class="history-result good">' + fmtTime(h.timeSeconds) + '</div></div>';
            }
            return '';
        }).join('');
    }

    buildAvatars(); render();
})();
