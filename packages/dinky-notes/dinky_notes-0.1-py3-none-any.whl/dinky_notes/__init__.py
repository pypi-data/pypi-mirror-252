import pluggy
import requests
import textwrap
from PIL import Image, ImageFont, ImageDraw

from dinky.layouts.layout_configuration import Zone

hookimpl = pluggy.HookimplMarker("dinky")

class DinkyNotesPlugin:
    primary_color = "#2a9d8f"

    def __init__(self, url: str):
        self.url = url

    def _get_notes(self):
        r = requests.get(
            url=self.url,
        )
        return r.text


    @hookimpl
    def dinky_draw_zone(self, zone: Zone):
        notes = self._get_notes()
        im = Image.new('RGB', (zone.width, zone.height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        fnt_header = ImageFont.truetype("arial.ttf", 36)
        fnt_regular = ImageFont.truetype("arial.ttf", 14)
        draw.rectangle((zone.padding, zone.padding, zone.width-zone.padding, zone.padding + 55), fill=self.primary_color)
        draw.text((zone.padding + 5, zone.padding + 5), "Notes", font=fnt_header, fill="white")
        wrapper = textwrap.TextWrapper(width=int(0.15 * (zone.width - 2 * zone.padding)), drop_whitespace=False, replace_whitespace=False, subsequent_indent='    ')
        draw.multiline_text((zone.padding + 5, zone.padding + 5 + 55), wrapper.fill(notes), font=fnt_regular, fill="black")
        return im