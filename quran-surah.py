import http.server
import socketserver
import requests

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def get_api_quran(self):
        response = requests.get('https://api.alquran.cloud/v1/surah')
        data = response.json()

        html = '<html>'
        html += '<head>'
        html += '<meta charset="UTF-8">'
        html += '</head>'
        html += '<body>'
        html += '<ul>'
        for surah in data['data']:
            html += '<li>'
            html += f"Number: {surah['number']}<br>"
            html += f"Name: {surah['name']}<br>"
            html += f"English Name: {surah['englishName']}<br>"
            html += f"English Name Translation: {surah['englishNameTranslation']}<br>"
            html += f"Number of Ayahs: {surah['numberOfAyahs']}<br>"
            html += f"Revelation Type: {surah['revelationType']}<br>"
            html += '</li>'
        html += '</ul>'

        return html.encode('utf-8')

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('charset', 'utf-8')
            self.end_headers()
            self.wfile.write(self.get_api_quran())
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", 8000), MyRequestHandler) as httpd:
    print("Server started on port 8000")
    httpd.serve_forever()