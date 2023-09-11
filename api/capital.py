from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import urllib.parse


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the query parameters
        query = urllib.parse.urlparse(self.path).query
        query_params = urllib.parse.parse_qs(query)

        # Interact with the REST Countries API
        response = requests.get("https://restcountries.com/v3.1/all")
        countries = response.json()

        # Find the country or capital based on the query
        message = "Not found"
        if "country" in query_params:
            country_name = query_params["country"][0].capitalize()
            for country in countries:
                if country_name in country["name"]["common"]:
                    capital = country["capital"][0]
                    message = f"The capital of {country_name} is {capital}"
                    break
        elif "capital" in query_params:
            capital_name = query_params["capital"][0]
            for country in countries:
                if capital_name in country["capital"]:
                    country_name = country["name"]["common"]
                    message = f"{capital_name} is the capital of {country_name}"
                    break

        # Send the response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())
