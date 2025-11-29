from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import os

PORT = int(os.environ.get('PORT', 8080))  # Use Render's PORT or default to 8080

class LocationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Remove query parameters from path
        path = self.path.split('?')[0]
        
        if path == '/' or path == '':
            # Serve the HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        
        elif path == '/view-locations':
            # Show saved locations
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            if os.path.exists('loc.txt'):
                with open('loc.txt', 'r') as file:
                    self.wfile.write(file.read().encode())
            else:
                self.wfile.write(b'No locations recorded yet.')
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/save-location':
            # Read the posted data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            location_data = json.loads(post_data.decode('utf-8'))
            
            # Create log entry
            log_entry = f"""
========================================
Timestamp: {location_data.get('timestamp')}
Latitude: {location_data.get('latitude')}
Longitude: {location_data.get('longitude')}
Accuracy: {location_data.get('accuracy')} meters
Altitude: {location_data.get('altitude', 'N/A')}
Altitude Accuracy: {location_data.get('altitudeAccuracy', 'N/A')}
Heading: {location_data.get('heading', 'N/A')}
Speed: {location_data.get('speed', 'N/A')}
User Agent: {location_data.get('userAgent')}
IP Address: {self.client_address[0]}
Google Maps Link: https://www.google.com/maps?q={location_data.get('latitude')},{location_data.get('longitude')}
========================================

"""
            
            # Save to file
            try:
                with open('loc.txt', 'a') as file:
                    file.write(log_entry)
                
                print(f"Location saved: {location_data.get('latitude')}, {location_data.get('longitude')}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': True, 'message': 'Location saved successfully'}
                self.wfile.write(json.dumps(response).encode())
            
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'error': str(e)}
                self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_error(404)

def run(server_class=HTTPServer, handler_class=LocationHandler, port=PORT):
    server_address = ('0.0.0.0', port)  # Listen on all interfaces for Render
    httpd = server_class(server_address, handler_class)
    print(f'Server is running on port {port}')
    print(f'View saved locations at: /view-locations')
    print('Press Ctrl+C to stop the server')
    print('\nKeep this window open to keep the server running!')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')

if __name__ == '__main__':
    run()
