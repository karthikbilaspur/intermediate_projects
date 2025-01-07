document.getElementById('send-email-btn').addEventListener('click', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const language = document.getElementById('language').value;

    fetch('/send_email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password, language })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error(error));
});