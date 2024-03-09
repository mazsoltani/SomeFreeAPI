import http.server
import socketserver

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <html>
                <body>
                <img id="image" src="https://php-noise.com/noise.php">
                <button onclick="refreshImage()">Refresh</button>
                <script>
                    function refreshImage() {
                        var image = document.getElementById('image');
                        image.src = "https://php-noise.com/noise.php?" + new Date().getTime();
                    }
                </script>
                </body>
                </html>
            ''')
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", 8000), MyRequestHandler) as httpd:
    print("Server started on port 8000")
    httpd.serve_forever()