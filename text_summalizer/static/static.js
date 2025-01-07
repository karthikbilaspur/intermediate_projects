// URL input validation
document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.querySelector('input[type="url"]');
    urlInput.addEventListener('input', function() {
        if (!this.value.match(/^https?:\/\//)) {
            this.setCustomValidity('Invalid URL');
        } else {
            this.setCustomValidity('');
        }
    });
});

// Summarization method selection
document.addEventListener('DOMContentLoaded', function() {
    const methodSelect = document.querySelector('select[name="method"]');
    methodSelect.addEventListener('change', function() {
        console.log(`Selected method: ${this.value}`);
    });
});

// Sentiment analysis visualization
function visualizeSentiment(sentiment) {
    const sentimentContainer = document.querySelector('.sentiment-container');
    sentimentContainer.innerHTML = `
        <p>Positive: ${sentiment.pos}</p>
        <p>Negative: ${sentiment.neg}</p>
        <p>Neutral: ${sentiment.neu}</p>
        <p>Compound: ${sentiment.compound}</p>
    `;
}

// Error message handling
function displayError(message) {
    const errorContainer = document.querySelector('.error-container');
    errorContainer.innerHTML = `<p>${message}</p>`;
}

// About page animation
document.addEventListener('DOMContentLoaded', function() {
    const aboutButton = document.querySelector('a[href="/about"]');
    aboutButton.addEventListener('click', function(event) {
        event.preventDefault();
        const aboutContainer = document.querySelector('.about-container');
        aboutContainer.classList.toggle('animate');
        setTimeout(() => {
            window.location.href = '/about';
        }, 500);
    });
});