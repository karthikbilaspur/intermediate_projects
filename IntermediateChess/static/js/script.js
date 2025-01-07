let selectedCell = null;
let gameState = null;

fetch('/board')
    .then(response => response.json())
    .then(data => {
        gameState = data;
        updateBoard();
    });

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('cell')) {
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);

        if (selectedCell) {
            fetch('/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ start: selectedCell, end: [row, col] })
            })
            .then(response => response.json())
            .then(data => {
                gameState = data;
                updateBoard();
            });
            selectedCell = null;
        } else {
            selectedCell = [row, col];
        }
    }
});

function updateBoard() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell) => {
        const row = parseInt(cell.dataset.row);
        const col = parseInt(cell.dataset.col);
        const piece = gameState[row][col];

        cell.innerHTML = '';
        if (piece) {
            const img = document.createElement('img');
            img.src = `/piece/${piece}`;
            cell.appendChild(img);
        }
    });
}

function undoMove() {
    fetch('/undo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        gameState = data;
        updateBoard();
    });
}

function redoMove() {
    fetch('/redo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        gameState = data;
        updateBoard();
    });
}

function getValidMoves(start) {
    fetch('/get-valid-moves', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: start })
    })
    .then(response => response.json())
    .then(data => {
        const validMoves = data;
        const cells = document.querySelectorAll('.cell');
        cells.forEach((cell) => {
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);
            if (validMoves.some((move) => move[0] === row && move[1] === col)) {
                cell.classList.add('valid-move');
            } else {
                cell.classList.remove('valid-move');
            }
        });
    });
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('cell')) {
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        getValidMoves([row, col]);
    }
});

document.getElementById('undo-btn').addEventListener('click', undoMove);
document.getElementById('redo-btn').addEventListener('click', redoMove);
