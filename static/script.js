// ===== COMMON THEME & PARTICLE LOGIC =====

const themes = [
    { primary: '#00ff88', secondary: '#00ccff', bg: '#050510' }, 
    { primary: '#ff0055', secondary: '#ffcc00', bg: '#1a0505' }, 
    { primary: '#cc00ff', secondary: '#00ffee', bg: '#0a051a' }  
];
let currentTheme = 0;

// Atmosphere theme handling (Used by themeOrb only, doesn't override default light/dark)
// Change Theme
function changeTheme() {
    currentTheme = (currentTheme + 1) % themes.length;
    const theme = themes[currentTheme];
    const root = document.documentElement;

    root.style.setProperty('--primary', theme.primary);
    root.style.setProperty('--secondary', theme.secondary);
    root.style.setProperty('--bg-deep', theme.bg);
    
    document.body.style.backgroundColor = theme.bg;
    initParticles(); 
}

// Attach theme toggle
document.addEventListener('DOMContentLoaded', () => {
    const themeOrb = document.getElementById('themeOrb');
    if (themeOrb) {
        themeOrb.addEventListener('click', changeTheme);
    }
    initParticles();
    
    // Settings dropdown (dashboard)
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsDropdown = document.getElementById('settingsDropdown');
    if (settingsBtn && settingsDropdown) {
        settingsBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const visible = settingsDropdown.classList.toggle('visible');
            settingsBtn.setAttribute('aria-expanded', visible);
            settingsDropdown.setAttribute('aria-hidden', !visible);
        });

        // Close dropdown on outside click
        document.addEventListener('click', (e) => {
            if (!settingsDropdown.classList.contains('visible')) return;
            if (!settingsDropdown.contains(e.target) && e.target !== settingsBtn) {
                settingsDropdown.classList.remove('visible');
                settingsBtn.setAttribute('aria-expanded', 'false');
                settingsDropdown.setAttribute('aria-hidden', 'true');
            }
        });
    }
});

// ===== PARTICLE SYSTEM =====
const canvas = document.getElementById('constellation');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    let mouse = { x: null, y: null, radius: 150 };

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.x;
        mouse.y = e.y;
    });

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.size = Math.random() * 2;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--primary');
            ctx.fill();
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0 || this.x > width) this.vx = -this.vx;
            if (this.y < 0 || this.y > height) this.vy = -this.vy;

            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx*dx + dy*dy);

            if (distance < mouse.radius) {
                const forceDirectionX = dx / distance;
                const forceDirectionY = dy / distance;
                const force = (mouse.radius - distance) / mouse.radius;
                this.vx += forceDirectionX * force * 0.6;
                this.vy += forceDirectionY * force * 0.6;
            }
            this.vx *= 0.98; 
            this.vy *= 0.98;
            this.draw();
        }
    }

    function initParticles() {
        particles = [];
        let numberOfParticles = (width * height) / 9000;
        for (let i = 0; i < numberOfParticles; i++) {
            particles.push(new Particle());
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, width, height);
        for (let a = 0; a < particles.length; a++) {
            for (let b = a; b < particles.length; b++) {
                let dx = particles[a].x - particles[b].x;
                let dy = particles[a].y - particles[b].y;
                let distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--secondary') + '44';
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.stroke();
                }
            }
            particles[a].update();
        }
    }

    initParticles();
    animate();
}

// ===== POPUP & REDIRECT FUNCTIONS =====

function showSuccessPopup() {
    const successPopup = document.getElementById('successPopup');
    if (successPopup) {
        successPopup.classList.remove('hidden');
        
        // Auto redirect after 3 seconds
        setTimeout(() => {
            redirectToDashboard();
        }, 3000);
    }
}

function redirectToDashboard() {
    const successPopup = document.getElementById('successPopup');
    const greenOverlay = document.getElementById('greenOverlay');
    
    if (successPopup) successPopup.classList.add('hidden');
    if (greenOverlay) greenOverlay.classList.remove('hidden');
    
    // Redirect after green overlay animation (1 second)
    setTimeout(() => {
        window.location.href = 'dashboard.html';
    }, 1000);
}
