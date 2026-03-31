document.getElementById('committeeForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Here you can handle the form data as needed
    const formData = new FormData(this);
    
    // Example: Log the form data to the console
    for (let [key, value] of formData.entries()) {
        console.log(key, value);
    }

    // You can also send the form data to a server using fetch or XMLHttpRequest
    // fetch('your-server-endpoint', {
    //     method: 'POST',
    //     body: formData
    // })
    // .then(response => response.json())
    // .then(data => console.log(data))
    // .catch(error => console.error('Error:', error));
});