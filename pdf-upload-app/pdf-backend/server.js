const express = require('express');
const multer = require('multer');
const pdfParse = require('pdf-parse');
const axios = require('axios');
const cors = require('cors');
const fs = require('fs'); // Import the fs module
require('dotenv').config(); // Load environment variables from .env file

const app = express();
app.use(cors());
app.use(express.json());

// Multer setup for handling file uploads
const upload = multer({ dest: 'uploads/' });

// Route to handle PDF upload and extraction
app.post('/upload-pdf', upload.single('file'), async (req, res) => {
    try {
        // Check if a file was uploaded
        if (!req.file) {
            return res.status(400).send('No file uploaded.');
        }

        // Read the uploaded PDF file as a buffer
        const pdfBuffer = fs.readFileSync(req.file.path);

        // Extract text from the uploaded PDF
        const data = await pdfParse(pdfBuffer);

        // Extracted text from the PDF
        const pdfText = data.text;

        // Send the text to Mistral API to summarize
        const summary = await getMistralSummary(pdfText);

        // Send the summarized text back to the frontend
        res.json({ summary });

        // Optional: Delete the uploaded file after processing
        fs.unlinkSync(req.file.path);
    } catch (error) {
        console.error(error);
        res.status(500).send('An error occurred while processing the PDF.');
    }
});

// Function to send the extracted text to Mistral
async function getMistralSummary(text) {
    try {
        const apiUrl = 'https://api.mistral.ai/v1/chat/completions';
        const response = await axios.post(apiUrl, {
            model: 'mistral-large-latest', // Use the appropriate model
            messages: [
                {
                    role: 'user',
                    content: text, // Pass the extracted PDF text as the user input
                },
            ],
        }, {
            headers: {
                'Authorization': `Bearer ${process.env.MISTRAL_API_KEY}`, // Use the environment variable
                'Content-Type': 'application/json', // Ensure the content type is correct
            }
        });

        // Return the summary from the API response
        return response.data.choices[0].message.content; // Adjust according to the actual response structure
    } catch (error) {
        console.error('Error calling Mistral API:', error.message);
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
        }
        throw new Error('Failed to summarize text with Mistral.');
    } // <- Add this closing brace
}

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
