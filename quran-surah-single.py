import http.server
import socketserver
import requests
from urllib.parse import urlparse, parse_qs

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):

    def add_css(self,text):
        text += ("<style>"
                 "body {"
                 "    font-family: Arial, sans-serif;text-align: center;"
                 "    background-color: #f1f1f1;"
                 "}"
                 "h1 {"
                 "    color: #3b82f6;"
                 "}"
                 "label {"
                 "    display: block;"
                 "    margin-bottom: 5px;"
                 "}"
                 "input[type='number'] {"
                 "    width: 50px;"
                 "    padding: 5px;"
                 "    border: 1px solid #ccc;"
                 "}"
                 "input[type='submit'] {"
                 "    padding: 5px 10px;"
                 "    background-color: #4CAF50;"
                 "    color: white;"
                 "    border: none;"
                 "    cursor: pointer;"
                 "}"
                "</style>")
        return text

    def get_api_quran(self):
        parsed_url   = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if query_params.get('number_surah', [''])[0] :
            number_surah = query_params['number_surah'][0]
        else:
            number_surah = "1"

        response     = requests.get('https://api.alquran.cloud/v1/surah/'+number_surah)
        data         = response.json()
        html = '<html>'
        html += '<head>'
        html += '<meta charset="UTF-8">'
        html += self.add_css(html)
        html += '</head>'
        html += '<body>'
        html += '<div style="padding: 10px;background: #cfcecd;">'
        html += f"<h1><span style='color: #ff0000;'>شماره سوره</span>:   {data['data']['number']}</h1>"
        html += f"<h1><span style='color: #ff0000;'>نام سوره</span>: {data['data']['name']}</h1>"
        html += f"<p><span style='color: #ff0000;'>english name</span>:  {data['data']['englishName']}</p>"
        html += f"<p><span style='color: #ff0000;'>تعداد آیه</span>: {data['data']['numberOfAyahs']}</p>"
        html += '</div>'


        html += "<form>"
        html += "<label for='number_surah'>شماره سوره</label>"
        html += "<input type='number' id='number_surah' name='number_surah' min='1' max='114' value='1'>"
        html += "<input type='submit' value='Submit'>"
        html += "</form>"


        html += '</body>'
        html += '</html>'

        return html.encode('utf-8')

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('charset', 'utf-8')
        self.end_headers()
        self.wfile.write(self.get_api_quran())


        return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", 8000), MyRequestHandler) as httpd:
    print("Server started on port 8000")
    httpd.serve_forever()