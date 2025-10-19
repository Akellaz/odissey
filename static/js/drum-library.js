/* --------------------------------------------------------------
   Drum Sequencer – полная версия с локальными звуками (WAV) и отображением нот
   --------------------------------------------------------------*/

class DrumSequencer {
    constructor() {
        /* ---------- Настройки ---------- */
        this.tracks = ['hihat', 'snare', 'kick', 'tom3', 'tom1']; // убран tom2
        this.steps  = 16;                     // количество шагов (16‑16‑th нот)
        this.bpm    = 120;                    // начальное BPM

        /* ---------- Состояние ---------- */
        this.pattern       = {};               // объект pattern[track][step] = 0/1
        this.isPlaying     = false;            // сейчас играет?
        this.currentStep   = 0;                 // текущий шаг во время воспроизведения
        this.intervalId    = null;             // ID setInterval
        this.audioContext  = null;             // Web Audio API context
        this.samples       = {};               // загруженные AudioBuffer‑ы
        this.audioReady    = false;            // true, когда все сэмплы загружены

        /* ---------- Инициализация ---------- */
        this.initPattern();       // пустой паттерн
        this.renderGrid();        // визуальная сетка
        this.setupEventListeners();
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
                tom3:    '/static/sounds/openhat.wav',
                tom1:    '/static/sounds/tom1.wav'
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
                stepDiv.className = `step ${v ? 'active' : ''} group-${Math.floor(i/4)}`;
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
        this.renderNotes(); // Обновляем нотный стан при каждом изменении
    }

    /* ------------------------------------------------------------------------
       NOTES – отображение нот на нотном стане
       ------------------------------------------------------------------------ */
    renderNotes() {
        const notesContainer = document.getElementById('notesContainer');
        if (!notesContainer) return;

        // Очищаем контейнер
        notesContainer.innerHTML = '';

        // Создаем нотный стан
        const staffContainer = document.createElement('div');
        staffContainer.className = 'staff-container';
        staffContainer.innerHTML = `
            <div class="staff-header">
                <h3>Нотный стан</h3>
                <button onclick="window.drumSequencer.clearPattern()">Очистить</button>
            </div>
            <div class="staff" id="staff">
                ${this.renderStaffLines()}
            </div>
        `;

        notesContainer.appendChild(staffContainer);

        // Рендерим ноты
        this.renderNotesOnStaff();
    }

    renderStaffLines() {
        // Создаем 5 линий нотного стана как в примере
        let staffHTML = '';
        for (let i = 0; i < 5; i++) {
            staffHTML += `<div class="staff-line"></div>`;
        }
        return staffHTML;
    }

    renderNotesOnStaff() {
        const staff = document.getElementById('staff');
        if (!staff) return;

        // Очищаем существующие ноты
        const existingNotes = staff.querySelectorAll('.note, .hihat-note');
        existingNotes.forEach(note => note.remove());

        // Маппинг барабанов на позиции нот (на третьей линии как в примере)
        const trackToPosition = {
            'hihat': 60,    // над третьей линией
            'snare': 40,    // на третьей линии
            'kick': 20,     // под третьей линией
            'tom3': 30,     // между второй и третьей
            'tom1': 50      // между третьей и четвертой
        };

        // Создаем ноты для каждого шага
        for (let step = 0; step < this.steps; step++) {
            this.tracks.forEach(track => {
                if (this.pattern[track][step]) {
                    if (track === 'hihat') {
                        // Для hihat создаем крестик
                        const hihatNote = document.createElement('div');
                        hihatNote.className = 'hihat-note';
                        hihatNote.dataset.track = track;
                        hihatNote.dataset.step = step;
                        hihatNote.style.left = `${(step * 40) + 20}px`;
                        hihatNote.style.bottom = `${trackToPosition[track]}%`;
                        hihatNote.title = `${track} на шаге ${step + 1}`;
                        staff.appendChild(hihatNote);
                    } else {
                        // Для остальных создаем обычные ноты
                        const note = document.createElement('div');
                        note.className = 'note';
                        note.dataset.track = track;
                        note.dataset.step = step;
                        note.style.left = `${(step * 40) + 20}px`;
                        note.style.bottom = `${trackToPosition[track]}%`;
                        note.title = `${track} на шаге ${step + 1}`;
                        staff.appendChild(note);
                    }
                }
            });
        }
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
        // Подсвечиваем соответствующие ноты на нотном стане
        this.highlightNotes(step);
    }

    highlightNotes(step) {
        const notes = document.querySelectorAll('.note, .hihat-note');
        notes.forEach(note => {
            const noteStep = parseInt(note.dataset.step);
            if (noteStep === step) {
                note.classList.add('playing');
            } else {
                note.classList.remove('playing');
            }
        });
    }

    clearHighlights() {
        const cells = document.querySelectorAll('.step.playing');
        cells.forEach(c => c.classList.remove('playing'));
        
        const notes = document.querySelectorAll('.note.playing, .hihat-note.playing');
        notes.forEach(n => n.classList.remove('playing'));
    }

    clearPattern() {
        this.initPattern();
        this.renderGrid();
        this.stopPattern();
        this.renderNotes(); // Обновляем нотный стан
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
    window.clearPattern        = () => drumSequencer.clearPattern();
    
    // Инициализируем отображение нот
    setTimeout(() => {
        if (window.drumSequencer) {
            window.drumSequencer.renderNotes();
        }
    }, 100);
});
