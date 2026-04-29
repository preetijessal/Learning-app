(function () {
    var KEYS = {
        avatar: 'tws_avatar',
        xp: 'tws_xp',
        streak: 'tws_streak',
        history: 'tws_history',
        badges: 'tws_badges',
        name: 'tws_student_name'
    };

    var BADGES = [
        { id: 'first_quiz', emoji: '⭐', name: 'First Steps', desc: 'Complete your first quiz' },
        { id: 'perfect', emoji: '💯', name: 'Perfect Score', desc: 'Get 100% on any quiz' },
        { id: 'streak_3', emoji: '🔥', name: 'On Fire', desc: '3-day practice streak' },
        { id: 'streak_7', emoji: '🚀', name: 'Unstoppable', desc: '7-day practice streak' },
        { id: 'quizzes_10', emoji: '🏆', name: 'Quiz Champion', desc: 'Complete 10 quizzes' },
        { id: 'memory_5', emoji: '🧠', name: 'Memory Master', desc: 'Win 5 memory games' },
        { id: 'memory_quick', emoji: '⚡', name: 'Quick Thinker', desc: 'Win memory in under 30 seconds' },
        { id: 'level_5', emoji: '🌟', name: 'Rising Star', desc: 'Reach Level 5' },
        { id: 'level_10', emoji: '👑', name: 'Math Royalty', desc: 'Reach Level 10' },
        { id: 'pressure_pro', emoji: '🌡️', name: 'Pressure Pro', desc: 'Perfect on a Pressure quiz' },
        { id: 'junior_coder', emoji: '💻', name: 'Junior Coder', desc: 'Save your first Code Lab creation' },
        { id: 'web_wizard', emoji: '🧙', name: 'Web Wizard', desc: 'Save 5 Code Lab creations' }
    ];

    var XP_PER_LEVEL = 100;
    var LEVEL_NAMES = [
        'Beginner', 'Explorer', 'Apprentice', 'Achiever', 'Rising Star',
        'Math Whiz', 'Genius', 'Champion', 'Master', 'Legend', 'Math Royalty'
    ];

    function getJSON(key, fallback) {
        try { var v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; }
    }
    function setJSON(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {} }
    function getStr(key, fallback) { var v = localStorage.getItem(key); return v === null ? fallback : v; }
    function setStr(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

    function todayStr() {
        var d = new Date();
        return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    }
    function dateDiffDays(a, b) {
        var da = new Date(a + 'T00:00:00'); var db = new Date(b + 'T00:00:00');
        return Math.round((db - da) / 86400000);
    }

    function recordVisit() {
        var streak = getJSON(KEYS.streak, { count: 0, lastDate: null });
        var today = todayStr();
        if (streak.lastDate === today) return streak;
        if (streak.lastDate === null) { streak.count = 1; }
        else { var diff = dateDiffDays(streak.lastDate, today); if (diff === 1) streak.count += 1; else if (diff > 1) streak.count = 1; }
        streak.lastDate = today;
        setJSON(KEYS.streak, streak);
        return streak;
    }

    function getXP() { return parseInt(getStr(KEYS.xp, '0'), 10) || 0; }
    function setXP(n) { setStr(KEYS.xp, String(n)); }
    function awardXP(n) {
        var prev = getXP(); var prevLvl = levelFromXP(prev); var next = prev + n; setXP(next);
        return { previous: prev, current: next, leveledUp: levelFromXP(next) > prevLvl };
    }
    function levelFromXP(xp) { return Math.floor(xp / XP_PER_LEVEL) + 1; }
    function levelName(lvl) { return LEVEL_NAMES[Math.min(lvl - 1, LEVEL_NAMES.length - 1)]; }
    function xpInLevel(xp) { return xp % XP_PER_LEVEL; }
    function getAvatar() { return getStr(KEYS.avatar, '🦊'); }
    function setAvatar(e) { setStr(KEYS.avatar, e); }
    function getName() { return getStr(KEYS.name, ''); }
    function getHistory() { return getJSON(KEYS.history, []); }
    function getBadges() { return getJSON(KEYS.badges, []); }

    function checkAndAwardBadges() {
        var existing = getBadges(); var newly = [];
        var hist = getHistory();
        var quizzes = hist.filter(function (h) { return h.type === 'quiz'; });
        var games = hist.filter(function (h) { return h.type === 'memory'; });
        var streak = getJSON(KEYS.streak, { count: 0 });
        var lvl = levelFromXP(getXP());
        function unlock(id) { if (existing.indexOf(id) === -1) { existing.push(id); newly.push(id); } }
        if (quizzes.length >= 1) unlock('first_quiz');
        if (quizzes.some(function (q) { return q.score === q.total && q.total > 0; })) unlock('perfect');
        if (streak.count >= 3) unlock('streak_3');
        if (streak.count >= 7) unlock('streak_7');
        if (quizzes.length >= 10) unlock('quizzes_10');
        if (games.length >= 5) unlock('memory_5');
        if (games.some(function (g) { return g.timeSeconds && g.timeSeconds < 30; })) unlock('memory_quick');
        if (lvl >= 5) unlock('level_5');
        if (lvl >= 10) unlock('level_10');
        if (quizzes.some(function (q) { return (q.topicKey === 'pressure' || q.topicKey === 'pressure_concepts') && q.score === q.total && q.total > 0; })) unlock('pressure_pro');
        var codelabSaves = getJSON('tws_codelab_saves', []);
        if (codelabSaves.length >= 1) unlock('junior_coder');
        if (codelabSaves.length >= 5) unlock('web_wizard');
        if (newly.length) setJSON(KEYS.badges, existing);
        return { all: existing, new: newly };
    }

    function renderHeaderBadge() {
        var el = document.getElementById('user-badge');
        if (!el) return;
        var xp = getXP(); var lvl = levelFromXP(xp); var inLvl = xpInLevel(xp);
        var streak = getJSON(KEYS.streak, { count: 0 });
        el.innerHTML = '<span class="ub-avatar">' + getAvatar() + '</span>' +
            '<span class="ub-info"><span class="ub-level">Lv ' + lvl + ' · ' + levelName(lvl) + '</span>' +
            '<span class="ub-bar"><span class="ub-bar-fill" style="width:' + inLvl + '%;"></span></span></span>' +
            '<span class="ub-streak" title="Day streak">🔥 ' + streak.count + '</span>';
    }

    function confetti(opts) {
        opts = opts || {}; var count = opts.count || 90;
        var colors = ['#6366f1', '#f59e0b', '#ec4899', '#10b981', '#fbbf24', '#8b5cf6', '#06b6d4'];
        var container = document.createElement('div'); container.className = 'confetti-layer';
        document.body.appendChild(container);
        for (var i = 0; i < count; i++) {
            var p = document.createElement('span'); p.className = 'confetti-piece';
            p.style.left = Math.random() * 100 + '%';
            p.style.background = colors[Math.floor(Math.random() * colors.length)];
            p.style.animationDelay = (Math.random() * 0.5) + 's';
            p.style.animationDuration = (1.8 + Math.random() * 1.4) + 's';
            container.appendChild(p);
        }
        setTimeout(function () { container.remove(); }, 3800);
    }

    function showBadgeToast(badgeIds) {
        if (!badgeIds || !badgeIds.length) return;
        badgeIds.forEach(function (id, i) {
            var b = BADGES.filter(function (x) { return x.id === id; })[0];
            if (!b) return;
            setTimeout(function () {
                var t = document.createElement('div'); t.className = 'badge-toast';
                t.innerHTML = '<span class="badge-toast-emoji">' + b.emoji + '</span>' +
                    '<div><div class="badge-toast-title">Badge Unlocked!</div>' +
                    '<div class="badge-toast-name">' + b.name + '</div></div>';
                document.body.appendChild(t);
                requestAnimationFrame(function () { t.classList.add('show'); });
                setTimeout(function () { t.classList.remove('show'); }, 4000);
                setTimeout(function () { t.remove(); }, 4600);
            }, i * 700);
        });
    }

    window.TWS = {
        BADGES: BADGES, XP_PER_LEVEL: XP_PER_LEVEL,
        getXP: getXP, awardXP: awardXP, levelFromXP: levelFromXP, levelName: levelName, xpInLevel: xpInLevel,
        getAvatar: getAvatar, setAvatar: setAvatar, getName: getName, getHistory: getHistory, getBadges: getBadges,
        getStreak: function () { return getJSON(KEYS.streak, { count: 0, lastDate: null }); },
        recordVisit: recordVisit, checkAndAwardBadges: checkAndAwardBadges,
        renderHeaderBadge: renderHeaderBadge, confetti: confetti, showBadgeToast: showBadgeToast
    };

    function init() {
        recordVisit(); renderHeaderBadge();
        var result = checkAndAwardBadges();
        if (result.new.length) { setTimeout(function () { showBadgeToast(result.new); }, 600); }
    }
    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
})();
