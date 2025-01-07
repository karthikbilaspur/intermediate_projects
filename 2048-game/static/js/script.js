const upBtn = document.getElementById('up-btn');
const downBtn = document.getElementById('down-btn');
const leftBtn = document.getElementById('left-btn');
const rightBtn = document.getElementById('right-btn');
const undoBtn = document.getElementById('undo-btn');
const hintBtn = document.getElementById('hint-btn');
const restartBtn = document.getElementById('restart-btn');

upBtn.addEventListener('click', () => {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'up' }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.game_over) {
            window.location.href = '/game-over';
        } else {
            const tiles = document.querySelectorAll('.tile');
            tiles.forEach((tile, index) => {
                tile.textContent = data.board[Math.floor(index / 4)][index % 4];
            });
        }
    });
});

downBtn.addEventListener('click', () => {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'down' }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.game_over) {
            window.location.href = '/game-over';
        } else {
            const tiles = document.querySelectorAll('.tile');
            tiles.forEach((tile, index) => {
                tile.textContent = data.board[Math.floor(index / 4)][index % 4];
            });
        }
    });
});

leftBtn.addEventListener('click', () => {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'left' }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.game_over) {
            window.location.href = '/game-over';
        } else {
            const tiles = document.querySelectorAll('.tile');
            tiles.forEach((tile, index) => {
                tile.textContent = data.board[Math.floor(index / 4)][index % 4];
            });
        }
    });
});

rightBtn.addEventListener('click', () => {
    fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'right' }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.game_over) {
            window.location.href = '/game-over';
        } else {
            const tiles = document.querySelectorAll('.tile');
            tiles.forEach((tile, index) => {
                tile.textContent = data.board[Math.floor(index / 4)][index % 4];
            });
        }
    });
});

undoBtn.addEventListener('click', () => {
    fetch('/undo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        const tiles = document.querySelectorAll('.tile');
        tiles.forEach((tile, index) => {
            tile.textContent = data.board[Math.floor(index / 4)][index % 4];
        });
    });
});

hintBtn.addEventListener('click', () => {
    fetch('/hint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        const tiles = document.querySelectorAll('.tile');
        tiles.forEach((tile, index) => {
            tile.textContent = data.board[Math.floor(index / 4)][index % 4];
        });
    });
});

restartBtn.addEventListener('click', () => {
    fetch('/restart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = '/';
    });
});