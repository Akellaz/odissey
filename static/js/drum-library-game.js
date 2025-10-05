/* --------------------------------------------------------------
   Drum Sequencer – базовая версия только с snare
   --------------------------------------------------------------*/

class DrumSequencer {
    constructor() {
        /* ---------- Настройки ---------- */
        this.track = 'snare';     // только один трек
        this.steps = 16;          // количество шагов (16‑16‑th нот)
        this.bpm   = 60;         // начальное BPM

        /* ---------- Состояние ---------- */
        this.pattern       = new Array(this.steps).fill(0); // простой массив для одного трека
        this.isPlaying     = false;            // сейчас играет?
        this.currentStep   = 0;                // текущий шаг во время воспроизведения
        this.intervalId    = null;             // ID setInterval
        this.audioContext  = null;             // Web Audio API context
        this.samples       = {};               // загруженные AudioBuffer‑ы
        this.audioReady    = false;            // true, когда все сэмплы загружены

        /* ---------- Инициализация ---------- */
        this.renderGrid();        // визуальная сетка
        this.setupEventListeners();

        // сразу начинаем загрузку звуков
        this.initAudio();
    }

    /* ------------------------------------------------------------------------
       AUDIO – инициализация и загрузка сэмплов
       ------------------------------------------------------------------------ */
    async initAudio() {
        try {
            this.audioContext = new (window.AudioContext ||
                                   window.webkitAudioContext)();

            // Загружаем только snare
            const url = '/static/sounds/snare.wav';
            console.log('Загрузка snare...');

            const resp = await fetch(url);
            if (!resp.ok) {
                throw new Error(`HTTP ${resp.status}`);
            }
            const arrayBuf = await resp.arrayBuffer();
            this.samples.snare = await this.audioContext.decodeAudioData(arrayBuf);
            console.log('✔️ snare загружен');
            
            this.audioReady = true;
            console.log('Сэмпл готов к использованию');
        } catch (e) {
            console.error('Ошибка загрузки аудио:', e);
        }
    }

    playSound(name) {
        if (!this.audioReady) {
            console.warn('Звук ещё не загружен');
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
       GRID – работа с визуализацией
       ------------------------------------------------------------------------ */
    renderGrid() {
        const grid = document.getElementById('drumGrid');
        if (!grid) {
            console.error('#drumGrid элемент не найден в DOM');
            return;
        }
        grid.innerHTML = '';

        const row = document.createElement('div');
        row.className = 'track-row';

        const nameDiv = document.createElement('div');
        nameDiv.className = 'track-name';
        nameDiv.textContent = this.track;
        row.appendChild(nameDiv);

        const stepsDiv = document.createElement('div');
        stepsDiv.className = 'track-steps';

        this.pattern.forEach((v, i) => {
            const stepDiv = document.createElement('div');
            stepDiv.className = `step ${v ? 'active' : ''}`;
            
            // Добавляем класс для выделения групп по 4
            const groupIndex = Math.floor(i / 4);
            stepDiv.classList.add(`group-${groupIndex % 4}`);
            
            stepDiv.dataset.step = i;
            stepDiv.textContent = v ? '●' : '';
            stepDiv.addEventListener('click', () => this.toggleStep(i));
            stepsDiv.appendChild(stepDiv);
        });

        row.appendChild(stepsDiv);
        grid.appendChild(row);
    }

    // Добавляем недостающий метод
    toggleStep(step) {
        this.pattern[step] = this.pattern[step] ? 0 : 1;
        this.renderGrid();
    }

    /* ------------------------------------------------------------------------
       PLAYBACK – воспроизведение
       ------------------------------------------------------------------------ */
    playPattern() {
        if (this.isPlaying) {
            this.stopPattern();
            return;
        }

        // Если контекст был «заморожен», разблокируем его
        if (this.audioContext && this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }

        if (!this.audioReady) {
            alert('Звук ещё не загружен. Пожалуйста, подождите.');
            return;
        }

        this.isPlaying = true;
        document.getElementById('playButton').textContent = 'Стоп';

        const stepTime = (60 / this.bpm) / 4 * 1000; // 16‑ти нотный шаг

        this.intervalId = setInterval(() => {
            this.highlightStep(this.currentStep);

            // Играем snare если активен
            if (this.pattern[this.currentStep]) {
                this.playSound(this.track);
            }

            this.currentStep = (this.currentStep + 1) % this.steps;
        }, stepTime);
    }

    stopPattern() {
        this.isPlaying = false;
        clearInterval(this.intervalId);
        document.getElementById('playButton').textContent = 'Проиграть';
        this.clearHighlights();
        this.currentStep = 0;
    }

    highlightStep(step) {
        this.clearHighlights();
        const cell = document.querySelector(`.step[data-step="${step}"]`);
        if (cell) cell.classList.add('playing');
    }

    clearHighlights() {
        const cells = document.querySelectorAll('.step.playing');
        cells.forEach(c => c.classList.remove('playing'));
    }

    clearPattern() {
        this.pattern = new Array(this.steps).fill(0);
        this.renderGrid();
        this.stopPattern();
    }

    /* ------------------------------------------------------------------------
       UI – обработчики элементов
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
    window.drumSequencer = new DrumSequencer();

    // Глобальные функции для HTML
    window.playPattern = () => drumSequencer.playPattern();
    window.clearPattern = () => drumSequencer.clearPattern();
});
