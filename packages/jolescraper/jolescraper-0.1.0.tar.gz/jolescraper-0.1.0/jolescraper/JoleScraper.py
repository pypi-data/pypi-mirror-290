import requests
import re
from bs4 import BeautifulSoup

class JoleScraper:
    def __init__(self, url : str, tags : list):
        self.url = url
        self.tags = tags

    def request_data(self) -> requests.models.Response:
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Check if the request was successful

            # Print info about the response
            print(f'------ Response status code: {response.status_code}')
            print(f'------ Response URL: {response.url}')

            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
    def process_data(self, response: requests.models.Response) -> str:
        scraped_text = ''

        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.find_all(self.tags)

        for rt in result:
            scraped_text += rt.get_text() + ' '
        
        scraped_text = re.sub(r'\s+', ' ', scraped_text)  # Remove extra spaces

        return scraped_text
