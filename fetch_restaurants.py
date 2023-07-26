import gzip
import json
import io
import http.client
from html.parser import HTMLParser


class NextDataParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            for attr in attrs:
                if attr[0] == "id" and attr[1] == "__NEXT_DATA__":
                    self.reading_script = True

    def handle_endtag(self, tag):
        if self.reading_script and tag == "script":
            self.reading_script = False

    def handle_data(self, data):
        if self.reading_script:
            self.script_content = data

    def clear(self):
        self.reading_script = False
        self.script_content = None


conn = http.client.HTTPSConnection("www.nyctourism.com")
conn.request(
    "GET",
    "/restaurant-week",
    headers={"Accept-Encoding": "gzip, deflate, br"},
)
res = conn.getresponse()
assert res.status == 200

data = res.read()
html_data = gzip.GzipFile(fileobj=io.BytesIO(data))
html_text = html_data.read().decode("utf-8")
parser = NextDataParser()
parser.clear()
parser.feed(html_text)
assert parser.script_content

next_data = json.loads(parser.script_content)
restaurants = next_data["props"]["pageProps"]["page"]["programParticipants"]

with open("./restaurants.json", "w") as f:
    json.dump(restaurants, f, indent=2, sort_keys=False)
