from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pywhatkit as kit
import datetime
import pyautogui
import time

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            html_content = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>WhatsApp Message Sender</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        padding: 20px;
                    }
                    .container {
                        max-width: 500px;
                        margin: 0 auto;
                        background: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    .container h2 {
                        margin-bottom: 20px;
                    }
                    .container label {
                        display: block;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                    .container input, .container textarea {
                        width: 100%;
                        padding: 10px;
                        margin-bottom: 20px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                    }
                    .container button {
                        background-color: #28a745;
                        color: white;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .container button:hover {
                        background-color: #218838;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>WhatsApp Message Sender</h2>
                    <form id="whatsapp-form">
                        <label for="phone_number">Phone Number:</label>
                        <input type="text" id="phone_number" name="phone_number" required>

                        <label for="message">Message:</label>
                        <textarea id="message" name="message" rows="4" required></textarea>

                        <label for="repeat_count">Repeat Count:</label>
                        <input type="number" id="repeat_count" name="repeat_count" required>

                        <button type="submit">Send Message</button>
                    </form>
                </div>

                <script>
                    document.getElementById("whatsapp-form").addEventListener("submit", function(event) {
                        event.preventDefault();
                        const phone_number = document.getElementById("phone_number").value;
                        const message = document.getElementById("message").value;
                        const repeat_count = document.getElementById("repeat_count").value;

                        fetch("/send_message", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                phone_number: phone_number,
                                message: message,
                                repeat_count: repeat_count
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            alert(data.message);
                        })
                        .catch(error => {
                            console.error("Error:", error);
                        });
                    });
                </script>
            </body>
            </html>
            '''
            self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        if self.path == '/send_message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            phone_number = data['phone_number']
            message_text = data['message']
            repeat_count = int(data['repeat_count'])

            try:
                
                now = datetime.datetime.now()
                current_hour = now.hour
                current_minute = now.minute + 1

                if current_minute >= 60:
                    current_minute = 0
                    current_hour += 1

                    if current_hour >= 24:
                        current_hour = 0

                
                kit.sendwhatmsg(phone_number, message_text, current_hour, current_minute)
                time.sleep(15)  

                
                for _ in range(repeat_count - 1):  
                    pyautogui.typewrite(message_text)
                    pyautogui.press('enter')
                    time.sleep(1)

                response = {
                    'message': 'Messages sent successfully!'
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                response = {
                    'message': f'Failed to send message: {e}'
                }
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
