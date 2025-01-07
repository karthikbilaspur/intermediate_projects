// Add event listener to form submit
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    form.addEventListener("submit", function(event) {
        // Prevent default form submission behavior
        event.preventDefault();

        // Get form data
        const ipRange = document.querySelector("input[name='ip-range']").value;
        const scanType = document.querySelector("select[name='scan-type']").value;

        // Send AJAX request to server
        fetch("/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ipRange: ipRange,
                scanType: scanType
            })
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    });
});