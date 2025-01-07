const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const resultsDiv = document.getElementById('results');

searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value.trim();
    if (query) {
        fetch(`/scrape?query=${query}`)
            .then((response) => response.json())
            .then((data) => {
                resultsDiv.innerHTML = '';
                data.forEach((result) => {
                    const resultDiv = document.createElement('div');
                    resultDiv.classList.add('result');
                    resultDiv.innerHTML = `
                        <div class="name">${result.name}</div>
                        <div class="address">${result.address}</div>
                    `;
                    resultsDiv.appendChild(resultDiv);
                });
            })
            .catch((error) => console.error(error));
    }
});