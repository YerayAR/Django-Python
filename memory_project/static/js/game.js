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
    
    // Update phase information
    if (data.phase) {
        updatePhase(data.phase);
    }
    
    if (data.win) {
        document.getElementById('message').style.display = 'block';
    }
}

function updatePhase(phase) {
    const phaseElement = document.getElementById('current-phase');
    const instructionElement = document.getElementById('instruction-text');
    const startMemorizingBtn = document.getElementById('start-memorizing');
    const startPlayingBtn = document.getElementById('start-playing');
    
    switch(phase) {
        case 'setup':
            phaseElement.textContent = 'Setup';
            instructionElement.textContent = 'Click "Start Memorizing" to see all the cards and memorize their positions.';
            startMemorizingBtn.style.display = 'block';
            startPlayingBtn.style.display = 'none';
            break;
        case 'memorizing':
            phaseElement.textContent = 'Memorizing';
            instructionElement.textContent = 'Memorize the positions of all cards. When ready, click "Start Playing".';
            startMemorizingBtn.style.display = 'none';
            startPlayingBtn.style.display = 'block';
            break;
        case 'playing':
            phaseElement.textContent = 'Playing';
            instructionElement.textContent = 'Click on cards to find matching pairs. Use your memory!';
            startMemorizingBtn.style.display = 'none';
            startPlayingBtn.style.display = 'none';
            break;
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

function startMemorizing() {
    fetch('/start-memorizing/')
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
        });
}

function startPlaying() {
    fetch('/start-playing/')
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
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
    
    document.getElementById('start-memorizing').addEventListener('click', startMemorizing);
    document.getElementById('start-playing').addEventListener('click', startPlaying);
});
