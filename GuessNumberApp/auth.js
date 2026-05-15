const Auth = {
    isRegisterMode: false,

    init() {
        const currentUser = Storage.get(APP_CONFIG.storage.CURRENT_USER, null);
        if (currentUser) {
            this.showApp(currentUser);
        } else {
            this.showAuth();
        }
        this.bindEvents();
    },


    toggleMode() {
        this.isRegisterMode = !this.isRegisterMode;
        
        document.getElementById('auth-title').textContent = 
            this.isRegisterMode ? 'Реєстрація' : 'Вхід';
        document.getElementById('auth-btn').textContent = 
            this.isRegisterMode ? 'Зареєструватися' : 'Увійти';
        document.getElementById('toggle-text').textContent = 
            this.isRegisterMode ? 'Вже є акаунт?' : 'Немає акаунту?';
        document.getElementById('toggle-link').textContent = 
            this.isRegisterMode ? 'Увійти' : 'Зареєструватися';
        
        document.getElementById('register-fields').classList.toggle('hidden', !this.isRegisterMode);
    },

    handleSubmit(event) {
        event.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            alert('Заповніть логін та пароль');
            return;
        }

        const users = Storage.get(APP_CONFIG.storage.USERS, []);

        if (this.isRegisterMode) {
            if (users.some(u => u.username === username)) {
                alert('Користувач з таким логіном вже існує');
                return;
            }

            const newUser = {
                username,
                password,
                fullName: document.getElementById('fullName').value.trim(),
                email: document.getElementById('email').value.trim(),
                createdAt: new Date().toISOString()
            };

            users.push(newUser);
            Storage.set(APP_CONFIG.storage.USERS, users);
            
            alert('Реєстрація успішна! Тепер увійдіть.');
            this.toggleMode();
        } else {
            const user = users.find(u => 
                u.username === username && u.password === password
            );

            if (user) {
                Storage.set(APP_CONFIG.storage.CURRENT_USER, user);
                this.showApp(user);
            } else {
                alert('Неправильний логін або пароль');
            }
        }
    },

    logout() {
        Storage.remove(APP_CONFIG.storage.CURRENT_USER);
        this.showAuth();
    },

    showAuth() {
        document.getElementById('navbar').classList.add('hidden');
        document.getElementById('auth-section').classList.remove('hidden');
        document.getElementById('profile-section').classList.add('hidden');
        document.getElementById('reviews-section').classList.add('hidden');
    },

    showApp(user) {
        document.getElementById('auth-section').classList.add('hidden');
        document.getElementById('navbar').classList.remove('hidden');
        document.getElementById('username-display').textContent = user.username;
        
        Profile.populateForm(user);
        
        showSection('reviews');
        Reviews.render();
    },

    bindEvents() {
        document.getElementById('auth-form')
            .addEventListener('submit', (e) => this.handleSubmit(e));
    }
};

function showSection(sectionId) {
    ['profile', 'reviews'].forEach(id => {
        document.getElementById(`${id}-section`).classList.add('hidden');
    });
    document.getElementById(`${sectionId}-section`).classList.remove('hidden');
}