// Add event listener to document
document.addEventListener('DOMContentLoaded', function() {
    // Get all book elements
    const books = document.querySelectorAll('li');

    // Add event listener to each book
    books.forEach(book => {
        book.addEventListener('click', function() {
            // Get book title
            const title = book.textContent;

            // Create alert message
            alert(`You clicked on: ${title}`);
        });
    });
});