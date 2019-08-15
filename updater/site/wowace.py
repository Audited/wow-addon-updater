import re

import requests

from updater.site.abstract_site import AbstractSite


class WoWAce(AbstractSite):
    _URL = 'https://www.wowace.com/projects/'

    def __init__(self, url: str):
        super().__init__(url)

    @classmethod
    def get_supported_urls(cls):
        return [cls._URL]

    def find_zip_url(self):
        return self.url + '/files/latest'

    def get_latest_version(self):
        try:
            page = requests.get(self.url + '/files')
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            # the first one encountered will be the WoW retail version
            version = re.search(
                r"project-file-name-container.+?data-id=.+?data-name=\"(?P<version>.+?)\"",
                content_string).group('version')
            return version
        except Exception:
            print(f"Failed to find version number for: {self.url}")
            raise