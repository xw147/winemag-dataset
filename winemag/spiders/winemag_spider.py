import scrapy
from scrapy.loader import ItemLoader
 
from winemag.items import PageItem
import os

class WinemagSpider(scrapy.Spider):
    name = 'winemag'
    url_prefix = 'https://www.winemag.com/?s=&drink_type=wine&page={}'
    total_pages = 15421
    custom_settings = {
            'FEED_FORMAT': 'csv',
            'FEED_URI': '/Users/work/2020-wine-files/winemeg2021/wineImg-test.csv'
     }
    defaultImg = 'https://253qv1sx4ey389p9wtpp9sj0-wpengine.netdna-ssl.com/wp-content/assets/reviews/label-images/wine/Wine_Default_label.jpg'

    def start_requests(self):
        start_page = int(self.start_page) if hasattr(self, 'start_page') else 1
        end_page = int(self.end_page) if hasattr(self,  'end_page') else self.total_pages
        end_page = min(end_page, self.total_pages)

        for page in range(start_page, end_page + 1):
            yield scrapy.Request(url=self.url_prefix.format(page), callback=self.parse)

    def parse(self, response):
        for idx, review_item in enumerate(response.css('li.review-item:not(.search-results-ad)')):
            imgLink = review_item.css('img.listing-label::attr(src)').extract()
            if self.defaultImg not in imgLink:
                review_listing = review_item.css('a.review-listing')
                url = review_listing.attrib.get('href')
                yield scrapy.Request(url=url, callback=WinemagSpider.parse_single, cb_kwargs=dict(imgUrl=imgLink))

    @staticmethod
    def parse_single(response, imgUrl):
        loader = ItemLoader(item=PageItem(), response=response)
        
        loader.add_value('url', response.url)
        loader.add_value('imgUrl', imgUrl[0])
        loader.add_value('imgName', os.path.basename(imgUrl[0]))
        
        

        loader.add_css('title', 'div.header__title h1')
        
        reviewer_info_loader = loader.nested_css('span.taster-area')
        reviewer_info_loader.add_css('reviewer', 'a::text')
        reviewer_info_loader.add_css('reviewerUrl', 'a::attr(href)')
    
        loader.add_css('vintage', 'div.header__title h1') # pass title text
        
        loader.add_css('rating', '#points')
        
        loader.add_css('description', 'p.description')

        primary_info_loader = loader.nested_css('ul.primary-info')
        primary_info_loader.add_css('price', 'li:nth-child(2) div.info')
        
            
        primary_info_loader.add_css('variety', 'li:nth-child(3) div.info')
        
        appellation_loader = primary_info_loader.nested_css('li.row:nth-last-child(2) div.info')
        appellation_loader.add_css('subsubregion', 'span a:nth-last-child(4)')
        appellation_loader.add_css('subregion', 'span a:nth-last-child(3)')
        appellation_loader.add_css('region', 'span a:nth-last-child(2)')
        appellation_loader.add_css('country', 'span a:nth-last-child(1)')

        primary_info_loader.add_css('winery', 'li.row:nth-last-child(1) div.info')

        secondary_info_loader = loader.nested_css('ul.secondary-info')

        secondary_info_loader.add_css('alcohol', 'li.row:nth-child(1) div.info')
        secondary_info_loader.add_css('bottleSize', 'li.row:nth-child(2) div.info')
        secondary_info_loader.add_css('category', 'li.row:nth-child(3) div.info')
        
        if len(secondary_info_loader.selector.css('li.row')) == 6:
            secondary_info_loader.add_css('importer', 'li.row:nth-child(4) div.info')
      
        
        secondary_info_loader.add_css('reviewDate', 'li.row:nth-last-child(2) div.info')


        yield loader.load_item()



