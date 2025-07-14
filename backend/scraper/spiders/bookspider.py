import scrapy
from scraper.items import BookItem

class BookSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = [
        'https://books.toscrape.com/'
    ]

    def parse(self, response):
        books = response.css('article.product_pod')
        
        # Extract book URLs for each book on the webpage, follow them
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
           
            yield response.follow(book_url, callback=self.parse_book_page)
        
        # Go to the next page if it exists
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
           
            yield response.follow(next_page_url, callback=self.parse)
            
    # Parse the individual book page for details
    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        
        book = BookItem()
        book['url'] = response.url
        book['title'] = response.css('.product_main h1::text').get()
        book['product_type'] = table_rows[1].css('td::text').get()
        book['price_excl_tax'] = table_rows[2].css('td::text').get()
        book['price_incl_tax'] = table_rows[3].css('td::text').get()
        book['tax'] = table_rows[4].css('td::text').get()
        book['availability'] = table_rows[5].css('td::text').get()
        book['num_reviews'] = table_rows[6].css('td::text').get()
        book['stars'] = response.css('p.star-rating').attrib['class']
        book['category'] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        book['description'] = response.xpath('//*[@id="content_inner"]/article/p/text()').get()
        book['price'] = response.css('.product_main .price_color::text').get()
        
        yield book