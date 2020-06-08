# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazontutorialItem
import pandas as pd

class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']

    start_urls = [
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&crid=18JBIS88NP6BM&qid=1591054244&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_st_review-rank'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=2&crid=18JBIS88NP6BM&qid=1591054247&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_1'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=3&crid=18JBIS88NP6BM&qid=1591054723&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_2'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=4&crid=18JBIS88NP6BM&qid=1591054751&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_3'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=5&crid=18JBIS88NP6BM&qid=1591054763&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_4'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=6&crid=18JBIS88NP6BM&qid=1591054772&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_5'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=7&crid=18JBIS88NP6BM&qid=1591054783&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_6'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=8&crid=18JBIS88NP6BM&qid=1591054793&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_7'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=9&crid=18JBIS88NP6BM&qid=1591054804&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_8'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=10&crid=18JBIS88NP6BM&qid=1591054816&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_9'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=11&crid=18JBIS88NP6BM&qid=1591054826&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_10'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=12&crid=18JBIS88NP6BM&qid=1591054841&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_11'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=13&crid=18JBIS88NP6BM&qid=1591054861&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_12'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=14&crid=18JBIS88NP6BM&qid=1591054877&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_13'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=15&crid=18JBIS88NP6BM&qid=1591054889&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_14'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=16&crid=18JBIS88NP6BM&qid=1591054900&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_15'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=17&crid=18JBIS88NP6BM&qid=1591054910&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_16'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=18&crid=18JBIS88NP6BM&qid=1591054923&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_17'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=19&crid=18JBIS88NP6BM&qid=1591054948&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_18'
        ,
        'https://www.amazon.com/s?k=renewed+laptops&rh=p_72%3A2661618011&s=review-rank&dc&page=20&crid=18JBIS88NP6BM&qid=1591054960&rnid=2661617011&sprefix=renewed%2Caps%2C204&ref=sr_pg_19']

    def parse(self, response):
        items = AmazontutorialItem()

        all_div_quotes=response.css('div.sg-row div.sg-col-4-of-12.sg-col-8-of-16.sg-col-16-of-24.sg-col-12-of-20.sg-col-24-of-32.sg-col.sg-col-28-of-36.sg-col-20-of-28')
        for amazon in all_div_quotes:
            yield {'nombre': amazon.css('.a-color-base.a-text-normal::text').extract(),
                   'customers_number':amazon.css('.a-size-small .a-size-base').css('::text').extract(),
                   'customers_points': amazon.css('.sg-col-12-of-28 .a-icon-alt::text').extract(),
                   'price_whole': amazon.css('.a-price-whole::text').extract(),
                   'product_link': amazon.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 a.a-link-normal.a-text-normal::attr(href)').extract(),
                   }


#'img_link': amazon.css('.s-image-fixed-height.s-image::attr(src)').extract(),