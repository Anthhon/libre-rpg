// Generate stars VFX in login form
(function generateStars() {
    const container = document.getElementById('stars');
    const configs = [
        { count: 40, minSize: 1, maxSize: 1.5, minOp: 0.03, maxOp: 0.2, minDur: 3, maxDur: 6 },
        { count: 20, minSize: 1.5, maxSize: 2.5, minOp: 0.05, maxOp: 0.35, minDur: 4, maxDur: 8 },
        { count: 8,  minSize: 2,   maxSize: 3.5, minOp: 0.08, maxOp: 0.5,  minDur: 5, maxDur: 10 },
    ];
    configs.forEach(({ count, minSize, maxSize, minOp, maxOp, minDur, maxDur }) => {
        for (let i = 0; i < count; i++) {
            const s = document.createElement('div');
            s.className = 'star';
            const size = minSize + Math.random() * (maxSize - minSize);
            s.style.cssText = `
            width:${size}px; height:${size}px;
            left:${Math.random()*100}%; top:${Math.random()*100}%;
            --min-op:${minOp}; --max-op:${maxOp};
            --dur:${(minDur + Math.random()*(maxDur-minDur)).toFixed(1)}s;
            --delay:-${(Math.random()*maxDur).toFixed(1)}s;
          `;
            container.appendChild(s);
        }
    });
})();

// Toggle password visibility in login form
function togglePassword() {
    const input  = document.getElementById('input-password');
    const icon   = document.getElementById('eye-icon');
    const isHidden = input.type === 'password';

    input.type = isHidden ? 'text' : 'password';

    // Toggle icon
    icon.innerHTML = isHidden
        ? `<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/>
       <path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/>
       <line x1="1" y1="1" x2="23" y2="23"/>`
        : `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
       <circle cx="12" cy="12" r="3"/>`;
}
