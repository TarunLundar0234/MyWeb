# Location Tracker

A simple web application that captures the location of anyone who opens the link and saves it to a `loc.txt` file on the server.

## Features

- 📍 Automatically requests location when page is opened
- 💾 Saves location data to `loc.txt` file
- 🗺️ Includes Google Maps link for each location
- 📱 Works on desktop and mobile browsers
- 🎨 Clean, modern UI

## Setup

### Option 1: Python (Recommended if you don't have Node.js)

1. Start the server:
   ```bash
   python server.py
   ```

2. The server will run on `http://localhost:3000`

### Option 2: Node.js

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the server:
   ```bash
   npm start
   ```

3. The server will run on `http://localhost:3000`

## Usage

1. Share the link `http://localhost:3000` with anyone
2. When they open it, their location will be captured (they must allow location access)
3. Location data is saved to `loc.txt` in the project folder
4. View all saved locations at `http://localhost:3000/view-locations`

## What Gets Saved

Each location entry includes:
- Latitude and Longitude
- Accuracy (in meters)
- Timestamp
- User Agent (browser/device info)
- IP Address
- Direct Google Maps link

## Notes

- Users must grant permission for location access in their browser
- HTTPS is recommended for production (geolocation works best with HTTPS)
- For public access, you'll need to deploy this to a server or use a service like ngrok for testing

## Security Warning

⚠️ This application tracks user locations. Always:
- Inform users that their location is being tracked
- Comply with privacy laws (GDPR, etc.)
- Secure the `loc.txt` file appropriately
- Use HTTPS in production
