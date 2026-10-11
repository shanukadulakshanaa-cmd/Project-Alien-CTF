/**
 * A.R.G.U.S. Threat Assessment Interface
 * Client-side effects: Matrix rain, terminal typing, and UI interactions.
 */

// ─── Matrix Rain Effect ─────────────────────────────────────────────
(function initMatrixRain() {
    const canvas = document.getElementById('matrix-rain');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Matrix characters (mix of Latin, katakana-like, and symbols)
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZアイウエオカキクケコサシスセソ0123456789@#$%^&*()+=<>◆◇▸▹△▽';
    const charArray = chars.split('');

    const fontSize = 14;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = new Array(columns).fill(1);

    function draw() {
        // Fade previous frame
        ctx.fillStyle = 'rgba(6, 6, 16, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff41';
        ctx.font = `${fontSize}px monospace`;

        for (let i = 0; i < drops.length; i++) {
            const char = charArray[Math.floor(Math.random() * charArray.length)];
            const x = i * fontSize;
            const y = drops[i] * fontSize;

            ctx.fillText(char, x, y);

            // Reset drop to top with random probability
            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }

    // Recalculate columns on resize
    window.addEventListener('resize', () => {
        columns = Math.floor(canvas.width / fontSize);
        drops = new Array(columns).fill(1);
    });

    setInterval(draw, 50);
})();


// ─── Terminal Typing Effect ─────────────────────────────────────────
function typeText(element, text, speed = 30) {
    return new Promise(resolve => {
        let i = 0;
        element.textContent = '';
        function type() {
            if (i < text.length) {
                element.textContent += text[i];
                i++;
                setTimeout(type, speed);
            } else {
                resolve();
            }
        }
        type();
    });
}


// ─── Glitch Text Effect ────────────────────────────────────────────
function glitchText(element, duration = 200) {
    const original = element.textContent;
    const glitchChars = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`';
    let iterations = 0;
    const maxIterations = duration / 50;

    const interval = setInterval(() => {
        element.textContent = original
            .split('')
            .map((char, idx) => {
                if (idx < iterations) return original[idx];
                return glitchChars[Math.floor(Math.random() * glitchChars.length)];
            })
            .join('');

        iterations += 1;

        if (iterations > original.length || iterations > maxIterations) {
            element.textContent = original;
            clearInterval(interval);
        }
    }, 50);
}


// ─── Animate Elements on Scroll / Load ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Animate threat cards with staggered entrance
    const cards = document.querySelectorAll('.threat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + index * 100);
    });

    // Glitch effect on card titles on hover
    cards.forEach(card => {
        const title = card.querySelector('.card-title');
        if (title) {
            card.addEventListener('mouseenter', () => {
                glitchText(title, 150);
            });
        }
    });

    // Animate stage sections
    const sections = document.querySelectorAll('.stage-section');
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(15px)';
        setTimeout(() => {
            section.style.transition = 'all 0.4s ease';
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, 200 + index * 120);
    });

    // Animate status bar counters
    const statusValues = document.querySelectorAll('.status-value');
    statusValues.forEach(val => {
        const text = val.textContent;
        val.style.opacity = '0';
        setTimeout(() => {
            val.style.transition = 'opacity 0.5s ease';
            val.style.opacity = '1';
        }, 300);
    });

    // Animate progress bar
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        const targetWidth = progressFill.style.width;
        progressFill.style.width = '0%';
        setTimeout(() => {
            progressFill.style.width = targetWidth;
        }, 500);
    }

    // Auto-dismiss flash messages
    const flashMsgs = document.querySelectorAll('.flash-msg');
    flashMsgs.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'all 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
});


// ─── Sound Effects (Web Audio API) ──────────────────────────────────
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function playBeep(frequency = 800, duration = 100, volume = 0.05) {
    try {
        if (!audioCtx) audioCtx = new AudioCtx();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
        gainNode.gain.setValueAtTime(volume, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration / 1000);
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + duration / 1000);
    } catch (e) {
        // Audio not supported or blocked — silently fail
    }
}

function playSuccess() {
    playBeep(523, 100, 0.04);
    setTimeout(() => playBeep(659, 100, 0.04), 120);
    setTimeout(() => playBeep(784, 200, 0.04), 240);
}

function playError() {
    playBeep(200, 200, 0.03);
    setTimeout(() => playBeep(150, 300, 0.03), 200);
}
