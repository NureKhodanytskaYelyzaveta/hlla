const Reviews = {
    init() {
        const form = document.getElementById('review-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    },

    handleSubmit(event) {
        event.preventDefault();

        const product = document.getElementById('review-product').value.trim();
        const text = document.getElementById('review-text').value.trim();
        const isBadQuality = document.getElementById('review-bad').checked;

        const currentUser = Storage.get(APP_CONFIG.storage.CURRENT_USER);

        if (!product || !text) {
            alert('Заповніть всі поля');
            return;
        }

        const newReview = {
            id: Date.now(),
            product,
            text,
            isBadQuality,
            username: currentUser?.username || 'Анонім',
            date: new Date().toLocaleDateString('uk-UA')
        };

        const reviews = Storage.get(APP_CONFIG.storage.REVIEWS, []);
        reviews.unshift(newReview);
        Storage.set(APP_CONFIG.storage.REVIEWS, reviews);

        event.target.reset();
        this.render();
    },

    render() {
        const container = document.getElementById('reviews-list');
        const reviews = Storage.get(APP_CONFIG.storage.REVIEWS, []);

        if (!container) return;

        if (reviews.length === 0) {
            container.innerHTML = '<p style="color:#666">Відгуків ще немає</p>';
            return;
        }

        container.innerHTML = reviews.map(r => this.createCard(r)).join('');
    },

    createCard(review) {
        return `
            <div class="review-card ${review.isBadQuality ? 'bad-quality' : ''}">
                <div class="review-header">
                    <strong>${this.escapeHtml(review.product)}</strong>
                    <span>${review.date}</span>
                </div>

                <div class="review-text">
                    ${this.escapeHtml(review.text)}
                </div>

                ${
                    review.isBadQuality
                        ? '<div class="review-warning">⚠️ Позначено як неякісний</div>'
                        : ''
                }
            </div>
        `;
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};