(function () {
    var WORDS_3 = [
        { w: 'CAT', e: '🐱' }, { w: 'DOG', e: '🐶' }, { w: 'PIG', e: '🐷' },
        { w: 'COW', e: '🐮' }, { w: 'HEN', e: '🐔' }, { w: 'FOX', e: '🦊' },
        { w: 'BEE', e: '🐝' }, { w: 'OWL', e: '🦉' }, { w: 'ANT', e: '🐜' },
        { w: 'RAT', e: '🐀' }, { w: 'BAT', e: '🦇' },
        { w: 'SUN', e: '☀️' }, { w: 'SKY', e: '☁️' }, { w: 'SEA', e: '🌊' },
        { w: 'BED', e: '🛏️' }, { w: 'CUP', e: '☕' }, { w: 'HAT', e: '🎩' },
        { w: 'BAG', e: '👜' }, { w: 'BUS', e: '🚌' }, { w: 'CAR', e: '🚗' },
        { w: 'KEY', e: '🔑' }, { w: 'TOY', e: '🧸' }, { w: 'PIE', e: '🥧' },
        { w: 'EGG', e: '🥚' }, { w: 'BOY', e: '👦' }, { w: 'MOM', e: '👩' },
        { w: 'DAD', e: '👨' }, { w: 'EYE', e: '👁️' }, { w: 'EAR', e: '👂' }
    ];
    var WORDS_4 = [
        { w: 'FISH', e: '🐟' }, { w: 'BIRD', e: '🐦' }, { w: 'FROG', e: '🐸' },
        { w: 'BEAR', e: '🐻' }, { w: 'GOAT', e: '🐐' }, { w: 'LION', e: '🦁' },
        { w: 'WOLF', e: '🐺' }, { w: 'DUCK', e: '🦆' }, { w: 'CRAB', e: '🦀' },
        { w: 'DEER', e: '🦌' }, { w: 'MILK', e: '🥛' }, { w: 'CAKE', e: '🎂' },
        { w: 'RICE', e: '🍚' }, { w: 'PEAR', e: '🍐' }, { w: 'MEAT', e: '🥩' },
        { w: 'BOOK', e: '📖' }, { w: 'BALL', e: '⚽' }, { w: 'DOOR', e: '🚪' },
        { w: 'SHIP', e: '🚢' }, { w: 'KITE', e: '🪁' }, { w: 'DRUM', e: '🥁' },
        { w: 'BOAT', e: '⛵' }, { w: 'BIKE', e: '🚲' }, { w: 'STAR', e: '⭐' },
        { w: 'MOON', e: '🌙' }, { w: 'RAIN', e: '🌧️' }, { w: 'SNOW', e: '❄️' },
        { w: 'TREE', e: '🌳' }, { w: 'LEAF', e: '🍃' }, { w: 'FIRE', e: '🔥' },
        { w: 'KING', e: '👑' }, { w: 'BABY', e: '👶' }
    ];
    var LETTER_SOUNDS = {
        A: 'aah', B: 'buh', C: 'kuh', D: 'duh', E: 'eh',
        F: 'ffff', G: 'guh', H: 'huh', I: 'ih', J: 'juh',
        K: 'kuh', L: 'lll', M: 'mmm', N: 'nnn', O: 'ah',
        P: 'puh', Q: 'kwuh', R: 'rrr', S: 'sss', T: 'tuh',
        U: 'uh', V: 'vuh', W: 'wuh', X: 'ks', Y: 'yuh', Z: 'zzz'
    };

    var lengthToggle = document.getElementById('length-toggle');
    var modeToggle = document.getElementById('mode-toggle');
    var shuffleBtn = document.getElementById('shuffle-btn');
    var learnStage = document.getElementById('learn-stage');
    var practiceStage = document.getElementById('practice-stage');
    var counter = document.getElementById('learn-counter');
    var emojiEl = document.getElementById('learn-emoji');
    var wordEl = document.getElementById('learn-word');
    var sayBtn = document.getElementById('say-word');
    var prevBtn = document.getElementById('prev-btn');
    var nextBtn = document.getElementById('next-btn');
    var practiceEmoji = document.getElementById('practice-emoji');
    var practiceOptions = document.getElementById('practice-options');
    var practiceFeedback = document.getElementById('practice-feedback');
    var practiceScore = document.getElementById('practice-score');
    var practiceHear = document.getElementById('practice-hear');

    var currentLen = 3, currentMode = 'learn', words = WORDS_3.slice(), idx = 0;
    var practiceRight = 0, practiceTried = 0, practiceCurrent = null, practiceLocked = false;

    function speak(text, opts) {
        opts = opts || {};
        if (!window.speechSynthesis) return;
        try {
            window.speechSynthesis.cancel();
            var u = new SpeechSynthesisUtterance(text);
            u.rate = opts.rate || 0.75; u.pitch = opts.pitch || 1.1; u.lang = 'en-US';
            window.speechSynthesis.speak(u);
        } catch (e) {}
    }
    function shuffle(arr) {
        for (var i = arr.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1)); var t = arr[i]; arr[i] = arr[j]; arr[j] = t;
        }
        return arr;
    }
    function loadWords() { words = (currentLen === 3 ? WORDS_3 : WORDS_4).slice(); idx = 0; }
    function renderLearn() {
        if (!words.length) return;
        var w = words[idx];
        counter.textContent = 'Word ' + (idx + 1) + ' of ' + words.length;
        emojiEl.textContent = w.e;
        wordEl.innerHTML = w.w.split('').map(function (ch, i) {
            return '<button type="button" class="letter-tile" data-letter="' + ch + '">' + ch + '</button>';
        }).join('');
        wordEl.querySelectorAll('.letter-tile').forEach(function (b) {
            b.addEventListener('click', function () {
                var ch = b.dataset.letter;
                b.classList.add('pop');
                setTimeout(function () { b.classList.remove('pop'); }, 350);
                speak(LETTER_SOUNDS[ch] || ch, { rate: 0.7 });
            });
        });
        speak(w.w, { rate: 0.7 });
    }
    function renderPractice() {
        var pool = currentLen === 3 ? WORDS_3 : WORDS_4;
        practiceCurrent = pool[Math.floor(Math.random() * pool.length)];
        practiceEmoji.textContent = practiceCurrent.e;
        practiceFeedback.textContent = ''; practiceFeedback.className = 'practice-feedback';
        practiceLocked = false;
        var others = pool.filter(function (x) { return x.w !== practiceCurrent.w; });
        shuffle(others);
        var choices = [practiceCurrent, others[0], others[1]]; shuffle(choices);
        practiceOptions.innerHTML = choices.map(function (c) {
            return '<button type="button" class="practice-option" data-w="' + c.w + '">' + c.w + '</button>';
        }).join('');
        practiceOptions.querySelectorAll('.practice-option').forEach(function (b) {
            b.addEventListener('click', function () {
                if (practiceLocked) return;
                var pick = b.dataset.w; practiceTried += 1;
                if (pick === practiceCurrent.w) {
                    practiceRight += 1; b.classList.add('correct');
                    practiceFeedback.textContent = 'Great job! 🎉'; practiceFeedback.className = 'practice-feedback correct';
                    speak(practiceCurrent.w, { rate: 0.7 }); practiceLocked = true;
                    setTimeout(renderPractice, 1800);
                } else {
                    b.classList.add('wrong');
                    practiceFeedback.textContent = 'Try again! 💜'; practiceFeedback.className = 'practice-feedback wrong';
                    speak(practiceCurrent.w, { rate: 0.7 });
                }
                practiceScore.textContent = 'Right: ' + practiceRight + ' · Tried: ' + practiceTried;
            });
        });
        speak(practiceCurrent.w, { rate: 0.7 });
    }

    sayBtn.addEventListener('click', function () { speak(words[idx].w, { rate: 0.7 }); });
    practiceHear.addEventListener('click', function () { if (practiceCurrent) speak(practiceCurrent.w, { rate: 0.7 }); });
    prevBtn.addEventListener('click', function () { idx = (idx - 1 + words.length) % words.length; renderLearn(); });
    nextBtn.addEventListener('click', function () { idx = (idx + 1) % words.length; renderLearn(); });
    shuffleBtn.addEventListener('click', function () {
        if (currentMode === 'learn') { shuffle(words); idx = 0; renderLearn(); } else { renderPractice(); }
    });
    lengthToggle.querySelectorAll('button').forEach(function (b) {
        b.addEventListener('click', function () {
            lengthToggle.querySelectorAll('button').forEach(function (x) { x.classList.remove('active'); });
            b.classList.add('active'); currentLen = parseInt(b.dataset.len, 10); loadWords();
            if (currentMode === 'learn') renderLearn(); else renderPractice();
        });
    });
    modeToggle.querySelectorAll('button').forEach(function (b) {
        b.addEventListener('click', function () {
            modeToggle.querySelectorAll('button').forEach(function (x) { x.classList.remove('active'); });
            b.classList.add('active'); currentMode = b.dataset.mode;
            if (currentMode === 'learn') { learnStage.hidden = false; practiceStage.hidden = true; renderLearn(); }
            else { learnStage.hidden = true; practiceStage.hidden = false; practiceRight = 0; practiceTried = 0; practiceScore.textContent = 'Right: 0 · Tried: 0'; renderPractice(); }
        });
    });
    loadWords(); renderLearn();
})();
