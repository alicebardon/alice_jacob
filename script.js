const apiKey = 'luma-4ddd7418-c15f-4bc9-ad91-14bf52bef1e8-5f250147-e74e-409c-9969-4ecd6c740087'; // Replace with your actual API key

document.getElementById('generateBtn').addEventListener('click', generateImage);

function generateImage() {
    const options = {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            prompt: 'A serene lake surrounded by mountains at sunset',
            aspect_ratio: '16:9',
            loop: false
        })
    };

    fetch('https://api.lumalabs.ai/dream-machine/v1/generations', options)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            checkGenerationStatus(data.id);
        })
        .catch(err => console.error('Error:', err));
}

function checkGenerationStatus(id) {
    const statusOptions = {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'authorization': `Bearer ${apiKey}`
        }
    };

    const checkStatus = setInterval(() => {
        fetch(`https://api.lumalabs.ai/dream-machine/v1/generations/${id}`, statusOptions)
            .then(response => response.json())
            .then(data => {
                console.log('Status:', data.status);
                if (data.status === 'finished') {
                    clearInterval(checkStatus);
                    displayResult(data);
                }
            })
            .catch(err => console.error('Error:', err));
    }, 5000); // Check every 5 seconds
}

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    if (data.assets && data.assets.image_url) {
        resultDiv.innerHTML = `<img src="${data.assets.image_url}" alt="Generated Image">`;
    } else {
        resultDiv.innerHTML = 'Image generation failed or no image URL available.';
    }
}
