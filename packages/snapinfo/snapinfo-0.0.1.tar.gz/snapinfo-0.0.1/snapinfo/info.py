import requests
from bs4 import BeautifulSoup
import json

class SnapInfo:
    def __init__(self):
        self.session = requests.Session()

    def get_info(self, user):
        url = 'https://www.snapchat.com/add/' + user
        response = self.session.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            script_tag = soup.find('script', {'type': 'application/json'})

            if script_tag:
                data = json.loads(script_tag.string)
                username = data.get('props', {}).get('pageProps', {}).get('userProfile', {}).get('userInfo', {}).get('username')
                display_name = data.get('props', {}).get('pageProps', {}).get('userProfile', {}).get('userInfo', {}).get('displayName')
                bitmoji_url = data.get('props', {}).get('pageProps', {}).get('userProfile', {}).get('userInfo', {}).get('bitmoji3d', {}).get('avatarImage', {}).get('url')

                info_dict = {
                    'username': username,
                    'display_name': display_name,
                    'bitmoji_url': bitmoji_url
                }

                return info_dict
            else:
                raise ValueError('No JSON data found.')
        else:
            raise ConnectionError(f'Failed to fetch data. Status code: {response.status_code}')