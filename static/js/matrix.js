const canvas = document.getElementById("matrixCanvas");
const ctx = canvas.getContext("2d");

// Make canvas full screen
canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

// Characters (mix of numbers + letters)
const letters = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const fontSize = 16;
const columns = canvas.width / fontSize;

// Array for drops
const drops = [];

// Initialize drops
for (let i = 0; i < columns; i++) {
    drops[i] = Math.random() * canvas.height;
}

function draw() {
    // Dark fade effect (motion blur)
    ctx.fillStyle = "rgba(0, 0, 0, 0.08)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#00ff99";  // green color
    ctx.font = fontSize + "px monospace";

    for (let i = 0; i < drops.length; i++) {

        const text = letters.charAt(Math.floor(Math.random() * letters.length));

        // Random blur effect
        if (Math.random() > 0.98) {
            ctx.fillStyle = "#00ffaa";
        } else {
            ctx.fillStyle = "#008f5a";
        }

        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        // Reset drop randomly
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }

        drops[i]++;
    }
}

// Animation speed (not too fast)
setInterval(draw, 40);

// Responsive resize
window.addEventListener("resize", () => {
    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;
});