// Base ///////////////////////////////////////////////////////////////////////
// Toggle Sidebar
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
}

// Login page /////////////////////////////////////////////////////////////////

// Toggle password visibility in login form
function togglePassword() {
    const input  = document.getElementById('id_password');
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


// Players list ///////////////////////////////////////////////////////////////
let activeFilter = 'all';

function filterUsers(query) {
    applyFilters(query.toLowerCase().trim(), activeFilter);
}

function setFilter(role, btn) {
    activeFilter = role;
    document.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const query = document.getElementById('userlist-search').value.toLowerCase().trim();
    applyFilters(query, role);
}

function applyFilters(query, role) {
    const cards = document.querySelectorAll('.user-card');
    let visible = 0;

    cards.forEach(card => {
        const name    = card.dataset.name   || '';
        const cardRole= card.dataset.role   || '';
        const online  = card.dataset.online === 'true';

        const matchQuery  = !query  || name.includes(query);
        const matchRole   = role === 'all'
            || role === 'online'  && online
            || role === cardRole;

        if (matchQuery && matchRole) {
            card.classList.remove('hidden');
            visible++;
        } else {
            card.classList.add('hidden');
        }
    });

    // Update counter
    document.getElementById('visible-count').textContent = visible;

    // Toggle search-empty state
    const searchEmpty = document.getElementById('search-empty');
    if (visible === 0 && cards.length > 0) {
        searchEmpty.style.display = 'block';
    } else {
        searchEmpty.style.display = 'none';
    }
}

// Campaigns List /////////////////////////////////////////////////////////////

// Cover image preview
const coverInput = document.querySelector('input[type="file"]');
const coverPreview = document.getElementById('cover-preview');
const coverOverlay = document.getElementById('cover-overlay');
const coverIcon = document.getElementById('cover-placeholder-icon');
const coverText = document.getElementById('cover-upload-text');

coverInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
        coverPreview.src = e.target.result;
        coverPreview.classList.add('visible');
        coverIcon.style.display = 'none';
        coverText.style.display = 'none';
    };
    reader.readAsDataURL(file);
});

// Drag & drop visual feedback
const uploadArea = document.getElementById('cover-upload-area');
uploadArea.addEventListener('dragover', e => { e.preventDefault(); uploadArea.classList.add('dragover'); });
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
uploadArea.addEventListener('drop', () => uploadArea.classList.remove('dragover'));

// Description char counter
const descField = document.getElementById('{{ new_campaign_form.description.id_for_label }}');
const descCounter = document.getElementById('desc-counter');

if (descField && descCounter) {
    descField.addEventListener('input', function () {
        const len = this.value.length;
        descCounter.textContent = `${len} / 128`;
        descCounter.classList.toggle('warn', len > 110);
    });
}
