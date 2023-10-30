import scrapy
from urllib.parse import urlparse

class lyricstranslateSpider(scrapy.Spider):
    name = 'lyricstranslate'

    def start_requests(self):
        # Start by authenticating.
        # Start by accessing homepage for list of cities.
        url = 'https://lyricstranslate.com/en/songs/15/none/none?page=1&order=Popularity'
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
            return int(url.split("&")[0].split("=")[1])
        except:
            return None

    def parse_track_list(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)[:-1]
        links = response.xpath('//@href').extract()
        song_links = response.xpath('//div[@class="stt"]/a/@href').extract()
        next_page_num = self.page_from_url(response.url) + 1
        # this will go to infinity, should stop when no pages
        next_page_url = f"https://lyricstranslate.com/en/songs/15/none/none?page={next_page_num}&order=Popularity"
        follow_links = list(set([l for l in links if l[:9] == '/en/songs'
                        and self.page_from_url(l) == next_page_num]))

        for l in song_links:
            request = scrapy.Request(
                domain + l, self.parse_song,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            yield request

        request = scrapy.Request(
            next_page_url, self.parse_track_list,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        yield request

    def parse_song(self, response):
        try:
            lyrics = response.xpath('string(//div[@id="song-body"])').extract_first()
            title = response.xpath('string(//div[@id="song-title"])').extract_first().replace("lyrics","").strip()
            artist = response.xpath(
                'string(//div[@class="artist-title"])'
            ).extract_first()
            video_link = response.xpath("//*[@videoid]/a/@href").extract_first()
            # Check result returned correctly.
            track = {
                'lyrics': lyrics,
                'title': title,
                'artist': artist,
                'url': response.url,
                'video_link': video_link
                }
            yield track
        except:
            print('error')
            return
