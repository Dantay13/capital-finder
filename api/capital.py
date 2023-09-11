from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL to get the query parameters
        url_components = parse.urlsplit(self.path)
        print("URL components:", url_components)
        query_params = dict(parse.parse_qsl(url_components.query))
        print("Query parameters:", query_params)

        # Base URL for the REST Countries API
        base_api_url = "https://restcountries.com/v3.1/"

        # Check if 'country' is in the query parameters
        if 'country' in query_params:
            country_name = query_params['country']
            response = requests.get(base_api_url + "name/" + country_name)
            if response.status_code == 200:
                data = response.json()
                capital = data[0]['capital'][0]
                message = f"The capital of {country_name.title()} is {capital}."
            else:
                message = f"Country named {country_name.title()} not found."

        # Check if 'capital' is in the query parameters
        elif 'capital' in query_params:
            capital_name = query_params['capital']
            response = requests.get(base_api_url + "capital/" + capital_name)
            if response.status_code == 200:
                data = response.json()
                country = data[0]['name']['common']
                message = f"{capital_name.title()} is the capital of {country}."
            else:
                message = f"Capital named {capital_name.title()} not found."

        else:
            message = "Please provide a valid 'country' or 'capital' in the query parameters."

        # Send the response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())


if __name__ == '__main__':
    server_address = ('localhost', 3000)  # use any available port
    httpd = HTTPServer(server_address, handler)  # httpd is a commonly used abbreviation for "HTTP Daemon"
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()