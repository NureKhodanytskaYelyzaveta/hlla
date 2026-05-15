const Profile = {
    populateForm(user) {
        document.getElementById('profile-fullName').value = user.fullName || '';
        document.getElementById('profile-email').value = user.email || '';
        document.getElementById('profile-password').value = '';
    },

    init() {
        document.getElementById('profile-form')
            .addEventListener('submit', (e) => this.handleSubmit(e));
    },

    handleSubmit(event) {
        event.preventDefault();

        const currentUser = Storage.get(APP_CONFIG.storage.CURRENT_USER);
        if (!currentUser) return;

        const newFullName = document.getElementById('profile-fullName').value.trim();
        const newEmail = document.getElementById('profile-email').value.trim();
        const newPassword = document.getElementById('profile-password').value;

        currentUser.fullName = newFullName;
        currentUser.email = newEmail;
        if (newPassword) {
            currentUser.password = newPassword;
        }

        const users = Storage.get(APP_CONFIG.storage.USERS, []);
        const index = users.findIndex(u => u.username === currentUser.username);
        
        if (index !== -1) {
            users[index] = currentUser;
            Storage.set(APP_CONFIG.storage.USERS, users);
        }

        Storage.set(APP_CONFIG.storage.CURRENT_USER, currentUser);
        
        document.getElementById('username-display').textContent = currentUser.username;
        
        alert('✅ Профіль оновлено!');
    }
};

Profile.init();