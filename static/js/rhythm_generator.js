document.addEventListener("DOMContentLoaded", () => {
    const tracks = ['hihat', 'snare', 'kick'];
    const canvas = document.getElementById('notationCanvas');
    const ctx = canvas.getContext('2d');

    // Инициализация дорожек
    tracks.forEach(trackId => {
        const track = document.getElementById(trackId);
        for (let i = 0; i < 16; i++) {
            const cell = document.createElement('div');
            cell.dataset.index = i;
            cell.addEventListener('click', () => {
                cell.classList.toggle('selected');
                drawNotation();
            });
            track.appendChild(cell);
        }
    });

    function drawNotation() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const hihat = getSelectedCells('hihat');
        const snare = getSelectedCells('snare');
        const kick = getSelectedCells('kick');

        drawTrackNotes(hihat, 180); // Верхняя дорожка
        drawTrackNotes(snare, 100); // Средняя
        drawTrackNotes(kick, 20);   // Нижняя
    }

    function getSelectedCells(trackId) {
        const cells = document.querySelectorAll(`#${trackId} .selected`);
        return Array.from(cells).map(cell => parseInt(cell.dataset.index));
    }

    function drawTrackNotes(selected, yPos) {
        if (selected.length === 0) return;

        // Простой пример: рисуем шестнадцатые ноты
        selected.forEach(index => {
            const x = 50 + index * 40;
            drawSixteenthNote(x, yPos);
        });
    }

    function drawSixteenthNote(x, y) {
        // Головка
        ctx.beginPath();
        ctx.ellipse(x, y, 6, 3, 0, 0, Math.PI * 2);
        ctx.fill();

        // Штиль
        ctx.beginPath();
        ctx.moveTo(x + 6, y - 10);
        ctx.lineTo(x + 6, y + 10);
        ctx.stroke();

        // Флажки
        ctx.beginPath();
        ctx.moveTo(x + 6, y - 10);
        ctx.lineTo(x + 12, y - 15);
        ctx.moveTo(x + 6, y - 8);
        ctx.lineTo(x + 12, y - 13);
        ctx.stroke();
    }
});
