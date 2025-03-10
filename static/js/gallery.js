
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('editphoto-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent default form submission

        const formData = new FormData(form);

        fetch('', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Photo edited successfully!'); // Success message
                form.reset(); // Reset the form after successful submission
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('addphoto-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent default form submission

        const formData = new FormData(form);

        fetch('', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Photo added successfully!'); // Success message
                form.reset(); // Reset the form after successful submission
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

