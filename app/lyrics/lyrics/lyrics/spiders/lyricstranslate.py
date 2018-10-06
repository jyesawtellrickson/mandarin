import scrapy
from urllib.parse import urlparse

class lyricstranslateSpider(scrapy.Spider):
    name = 'lyricstranslate'

    def start_requests(self):
        # Start by authenticating.
        # Start by accessing homepage for list of cities.
        url = 'https://lyricstranslate.com/en/songs/15/none/none?page=1'
        request = scrapy.Request(
            url, self.parse_track_list,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        yield request

    @staticmethod
    def remove_query_part(url):
        return url.split('?')[0]

    @staticmethod
    def page_from_url(url):
        try:
            return int(url.split('=')[1])
        except:
            return None

    def parse_track_list(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)[:-1]
        links = response.xpath('//@href').extract()
        song_links = [l for l in links if l[-11:] == 'lyrics.html']
        next_page = self.page_from_url(response.url) + 1
        follow_links = list(set([l for l in links if l[:9] == '/en/songs'
                        and self.page_from_url(l) == next_page]))
        for l in follow_links:
            request = scrapy.Request(
                domain + l, self.parse_track_list,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            yield request

        for l in song_links:
            request = scrapy.Request(
                domain + l, self.parse_song,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            yield request

    def parse_song(self, response):
        try:
            lyrics = ''.join(response.xpath(
                '//div[@class="song-node-text"]/div/div/div/text()'
            ).extract())
            title = response.xpath(
                '//h2[@class="title-h2"]/text()'
            ).extract_first()
            artist = response.xpath(
                '//li[@class="song-node-info-artist"]/a/text()'
            ).extract_first()
            # Check result returned correctly.
            track = {'lyrics': lyrics,
                      'title': title,
                      'artist': artist,
                      'url': response.url}
            yield track
        except:
            print('error')
            return
