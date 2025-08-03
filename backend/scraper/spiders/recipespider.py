import scrapy
from scraper.items import RecipeItem

class RecipeSpider(scrapy.Spider):
    name = "recipespider"
    allowed_domains = ["allrecipes.com"]
    start_urls = [
        "https://www.allrecipes.com/search?q=lasagna"
    ]
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [460]
    }

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        for url in self.start_urls:
            self.logger.info(f"Sending request to: {url}")
            yield scrapy.Request(
                url,
                headers=headers,
                callback=self.parse
            )

    def parse(self, response):
        recipes = response.css("a.mntl-card-list-card--extendable")
        self.logger.info(f"Found {len(recipes)} recipes on the page: {response.url}")
        for recipe in recipes:
            recipe_url = recipe.css("a::attr(href)").get()
            self.logger.info(f"Found recipe URL: {recipe_url}")
            yield response.follow(recipe_url, callback=self.parse_recipe_page, headers=response.request.headers)

    # Parse individual recipe pages
    def parse_recipe_page(self, response):
        # Select all <li> elements inside the <ol> with the specific id
        steps = response.css('ol > li')
        self.logger.info(f"Found {len(steps)} steps in the recipe page: {response.url}")
        instructions = []
        for step in steps:
            # Get the text inside the <p> tag within each <li>
            text = step.css('p::text').get()
            if text:
                instructions.append(text.strip())
        # Try multiple selectors for ingredients
        ingredients = response.css('li.mntl-structured-ingredients__list-item')
        if not ingredients:
            ingredients = response.css('li span[data-ingredient-name]')
        if not ingredients:
            ingredients = response.css('li span.ingredient')
        ingredient_list = [' '.join(i.css('::text').getall()).strip() for i in ingredients]
        recipe = RecipeItem()
        recipe['url'] = response.url
        recipe['title'] = response.css('h1::text').get()
        recipe['ingredients'] = [i for i in ingredient_list if i]
        recipe['instructions'] = instructions
        self.logger.info(f"Scraped recipe: {recipe['title']} from {recipe['url']}")
        yield recipe



