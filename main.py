import scrapy
from scrapy.crawler import CrawlerProcess

class TripSpider(scrapy.Spider):
    name = "trip"
    start_urls = ['https://www.tripadvisor.com/Restaurants-g4-Europe.html#LOCATION_LIST']
    first_page = True

    def parse(self, response):
        if self.first_page:
            list = response.css('.geo_name a::attr(href)').getall()
            next_page = response.css('.nav.next.rndBtn.ui_button.primary.taLnk::attr(href)').get()
            self.first_page = False
        else:
            list = response.css('.geoList a::attr(href)').getall()
            next_page = response.css('.guiArw.sprite-pageNext.pid0::attr(href)').get()
        for i in list:
            yield response.follow(i, callback=self.parse_city)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_city(self, response):
        for i in response.css('.deQwQ .cauvp'):
            city = response.css('h1::text').get().replace('Best Restaurants in ', '')
            if len(i.css('.bHGqj::text').extract()) > 1:
                url = f"{i.css('.bHGqj::attr(href)').get()}#REVIEWS"
                yield response.follow(url, callback=self.parse_cafe, cb_kwargs={'city': city})
        if response.css('.nav.next.rndBtn.ui_button.primary.taLnk::attr(href)').get() is not None:
            yield response.follow(response.css('.nav.next.rndBtn.ui_button.primary.taLnk::attr(href)').get(), callback=self.parse_city)
    
    def parse_cafe(self, response, city):
        yield{
            'Country': city.split(',')[1].strip(),
            'City' : city.split(',')[0],
            'Address': response.css('.fhGHT::text').get(),
            'Name': response.css('.fHibz::text').get(),
            'Phone': response.css('.fhGHT a::text').get(default='').strip().replace(' ', ''),
            'Price': response.xpath('//div[contains(text(), "PRICE RANGE")]/following-sibling::div/text()').get(),
            'Rating': response.css('.dyeJW a svg::attr(aria-label)').get().replace(' of 5 bubbles', ''),
            'Ranking': response.css('.fhGHT span b span::text').get(default='').replace('#', ''),
            'Features': response.css('.dyeJW.VRlVV a::text').getall(),
            'Cuisines': response.xpath('//div[contains(text(), "CUISINES")]/following-sibling::div/text()').get(),
            'Diets': response.xpath('//div[contains(text(), "Special Diets")]/following-sibling::div/text()').get(),
            'Reviews': response.css('.eBTWs::text').get(),
            'English': response.xpath('//*[@data-tracker="English"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'French': response.xpath('//*[@data-tracker="French"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'German': response.xpath('//*[@data-tracker="German"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Italian': response.xpath('//*[@data-tracker="Italian"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Greek': response.xpath('//*[@data-tracker="Greek"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Chinese (Sim.)': response.xpath('//*[@data-tracker="Chinese (Sim.)"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Chinese (Trad.)': response.xpath('//*[@data-tracker="Chinese (Trad.)"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Spanish': response.xpath('//*[@data-tracker="Spanish"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Polish': response.xpath('//*[@data-tracker="Polish"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Portuguese': response.xpath('//*[@data-tracker="Portuguese"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Korean': response.xpath('//*[@data-tracker="Korean"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Norwegian': response.xpath('//*[@data-tracker="Norwegian"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Czech': response.xpath('//*[@data-tracker="Czech"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Dutch': response.xpath('//*[@data-tracker="Dutch"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Japanese': response.xpath('//*[@data-tracker="Japanese"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Russian': response.xpath('//*[@data-tracker="Russian"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Danish': response.xpath('//*[@data-tracker="Danish"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Swedish': response.xpath('//*[@data-tracker="Swedish"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Turkish': response.xpath('//*[@data-tracker="Turkish"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Hebrew': response.xpath('//*[@data-tracker="Hebrew"]/label/span/text()').get(default='').replace('(', '').replace(')', ''),
            'Arabic': response.xpath('//*[@data-tracker="Arabic"]/label/span/text()').get(default='').replace('(', '').replace(')', '') ,
        }
process = CrawlerProcess(settings={
    'FEED_URI': 'cafes.csv',
    'FEED_FORMAT': 'csv'
})
process.crawl(TripSpider)
process.start()