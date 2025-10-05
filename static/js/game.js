const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const messageDiv = document.getElementById('message');

const noteDurations = {
    "quarter": {name: "Четвертная", beats: 1},
    "eighth_pair": {name: "Восьмые", beats: 1},
    "sixteenth_quartet": {name: "Шестнадцатые", beats: 1},
    "sixteenth_pair_eighth": {name: "Две шестнадцатых + восьмая", beats: 2},
    "eighth_sixteenth_pair": {name: "Восьмая + две шестнадцатых", beats: 2},
    "sixteenth_eighth_sixteenth": {name: "Шестнадцатая + восьмая + шестнадцатая", beats: 2}
};

let currentNotes = [];
let selectedNoteTypes = new Set([
    'quarter', 
    'eighth_pair', 
    'sixteenth_quartet', 
    'sixteenth_pair_eighth',
    'eighth_sixteenth_pair',
    'sixteenth_eighth_sixteenth'
]);

// Функция для выбора/отмены выбора типа нот
function toggleNoteType(noteType) {
    const noteNames = {
        "quarter": "Четвертная",
        "eighth_pair": "Восьмые",
        "sixteenth_quartet": "Шестнадцатые",
        "sixteenth_pair_eighth": "2 шестнадцатых + восьмая",
        "eighth_sixteenth_pair": "Восьмая + две шестнадцатых",
        "sixteenth_eighth_sixteenth": "Шестнадцатая + восьмая + шестнадцатая"
    };
    
    const elements = document.querySelectorAll('.note-group');
    elements.forEach(element => {
        if (element.textContent.includes(noteNames[noteType])) {
            if (selectedNoteTypes.has(noteType)) {
                selectedNoteTypes.delete(noteType);
                element.classList.remove('selected');
            } else {
                selectedNoteTypes.add(noteType);
                element.classList.add('selected');
            }
        }
    });
}

// Выбрать все типы нот
function selectAll() {
    selectedNoteTypes = new Set([
        'quarter', 
        'eighth_pair', 
        'sixteenth_quartet', 
        'sixteenth_pair_eighth',
        'eighth_sixteenth_pair',
        'sixteenth_eighth_sixteenth'
    ]);
    const elements = document.querySelectorAll('.note-group');
    elements.forEach(element => element.classList.add('selected'));
}

// Снять выбор со всех типов нот
function deselectAll() {
    selectedNoteTypes.clear();
    const elements = document.querySelectorAll('.note-group');
    elements.forEach(element => element.classList.remove('selected'));
}

// Класс для рисования нот
class MusicNotes {
    constructor(ctx) {
        this.ctx = ctx;
        this.ovalWidth = 16;
        this.ovalHeight = 10;
        this.stemHeight = 55;
        this.lineY = 190;
    }
    
    clear() {
        this.ctx.clearRect(0, 0, canvas.width, canvas.height);
        this.drawStaff();
    }
    
    drawStaff() {
        const y = 150;
        this.ctx.strokeStyle = '#333';
        this.ctx.lineWidth = 1;
        for (let i = 0; i < 5; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(50, y + i * 20);
            this.ctx.lineTo(750, y + i * 20);
            this.ctx.stroke();
        }
    }
    
    // Четвертная нота
    drawQuarterNote(x, y, color = 'black') {
        const stemTopY = this.lineY - this.stemHeight;
        const stemX = x + this.ovalWidth;
        
        this.ctx.beginPath();
        this.ctx.moveTo(stemX, this.lineY - 5);
        this.ctx.lineTo(stemX, stemTopY);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.ellipse(x, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
        this.ctx.fillStyle = color;
        this.ctx.fill();
    }
    
    // Пара восьмых нот
    drawEighthPair(x, y, color = 'black') {
        const stemTopY = this.lineY - this.stemHeight;
        const stemX1 = x - 8 + this.ovalWidth;
        const stemX2 = x + 48 + this.ovalWidth;
        const beamY = stemTopY + 5;
        
        this.ctx.beginPath();
        this.ctx.moveTo(stemX1, this.lineY - 5);
        this.ctx.lineTo(stemX1, beamY);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.ellipse(x - 8, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
        this.ctx.fillStyle = color;
        this.ctx.fill();
        
        this.ctx.beginPath();
        this.ctx.moveTo(stemX2, this.lineY - 5);
        this.ctx.lineTo(stemX2, beamY);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.ellipse(x + 48, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
        this.ctx.fillStyle = color;
        this.ctx.fill();
        
        this.ctx.beginPath();
        this.ctx.moveTo(stemX1, beamY);
        this.ctx.lineTo(stemX2, beamY);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
    }
    
    // Четверка шестнадцатых нот
    drawSixteenthQuartet(x, y, color = 'black') {
        const stemTopY = this.lineY - this.stemHeight;
        const beamY1 = stemTopY + 5;
        const beamY2 = stemTopY + 20;
        const ovalPositions = [-8, 24, 56, 88];
        const stemPositions = ovalPositions.map(pos => pos + this.ovalWidth);
        
        for (let i = 0; i < 4; i++) {
            const ovalX = x + ovalPositions[i];
            const stemX = x + stemPositions[i];
            
            this.ctx.beginPath();
            this.ctx.moveTo(stemX, this.lineY - 5);
            this.ctx.lineTo(stemX, stemTopY);
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = color;
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.ellipse(ovalX, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
        }
        
        this.ctx.beginPath();
        this.ctx.moveTo(x + stemPositions[0], beamY1);
        this.ctx.lineTo(x + stemPositions[3], beamY1);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(x + stemPositions[0], beamY2);
        this.ctx.lineTo(x + stemPositions[3], beamY2);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        for (let i = 0; i < 4; i++) {
            const stemX = x + stemPositions[i];
            this.ctx.beginPath();
            this.ctx.moveTo(stemX, beamY1);
            this.ctx.lineTo(stemX, beamY2);
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = color;
            this.ctx.stroke();
        }
    }
    
    // Две шестнадцатых + одна восьмая
    drawSixteenthPairEighth(x, y, color = 'black') {
        const stemTopY = this.lineY - this.stemHeight;
        const beamY1 = stemTopY + 5;
        const beamY2 = stemTopY + 20;
        const eighthBeamY = stemTopY + 5;
        
        const ovalPositions = [0, 32, 80];
        const stemPositions = ovalPositions.map(pos => pos + this.ovalWidth);
        
        for (let i = 0; i < 3; i++) {
            const ovalX = x + ovalPositions[i];
            const stemX = x + stemPositions[i];
            
            this.ctx.beginPath();
            this.ctx.moveTo(stemX, this.lineY - 5);
            this.ctx.lineTo(stemX, stemTopY);
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = color;
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.ellipse(ovalX, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
        }
        
        const firstStemX = x + stemPositions[0];
        const secondStemX = x + stemPositions[1];
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY1);
        this.ctx.lineTo(secondStemX, beamY1);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY2);
        this.ctx.lineTo(secondStemX, beamY2);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        for (let i = 0; i < 2; i++) {
            const stemX = x + stemPositions[i];
            this.ctx.beginPath();
            this.ctx.moveTo(stemX, beamY1);
            this.ctx.lineTo(stemX, beamY2);
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = color;
            this.ctx.stroke();
        }
        
        const thirdStemX = x + stemPositions[2];
        this.ctx.beginPath();
        this.ctx.moveTo(thirdStemX, eighthBeamY);
        this.ctx.lineTo(secondStemX, eighthBeamY);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
    }
    
    // Восьмая + две шестнадцатых
    drawEighthSixteenthPair(x, y, color = 'black') {
        const stemTopY = this.lineY - this.stemHeight;
        const beamY1 = stemTopY + 5;
        const beamY2 = stemTopY + 20;
        
        const positions = [32, 64, 96];
        const ovalPositions = [16, 48, 80];
        const stemPositions = positions;
        
        for (let i = 0; i < 3; i++) {
            const ovalX = x + ovalPositions[i];
            const stemX = x + stemPositions[i];
            
            this.ctx.beginPath();
            this.ctx.moveTo(stemX, this.lineY - 5);
            this.ctx.lineTo(stemX, stemTopY);
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = color;
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.ellipse(ovalX, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
        }
        
        const firstStemX = x + stemPositions[0];
        const secondStemX = x + stemPositions[1];
        const thirdStemX = x + stemPositions[2];
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY1);
        this.ctx.lineTo(thirdStemX, beamY1);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(secondStemX, beamY2);
        this.ctx.lineTo(thirdStemX, beamY2);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY1);
        this.ctx.lineTo(firstStemX, beamY2 - 15);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(secondStemX, beamY1);
        this.ctx.lineTo(secondStemX, beamY2);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(thirdStemX, beamY1);
        this.ctx.lineTo(thirdStemX, beamY2);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
    }
    
    // Шестнадцатая + восьмая + шестнадцатая
    drawSixteenthEighthSixteenth(x, y, color = 'black') {
        const stemTopY = this.lineY - this.stemHeight;
        const beamY1 = stemTopY + 5;
        const beamY2 = stemTopY + 20;
        
        const positions = [16, 48, 96];
        const ovalPositions = [0, 32, 80];
        const stemPositions = positions;
        
        for (let i = 0; i < 3; i++) {
            const ovalX = x + ovalPositions[i];
            const stemX = x + stemPositions[i];
            
            this.ctx.beginPath();
            this.ctx.moveTo(stemX, this.lineY - 5);
            this.ctx.lineTo(stemX, stemTopY);
            this.ctx.lineWidth = 2;
            this.ctx.strokeStyle = color;
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.ellipse(ovalX, this.lineY, this.ovalWidth, this.ovalHeight, 0, 0, 2 * Math.PI);
            this.ctx.fillStyle = color;
            this.ctx.fill();
        }
        
        const firstStemX = x + stemPositions[0];
        const secondStemX = x + stemPositions[1];
        const thirdStemX = x + stemPositions[2];
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY1);
        this.ctx.lineTo(thirdStemX, beamY1);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY2);
        this.ctx.lineTo(firstStemX + 16, beamY2);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(thirdStemX - 16, beamY2);
        this.ctx.lineTo(thirdStemX, beamY2);
        this.ctx.lineWidth = 5;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(firstStemX, beamY1);
        this.ctx.lineTo(firstStemX, beamY2);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(secondStemX, beamY1);
        this.ctx.lineTo(secondStemX, beamY2 - 15);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(thirdStemX, beamY1);
        this.ctx.lineTo(thirdStemX, beamY2);
        this.ctx.lineWidth = 2;
        this.ctx.strokeStyle = color;
        this.ctx.stroke();
    }
    
    drawNote(noteType, x, y) {
        switch(noteType) {
            case 'quarter':
                this.drawQuarterNote(x, y);
                break;
            case 'eighth_pair':
                this.drawEighthPair(x, y);
                break;
            case 'sixteenth_quartet':
                this.drawSixteenthQuartet(x, y);
                break;
            case 'sixteenth_pair_eighth':
                this.drawSixteenthPairEighth(x, y);
                break;
            case 'eighth_sixteenth_pair':
                this.drawEighthSixteenthPair(x, y);
                break;
            case 'sixteenth_eighth_sixteenth':
                this.drawSixteenthEighthSixteenth(x, y);
                break;
        }
    }
}

const notes = new MusicNotes(ctx);

function newQuestion() {
    currentNotes = [];
    messageDiv.textContent = "";
    messageDiv.className = "";
    
    // Проверяем, есть ли выбранные типы нот
    if (selectedNoteTypes.size === 0) {
        messageDiv.textContent = "Пожалуйста, выберите хотя бы один тип нот!";
        messageDiv.className = "incorrect";
        return;
    }
    
    // Генерируем 4 случайные группы нот из выбранных типов
    const noteKeys = Array.from(selectedNoteTypes);
    const positions = [120, 280, 440, 600];
    
    for (let i = 0; i < 4; i++) {
        const noteType = noteKeys[Math.floor(Math.random() * noteKeys.length)];
        currentNotes.push({
            type: noteType,
            position: positions[i],
            beats: noteDurations[noteType].beats
        });
    }
    
    drawNotes();
}

function drawNotes() {
    notes.clear();
    
    // Рисуем все 4 группы нот на третьей линии
    for (let i = 0; i < currentNotes.length; i++) {
        const note = currentNotes[i];
        switch(note.type) {
            case 'eighth_pair':
                notes.drawNote(note.type, note.position - 32, 0);
                break;
            case 'sixteenth_quartet':
                notes.drawNote(note.type, note.position - 48, 0);
                break;
            case 'sixteenth_pair_eighth':
                notes.drawNote(note.type, note.position - 40, 0);
                break;
            case 'eighth_sixteenth_pair':
                notes.drawNote(note.type, note.position - 48, 0);
                break;
            case 'sixteenth_eighth_sixteenth':
                notes.drawNote(note.type, note.position - 48, 0);
                break;
            default:
                notes.drawNote(note.type, note.position, 0);
                break;
        }
    }
}

// Инициализация выбора
selectAll();
