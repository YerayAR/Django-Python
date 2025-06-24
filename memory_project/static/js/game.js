function updateBoard(data) {
    const board = document.getElementById('board');
    const cards = board.getElementsByClassName('card');
    for (let i = 0; i < cards.length; i++) {
        const card = cards[i];
        const state = data.states[i];
        if (state === 0) {
            card.textContent = '';
            card.classList.remove('matched');
        } else {
            card.textContent = data.cards[i];
            if (state === 2) {
                card.classList.add('matched');
            }
        }
    }
    document.getElementById('moves').textContent = 'Moves: ' + data.moves;
    if (data.win) {
        document.getElementById('message').style.display = 'block';
    }
}

function fetchFlip(index) {
    fetch('/flip/' + index + '/')
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
            if (data.mismatch) {
                setTimeout(() => {
                    fetch('/flip/-1/')
                        .then(r => r.json())
                        .then(updateBoard);
                }, 1000);
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => {
            const index = card.getAttribute('data-index');
            fetchFlip(index);
        });
    });
    document.getElementById('restart').addEventListener('click', () => {
        window.location.href = '/restart/';
    });
});
