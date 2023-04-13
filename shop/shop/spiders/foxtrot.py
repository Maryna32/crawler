import scrapy

from shop.items import ShopItem

class FoxtrotSpider(scrapy.Spider):
    name = "foxtrot"
    allowed_domains = ["foxtrot.com.ua"]
    start_urls = ["https://www.foxtrot.com.ua/uk/shop/girobordi.html"]
    # start_urls = ["https://www.foxtrot.com.ua/uk/shop/stiralniye_mashiniy_samsung_ww70t3020bwua.html"]

    def parse(self, response, **kwards):

        urls = response.css('div.listing__body-wrap div.card div.card__image a::attr(href)').extract()
        for url in urls[:5]:
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_products,
                dont_filter=True,
                cb_kwargs={'breadcrumbs': response.css('div.breadcrumbs li a::text').getall()}
            )

        next_page = response.css('nav.listing__pagination ul li.listing__pagination-nav')[-1]
        page = next_page.attrib['data-page']
        yield scrapy.Request(
             url=f'{response.url.split("?")[0]}?page={page}',
             callback=self.parse,
             dont_filter=True
        )


    def parse_products(self, response, breadcrumbs):
        item = ShopItem()
        item['url'] = response.url
        item['name'] = response.css('h1.page__title').attrib['title']
        item['rating'] = len(response.css('div.product-menu__card-review').xpath('.//div[@class="product-menu__card'
                                                                                 '-rating"]/i[contains(@class, '
                                                                                 '"icon_orange")]'))
        item['breadcrumbs'] = breadcrumbs
        yield item
