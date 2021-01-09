class Video:

    def __init__(self, url):
        self.url = url

    def serialize(self):
        return {
            "url" : self.url
        }
        
    def from_json(self, json_):
        self.url = json_["url"]


