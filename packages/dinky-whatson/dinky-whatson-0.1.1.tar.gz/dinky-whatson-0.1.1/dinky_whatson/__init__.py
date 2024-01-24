from bs4 import BeautifulSoup
import pluggy
import requests
import json
import textwrap
from datetime import date
from PIL import Image, ImageFont, ImageDraw
import pkg_resources
from io import BytesIO

from dinky.layouts.layout_configuration import Zone

hookimpl = pluggy.HookimplMarker("dinky")

class DinkyWhatsOnPlugin:
    primary_color: str = "#e76f51"

    def __init__(self, suburb: str):
        self.suburb = suburb

    def _get_events(self):
        r = requests.get(
            url=f'https://whatson.cityofsydney.nsw.gov.au/suburbs/{self.suburb.lower()}'
        )
        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup.select_one('script#__NEXT_DATA__')
        data = json.loads(script.contents[0])
        events = data['props']['pageProps']['events']['hits']
        todays_events = list(filter(lambda event: event.get('upcomingDate') == date.today().isoformat(), events))
        return todays_events


    @hookimpl
    def dinky_draw_zone(self, zone: Zone):
        events = self._get_events()
        im = Image.new('RGB', (zone.width, zone.height), (255, 255, 255))
        draw = ImageDraw.Draw(im)

        font_data = pkg_resources.resource_stream('dinky_whatson', 'fonts/Roboto-Regular.ttf')
        font_bytes = BytesIO(font_data.read())
        font_header = ImageFont.truetype(font_bytes, 36)
        font_bytes.seek(0)
        font_regular = ImageFont.truetype(font_bytes, 14)
        font_data = pkg_resources.resource_stream('dinky_whatson', 'fonts/Roboto-Bold.ttf')
        font_bytes = BytesIO(font_data.read())
        font_title = ImageFont.truetype(font_bytes, 14)

        draw.rectangle((zone.padding, zone.padding, zone.width-zone.padding, zone.padding + 55), fill=self.primary_color)
        draw.text((zone.padding + 5, zone.padding + 5), f"What's On", font=font_header, fill="white")
        for i, event in enumerate(events):
            wrapper = textwrap.TextWrapper(width=int(0.15 * (zone.width - 2 * zone.padding)), max_lines=1)
            draw.text((zone.padding + 5, 55 + zone.padding + 5 + (55 * i)), wrapper.fill(event["name"]), font=font_title, fill=self.primary_color)
            wrapper = textwrap.TextWrapper(width=int(0.15 * (zone.width - 2 * zone.padding)), max_lines=2)
            draw.multiline_text((zone.padding + 5, 55 + zone.padding + 5 + (55 * i) + 18), wrapper.fill(event["strapline"]), font=font_regular, fill="black")
        return im