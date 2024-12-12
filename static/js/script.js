function uploadPDF() {
    const fileInput = document.getElementById('pdf-upload');
    const questionsContainer = document.getElementById('questions-container');
    const errorMessage = document.getElementById('error-message');
    const loadingIndicator = document.getElementById('loading');

    // Reset previous state
    questionsContainer.innerHTML = '';
    errorMessage.textContent = '';
    loadingIndicator.style.display = 'block';

    // Check if file is selected
    if (!fileInput.files.length) {
        errorMessage.textContent = 'Please select a PDF file.';
        loadingIndicator.style.display = 'none';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/generate-questions', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingIndicator.style.display = 'none';

        if (data.error) {
            errorMessage.textContent = data.error;
        } else {
            // Display generated questions
            data.questions.forEach((question, index) => {
                const questionElement = document.createElement('div');
                questionElement.classList.add('question');
                questionElement.textContent = `${index + 1}. ${question}`;
                questionsContainer.appendChild(questionElement);
            });
        }
    })
    .catch(error => {
        loadingIndicator.style.display = 'none';
        errorMessage.textContent = 'An error occurred while processing the PDF.';
        console.error('Error:', error);
    });
}