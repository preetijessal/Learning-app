(function () {
    var SAVES_KEY = 'tws_codelab_saves';
    var STARTERS = [
        { title: '👋 Hello World', code: '<h1 style="color: purple;">Hello, World!</h1>\n<p>This is my very first webpage. 🌟</p>\n<p>Try changing the words and color!</p>' },
        { title: '🌈 Rainbow Name', code: '<h1 style="font-family: sans-serif;">\n  <span style="color: red;">M</span>\n  <span style="color: orange;">y</span>\n  <span style="color: green;">N</span>\n  <span style="color: blue;">a</span>\n  <span style="color: purple;">m</span>\n  <span style="color: deeppink;">e</span>\n</h1>\n<p>Change each letter to spell your own name! 🎨</p>' },
        { title: '🌟 About Me', code: '<div style="background: lightblue; padding: 24px; border-radius: 16px; font-family: sans-serif;">\n  <h2>About Me 🌟</h2>\n  <p>👋 Hi! My name is <b>Your Name</b>.</p>\n  <p>🎂 I am <b>10</b> years old.</p>\n  <p>🍕 My favorite food is <b>pizza</b>.</p>\n  <p>🎮 My favorite hobby is <b>gaming</b>.</p>\n  <p>🌟 When I grow up I want to be an <b>astronaut</b>.</p>\n</div>' },
        { title: '🐶 Pet Card', code: '<div style="text-align: center; background: #fff3cd; padding: 24px; border-radius: 20px; border: 3px solid orange; font-family: sans-serif;">\n  <h1>🐶 Buddy 🐶</h1>\n  <p style="font-size: 70px; margin: 0;">🦴</p>\n  <p><b>Type:</b> Golden Retriever</p>\n  <p><b>Age:</b> 3 years</p>\n  <p><b>Loves:</b> Belly rubs and tennis balls!</p>\n</div>' },
        { title: '🎉 Magic Button', code: '<div style="text-align: center; padding: 30px;">\n  <h2>Click the button below!</h2>\n  <button onclick="alert(\'You found me! 🎉\')"\n          style="font-size: 24px; padding: 16px 32px;\n                 background: hotpink; color: white;\n                 border: none; border-radius: 16px;\n                 cursor: pointer;">\n    🎁 Click me!\n  </button>\n</div>' },
        { title: '🎨 Color Garden', code: '<h2 style="font-family: sans-serif;">My Color Garden 🌷</h2>\n<div style="display: flex; gap: 10px; flex-wrap: wrap;">\n  <div style="width: 80px; height: 80px; background: red; border-radius: 12px;"></div>\n  <div style="width: 80px; height: 80px; background: orange; border-radius: 12px;"></div>\n  <div style="width: 80px; height: 80px; background: gold; border-radius: 12px;"></div>\n  <div style="width: 80px; height: 80px; background: limegreen; border-radius: 12px;"></div>\n  <div style="width: 80px; height: 80px; background: dodgerblue; border-radius: 12px;"></div>\n  <div style="width: 80px; height: 80px; background: purple; border-radius: 12px;"></div>\n</div>\n<p>Try changing the colors or adding more boxes!</p>' },
        { title: '😂 Joke Card', code: '<div style="background: linear-gradient(135deg, #ffd6e8, #fff3cd);\n            padding: 30px; border-radius: 20px;\n            font-family: sans-serif; text-align: center;">\n  <h2>😂 Joke of the Day</h2>\n  <p style="font-size: 20px;">Why did the math book look sad?</p>\n  <details>\n    <summary style="cursor: pointer; color: purple; font-weight: bold;">\n      Tap to see the answer!\n    </summary>\n    <p style="font-size: 22px; margin-top: 10px;">\n      Because it had too many <b>problems</b>! 📚\n    </p>\n  </details>\n</div>' },
        { title: '🧠 Mini Quiz', code: '<div style="font-family: sans-serif; padding: 24px; background: #f0e6ff; border-radius: 16px;">\n  <h2>🧠 Quick Quiz!</h2>\n  <p style="font-size: 20px;">What is 5 + 7?</p>\n  <button onclick="alert(\'Try again! 🤔\')" style="font-size: 18px; padding: 10px 18px; margin: 4px;">10</button>\n  <button onclick="alert(\'Correct! 🎉\')" style="font-size: 18px; padding: 10px 18px; margin: 4px;">12</button>\n  <button onclick="alert(\'Try again! 🤔\')" style="font-size: 18px; padding: 10px 18px; margin: 4px;">15</button>\n</div>' }
    ];

    var editor = document.getElementById('code-editor');
    var frame = document.getElementById('preview-frame');
    var runBtn = document.getElementById('run-btn');
    var clearBtn = document.getElementById('clear-btn');
    var autoRun = document.getElementById('auto-run');
    var saveBtn = document.getElementById('save-btn');
    var saveTitle = document.getElementById('save-title');
    var savesList = document.getElementById('saves-list');
    var savesEmpty = document.getElementById('saves-empty');
    var startersEl = document.getElementById('starters');

    function buildStarters() {
        startersEl.innerHTML = STARTERS.map(function (s, i) {
            return '<button type="button" class="starter-chip" data-i="' + i + '">' + s.title + '</button>';
        }).join('');
        startersEl.querySelectorAll('.starter-chip').forEach(function (b) {
            b.addEventListener('click', function () {
                var i = parseInt(b.dataset.i, 10);
                editor.value = STARTERS[i].code;
                run();
                if (!saveTitle.value) saveTitle.value = STARTERS[i].title.replace(/^[^\w]+/, '').trim();
                editor.focus();
            });
        });
    }

    function run() {
        var code = editor.value;
        var doc = '<!DOCTYPE html><html><head><meta charset="utf-8">' +
            '<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:16px;margin:0;color:#1e293b;}</style>' +
            '</head><body>' + code + '</body></html>';
        frame.srcdoc = doc;
    }

    var debounceTimer;
    editor.addEventListener('input', function () {
        if (!autoRun.checked) return;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(run, 300);
    });
    runBtn.addEventListener('click', run);
    clearBtn.addEventListener('click', function () {
        if (editor.value && !confirm('Clear your code?')) return;
        editor.value = ''; run(); editor.focus();
    });

    function getSaves() { try { return JSON.parse(localStorage.getItem(SAVES_KEY) || '[]'); } catch (e) { return []; } }
    function setSaves(arr) { try { localStorage.setItem(SAVES_KEY, JSON.stringify(arr)); } catch (e) {} }

    saveBtn.addEventListener('click', function () {
        var code = editor.value.trim();
        if (!code) { alert('Write some code first!'); return; }
        var title = saveTitle.value.trim() || 'My Creation';
        var saves = getSaves();
        saves.push({ id: Date.now(), title: title, code: editor.value, date: new Date().toISOString() });
        if (saves.length > 50) saves = saves.slice(-50);
        setSaves(saves); saveTitle.value = ''; renderSaves();
        saveBtn.textContent = 'Saved ✓';
        setTimeout(function () { saveBtn.textContent = '💾 Save Creation'; }, 1500);
        if (window.TWS) { var b = TWS.checkAndAwardBadges(); if (b.new.length) setTimeout(function () { TWS.showBadgeToast(b.new); }, 400); }
    });

    function escape(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    function fmtDate(iso) { try { var d = new Date(iso); return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }); } catch (e) { return ''; } }

    function renderSaves() {
        var saves = getSaves().slice().reverse();
        if (!saves.length) { savesList.innerHTML = ''; savesEmpty.hidden = false; return; }
        savesEmpty.hidden = true;
        savesList.innerHTML = saves.map(function (s) {
            return '<div class="save-item"><div class="save-info"><div class="save-title">' + escape(s.title) + '</div><div class="save-date">' + fmtDate(s.date) + '</div></div>' +
                '<div class="save-actions"><button type="button" class="btn btn-secondary btn-sm" data-load="' + s.id + '">Load</button>' +
                '<button type="button" class="btn btn-secondary btn-sm" data-del="' + s.id + '">Delete</button></div></div>';
        }).join('');
        savesList.querySelectorAll('[data-load]').forEach(function (b) {
            b.addEventListener('click', function () {
                var id = parseInt(b.dataset.load, 10);
                var hit = getSaves().filter(function (x) { return x.id === id; })[0];
                if (hit) { editor.value = hit.code; saveTitle.value = hit.title; run(); editor.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
            });
        });
        savesList.querySelectorAll('[data-del]').forEach(function (b) {
            b.addEventListener('click', function () {
                if (!confirm('Delete this creation?')) return;
                var id = parseInt(b.dataset.del, 10);
                setSaves(getSaves().filter(function (x) { return x.id !== id; })); renderSaves();
            });
        });
    }

    buildStarters(); renderSaves();
    editor.value = STARTERS[0].code; run();
})();
