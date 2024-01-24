import pluggy
import caldav
from icalendar import Calendar
from dateutil import tz
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
import pkg_resources
from io import BytesIO

from dinky.layouts.layout_configuration import Zone

hookimpl = pluggy.HookimplMarker("dinky")

class DinkyCalendarPlugin:
    primary_color = "#264653"

    def __init__(self, url: str, username: str, password: str, timezone: str):
        self.url = url
        self.username = username
        self.password = password
        self.timezone = timezone

    def _get_todays_events(self):
        today = datetime.now()
        return self._get_events(datetime(today.year, today.month, today.day))

    def _get_events(self, date):
        with caldav.DAVClient(url=self.url, username=self.username, password=self.password) as client:
            cal = client.calendar(url=self.url)
            events = cal.search(
                start=date,
                end=date + timedelta(hours=23, minutes=59, seconds=59),
                event=True,
                expand=True,
                sort_keys=("dtstart", "dtend")
            )

            response = []
            for event in events:
                gcal = Calendar.from_ical(event.data)
                for event in gcal.walk():
                    if event.name == "VEVENT":
                        start_utc = event.get('dtstart').dt
                        end_utc = event.get('dtend').dt
                        if not hasattr(start_utc, "hour") and not hasattr(end_utc, "hour"):
                            time = None
                        else:
                            start_utc = start_utc.replace(tzinfo=tz.gettz('UTC'))
                            start_local = start_utc.astimezone(tz.gettz(self.timezone))
                            end_utc = end_utc.replace(tzinfo=tz.gettz('UTC'))
                            end_local = end_utc.astimezone(tz.gettz(self.timezone))
                            time = f"{start_local.strftime('%H:%M')}-{end_local.strftime('%H:%M')}"
                        response.append({
                            "title": event.get('summary'),
                            "location": event.get('location'),
                            "time": time
                        })
            return response

    @hookimpl
    def dinky_draw_zone(self, zone: Zone):
        im = Image.new('RGB', (zone.width, zone.height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        draw.rectangle((zone.padding, zone.padding, zone.width - zone.padding, zone.padding + 55), fill=self.primary_color)

        font_data = pkg_resources.resource_stream('dinky_calendar', 'fonts/Roboto-Regular.ttf')
        font_bytes = BytesIO(font_data.read())
        font_date = ImageFont.truetype(font_bytes, 36)
        font_bytes.seek(0)
        font_regular = ImageFont.truetype(font_bytes, 14)
        font_data = pkg_resources.resource_stream('dinky_calendar', 'fonts/Roboto-Bold.ttf')
        font_bytes = BytesIO(font_data.read())
        font_weekday = ImageFont.truetype(font_bytes, 24)
        font_bytes.seek(0)
        font_title = ImageFont.truetype(font_bytes, 14)

        today = datetime.today()
        draw.text((zone.padding + 5, zone.padding + 5), today.strftime('%b %d'), font=font_date, fill="white")
        draw.text((zone.width - 60, zone.padding + 5), today.strftime('%a'), font=font_weekday, fill="white")

        events = self._get_todays_events()
        for i, event in enumerate(events):
            draw.text((zone.padding + 5, 55 + zone.padding + 5 + (40 * i)), event["title"], font=font_title, fill=self.primary_color)
            time = event["time"] if event["time"] else ""
            location = f'({event["location"]})' if event['location'] else ""
            draw.text((zone.padding + 5, 55 + zone.padding + 5 + (40 * i) + 18), f'{time} {location}', font=font_regular, fill="black")
        return im
