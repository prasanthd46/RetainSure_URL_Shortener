# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata



from dataclasses import dataclass
from datetime import UTC, datetime
import threading

@dataclass
class UrlMapping:
    original_url: str
    created_at: datetime
    clicks: int = 0

class UrlStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.store = {}
        self.url_to_code = {}

    def save(self, code, original_url):
        with self.lock:
            if code not in self.store:
                self.store[code] = UrlMapping(
                    original_url=original_url,
                    created_at=datetime.now(UTC)
                )
            self.url_to_code[original_url] = code

    def get(self, code):
        return self.store.get(code)

    def increment_click(self, code):
        with self.lock:
            if code in self.store:
                self.store[code].clicks += 1

    def exists(self, code):
        return code in self.store

    def find_code_for_url(self, url):
        return self.url_to_code.get(url)

    def get_all_codes(self):
        return list(self.store.keys())

store = UrlStore()