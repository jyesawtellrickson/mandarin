import scrapy
import json

class musixmatchSpider(scrapy.Spider):
    name = 'musixmatch'

    def start_requests(self):
        # Start by authenticating.
        # Start by accessing homepage for list of cities.
        url = 'https://api.musixmatch.com/ws/1.1/track.search?' \
            + 'format=jsonp&callback=callback&f_lyrics_language=zh&' \
            + 'quorum_factor=1&page_size=100&page=1&' \
            + 'apikey=3694cddce3a65fcfc72e43dc143cf717'
        request = scrapy.Request(
            url, self.parse_track_list,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        yield request

    @staticmethod
    def remove_query_part(url):
        return url.split('?')[0]

    def parse_track_list(self, response):
        res = json.loads(response.css('::text').extract_first())
        # Check result returned correctly.
        result = res.get('body').get('trackList')
        if result is not None:
            # Check if last page.
            for track in result:
                url = 'https://api.musixmatch.com/ws/1.1/track.lyrics.get?' \
                 + 'format=jsonp&callback=callback&track_id={track_id}&' \
                 + 'apikey=3694cddce3a65fcfc72e43dc143cf717' \
                 .replace('{track_id}', str(track.get('track_id')))
                request = scrapy.Request(url, self.parse_track,
                                     headers={'User-Agent': 'Mozilla/5.0'}
                                     )
                request.meta['track_name'] = result.get('track_name')
                yield request

    def parse_track(self, response):
        res = json.loads(response.css('::text').extract_first())
        # Check result returned correctly.
        result = res.get('body').get('lyrics')
        track = {'lyrics': result.get('lyrics_body'),
                  'title': response.meta['track_name']}
        yield track
