document.addEventListener('DOMContentLoaded', () => {
    const customerForm = document.getElementById('contact-form');

    customerForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission
        console.log('hi');
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        const requestData = {
            name: name,
            email: email,
            message: message,
        };

        const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

        try {
            const response = await fetch('/contact/', { // Make sure the URL matches your API endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Set Content-Type to JSON
                    'X-CSRFToken': csrfToken, // Include CSRF token for security
                },
                body: JSON.stringify(requestData), // Convert the data to JSON
            });

            if (response.ok) {
                const result = await response.json();
                alert('Message sent successfully!');
                console.log(result);
                window.location.href = '/contact/'; // Redirect after successful submission
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error || 'Message submission failed!'}`);
            }
        } catch (error) {
            console.error('Error during message submission:', error);
            alert('An unexpected error occurred. Please try again later.');
        }
    });
});
