/* --------------------------------------------------------------
   Drum Sequencer – полная версия с локальными звуками (WAV)
   --------------------------------------------------------------*/

class DrumSequencer {
    constructor() {
        /* ---------- Настройки ---------- */
        this.tracks = ['hihat', 'snare', 'kick', 'openhat', 'tom1', 'tom2']; // названия дорожек
        this.steps  = 16;                     // количество шагов (16‑16‑th нот)
        this.bpm    = 120;                    // начальное BPM

        /* ---------- Состояние ---------- */
        this.pattern       = {};               // объект pattern[track][step] = 0/1
        this.isPlaying     = false;            // сейчас играет?
        this.currentStep   = 0;                // текущий шаг во время воспроизведения
        this.intervalId    = null;             // ID setInterval
        this.audioContext  = null;             // Web Audio API context
        this.samples       = {};               // загруженные AudioBuffer‑ы
        this.audioReady    = false;            // true, когда все сэмплы загружены

        /* ---------- Инициализация ---------- */
        this.initPattern();       // пустой паттерн
        this.renderGrid();        // визуальная сетка
        this.setupEventListeners();
        this.refreshPatternList(); // список сохранённых паттернов

        // сразу начинаем загрузку звуков (можно вызвать вручную, если хотите)
        this.initAudio();
    }

    /* ------------------------------------------------------------------------
       AUDIO – инициализация и загрузка сэмплов
       ------------------------------------------------------------------------ */
    async initAudio() {
        try {
            // 1️⃣ создаём AudioContext (нужен пользовательский клик, но мы
            //    вызываем initAudio() при конструировании – большинство браузеров
            //    уже «разблокируют» контекст после первого клика на странице)
            this.audioContext = new (window.AudioContext ||
                                   window.webkitAudioContext)();

            // 2️⃣ пути к вашим wav‑файлам (разместите их в /static/sounds/)
            const samplesUrls = {
                kick:    '/static/sounds/kick.wav',
                snare:   '/static/sounds/snare.wav',
                hihat:   '/static/sounds/hihat.wav',
                openhat: '/static/sounds/openhat.wav',
                tom1:    '/static/sounds/tom1.wav',
                tom2:    '/static/sounds/tom2.wav'
            };

            console.log('Загрузка звуковых сэмплов...');

            // 3️⃣ параллельно загружаем все файлы
            const loadPromises = Object.entries(samplesUrls).map(
                async ([name, url]) => {
                    try {
                        const resp = await fetch(url);
                        if (!resp.ok) {
                            throw new Error(`HTTP ${resp.status}`);
                        }
                        const arrayBuf = await resp.arrayBuffer();
                        this.samples[name] = await this.audioContext.decodeAudioData(
                            arrayBuf
                        );
                        console.log(`✔️ ${name} загружен`);
                    } catch (e) {
                        console.error(`❌ Ошибка загрузки ${name}:`, e);
                    }
                }
            );

            await Promise.all(loadPromises);
            this.audioReady = true;
            console.log('Все сэмплы готовы к использованию');
        } catch (e) {
            console.error('Не удалось инициализировать AudioContext:', e);
        }
    }

    playSound(name) {
        if (!this.audioReady) {
            console.warn('Звуки ещё не загружены');
            return;
        }
        const buffer = this.samples[name];
        if (!buffer) {
            console.warn(`Сэмпл "${name}" не найден`);
            return;
        }

        try {
            const src = this.audioContext.createBufferSource();
            src.buffer = buffer;
            src.connect(this.audioContext.destination);
            src.start(0);
        } catch (e) {
            console.error(`Ошибка воспроизведения ${name}:`, e);
        }
    }

    /* ------------------------------------------------------------------------
       PATTERN – работа с паттерном
       ------------------------------------------------------------------------ */
    initPattern() {
        this.tracks.forEach(track => {
            this.pattern[track] = new Array(this.steps).fill(0);
        });
    }

    renderGrid() {
        const grid = document.getElementById('drumGrid');
        if (!grid) {
            console.error('#drumGrid элемент не найден в DOM');
            return;
        }
        grid.innerHTML = '';

        this.tracks.forEach(track => {
            const row = document.createElement('div');
            row.className = 'track-row';

            const nameDiv = document.createElement('div');
            nameDiv.className = 'track-name';
            nameDiv.textContent = track;
            row.appendChild(nameDiv);

            const stepsDiv = document.createElement('div');
            stepsDiv.className = 'track-steps';

            this.pattern[track].forEach((v, i) => {
                const stepDiv = document.createElement('div');
                stepDiv.className = `step ${v ? 'active' : ''}`;
                stepDiv.dataset.track = track;
                stepDiv.dataset.step = i;
                stepDiv.textContent = v ? '●' : '';
                stepDiv.addEventListener('click', () => this.toggleStep(track, i));
                stepsDiv.appendChild(stepDiv);
            });

            row.appendChild(stepsDiv);
            grid.appendChild(row);
        });
    }

    toggleStep(track, step) {
        this.pattern[track][step] = this.pattern[track][step] ? 0 : 1;
        this.renderGrid();
    }

    /* ------------------------------------------------------------------------
       PLAYBACK – воспроизведение паттерна
       ------------------------------------------------------------------------ */
    playPattern() {
        if (this.isPlaying) {
            this.stopPattern();
            return;
        }

        // Если контекст был «заморожен», разблокируем его (нужен пользовательский клик)
        if (this.audioContext && this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }

        if (!this.audioReady) {
            alert('Звуки ещё не загружены. Пожалуйста, подождите несколько секунд.');
            return;
        }

        this.isPlaying = true;
        document.getElementById('playButton').textContent = 'Стоп';

        const stepTime = (60 / this.bpm) / 4 * 1000; // 16‑ти нотный шаг

        this.intervalId = setInterval(() => {
            this.highlightStep(this.currentStep);

            // Проигрываем все дорожки, где в текущем столбце стоит 1
            this.tracks.forEach(track => {
                if (this.pattern[track][this.currentStep]) {
                    this.playSound(track);
                }
            });

            this.currentStep = (this.currentStep + 1) % this.steps;
        }, stepTime);
    }

    stopPattern() {
        this.isPlaying = false;
        clearInterval(this.intervalId);
        document.getElementById('playButton').textContent = 'Проиграть';
        this.clearHighlights();
    }

    highlightStep(step) {
        this.clearHighlights();
        const cells = document.querySelectorAll(`.step[data-step="${step}"]`);
        cells.forEach(c => c.classList.add('playing'));
    }

    clearHighlights() {
        const cells = document.querySelectorAll('.step.playing');
        cells.forEach(c => c.classList.remove('playing'));
    }

    clearPattern() {
        this.initPattern();
        this.renderGrid();
        this.stopPattern();
    }

    /* ------------------------------------------------------------------------
       STORAGE – API‑запросы для сохранения/загрузки паттернов
       ------------------------------------------------------------------------ */
    async savePattern() {
        const name = document.getElementById('patternName').value || 'default';
        try {
            const resp = await fetch(`/api/drum/pattern/${name}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.pattern)
            });

            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            const data = await resp.json();
            if (data.status === 'saved') {
                alert('Паттерн сохранён');
                this.refreshPatternList();
            } else {
                throw new Error(data.error || 'Неизвестная ошибка');
            }
        } catch (e) {
            console.error('Ошибка сохранения:', e);
            alert('Не удалось сохранить паттерн');
        }
    }

    async loadPattern() {
        const name = document.getElementById('patternName').value || 'default';
        try {
            const resp = await fetch(`/api/drum/pattern/${name}`);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            this.pattern = await resp.json();
            this.renderGrid();
            alert('Паттерн загружен');
        } catch (e) {
            console.error('Ошибка загрузки:', e);
            alert('Не удалось загрузить паттерн');
        }
    }

    async deletePattern() {
        const name = document.getElementById('patternName').value || 'default';
        if (!confirm(`Удалить паттерн "${name}"?`)) return;

        try {
            const resp = await fetch(`/api/drum/pattern/${name}`, {
                method: 'DELETE'
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            const data = await resp.json();
            if (data.status === 'deleted') {
                alert('Паттерн удалён');
                this.refreshPatternList();
            } else {
                throw new Error(data.error);
            }
        } catch (e) {
            console.error('Ошибка удаления:', e);
            alert('Не удалось удалить паттерн');
        }
    }

    async refreshPatternList() {
        try {
            const resp = await fetch('/api/drum/patterns');
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            const patterns = await resp.json();

            const sel = document.getElementById('patternSelect');
            sel.innerHTML = '<option value="">Выберите паттерн…</option>';
            patterns.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p;
                opt.textContent = p;
                sel.appendChild(opt);
            });
        } catch (e) {
            console.error('Ошибка получения списка паттернов:', e);
        }
    }

    async loadSelectedPattern() {
        const sel = document.getElementById('patternSelect');
        const name = sel.value;
        if (!name) return;
        document.getElementById('patternName').value = name;

        try {
            const resp = await fetch(`/api/drum/pattern/${name}`);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

            this.pattern = await resp.json();
            this.renderGrid();
        } catch (e) {
            console.error('Ошибка загрузки выбранного паттерна:', e);
        }
    }

    /* ------------------------------------------------------------------------
       UI – обработчики UI‑элементов
       ------------------------------------------------------------------------ */
    setBPM(val) {
        this.bpm = val;
        if (this.isPlaying) {
            this.stopPattern();
            this.playPattern();
        }
    }

    setupEventListeners() {
        // BPM‑слайдер
        const bpmSlider = document.getElementById('bpm');
        const bpmVal = document.getElementById('bpmValue');
        if (bpmSlider && bpmVal) {
            bpmSlider.addEventListener('input', () => {
                this.setBPM(parseInt(bpmSlider.value, 10));
                bpmVal.textContent = this.bpm;
            });
        }
    }
}

/* ------------------------------------------------------------------------
   Инициализация после загрузки DOM
   ------------------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', () => {
    // Создаём один глобальный экземпляр
    window.drumSequencer = new DrumSequencer();

    /* Глобальные функции, которые вызываются из HTML */
    window.playPattern          = () => drumSequencer.playPattern();
    window.savePattern          = () => drumSequencer.savePattern();
    window.loadPattern          = () => drumSequencer.loadPattern();
    window.deletePattern        = () => drumSequencer.deletePattern();
    window.clearPattern        = () => drumSequencer.clearPattern();
    window.refreshPatternList  = () => drumSequencer.refreshPatternList();
    window.loadSelectedPattern = () => drumSequencer.loadSelectedPattern();
});
