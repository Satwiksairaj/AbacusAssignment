// ===== Abacus Game State =====
const gameState = {
    beads: {
        10000: 0,
        1000: 0,
        100: 0,
        10: 0,
        1: 0
    },
    targetNumber: 0
};

const PLACE_VALUES = [10000, 1000, 100, 10, 1];
const MAX_BEADS = 9;

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    console.log('Initializing...');
    setupButtons();
    generateTarget();
    render();
    console.log('Initialized');
}

function setupButtons() {
    console.log('Setting up buttons...');

    // Add button handlers
    document.querySelectorAll('.add-btn').forEach(btn => {
        btn.onclick = function () {
            const place = parseInt(this.dataset.place);
            console.log('Adding bead to:', place);
            addBeadAtPlace(place);
            render();
        };
    });

    // Remove button handlers
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.onclick = function () {
            const place = parseInt(this.dataset.place);
            console.log('Removing bead from:', place);
            if (gameState.beads[place] > 0) {
                gameState.beads[place]--;
            }
            render();
        };
    });

    // New Question button
    const newBtn = document.getElementById('newQuestionBtn');
    if (newBtn) {
        newBtn.onclick = function () {
            console.log('New question');
            PLACE_VALUES.forEach(p => gameState.beads[p] = 0);
            generateTarget();
            render();
        };
    }

    console.log('Buttons setup complete');
}

function addBeadAtPlace(place) {
    gameState.beads[place]++;

    // Handle carry over
    if (gameState.beads[place] > MAX_BEADS) {
        gameState.beads[place] = 0;
        const index = PLACE_VALUES.indexOf(place);
        if (index > 0) {
            const nextPlace = PLACE_VALUES[index - 1];
            console.log('Carrying over to:', nextPlace);
            addBeadAtPlace(nextPlace);
        }
    }
}

function generateTarget() {
    gameState.targetNumber = Math.floor(Math.random() * 100000);
    const target = document.getElementById('targetNumber');
    if (target) {
        target.textContent = gameState.targetNumber;
        console.log('Target:', gameState.targetNumber);
    }
}

function render() {
    console.log('Current beads state:', gameState.beads);

    // Update beads for each rod
    PLACE_VALUES.forEach(place => {
        const container = document.querySelector(`.rod-wrapper[data-place="${place}"] .beads-area`);
        if (!container) {
            console.error('Container not found for place:', place);
            return;
        }

        container.innerHTML = '';
        for (let i = 0; i < gameState.beads[place]; i++) {
            const bead = document.createElement('div');
            bead.className = 'bead';
            container.appendChild(bead);
        }
    });

    // Update current value
    let value = 0;
    PLACE_VALUES.forEach(place => {
        value += place * gameState.beads[place];
    });

    const valueEl = document.getElementById('currentValue');
    if (valueEl) {
        valueEl.textContent = value;
        console.log('Current value:', value);
    }

    // Update status
    const statusEl = document.getElementById('statusMessage');
    if (statusEl) {
        if (value === gameState.targetNumber) {
            statusEl.textContent = '✅ You matched the number!';
            statusEl.style.color = '#059669';
        } else {
            statusEl.textContent = 'Keep adjusting the beads.';
            statusEl.style.color = '#92400e';
        }
    }
}
