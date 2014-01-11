from selenium_spiders import InteractiveSeleniumSpider
from public_employee.items import SullyDishItem

class DishAndrewsullivanComSpider(InteractiveSeleniumSpider):
    name = "dish.andrewsullivan.com"
    allowed_domains = ["dish.andrewsullivan.com"]
    start_urls = [
        'http://dish.andrewsullivan.com/'
        ]

    def scrape_items(self):
        print self.url_scheme.path+' - scrape_items'
        main = self.driver.find_element_by_id('main')
        posts = main.find_elements_by_class_name('post')
        for post in posts:
            title = post.find_element_by_class_name('post-title').text
            print title
            entry_content = post.find_element_by_class_name('entry-content').text
            the_time = post.find_element_by_class_name('the-time').text
            sdi = SullyDishItem()
            sdi['headline'] = title
            sdi['the_time'] = the_time
            sdi['entry_content'] = entry_content
            print sdi
            yield sdi

    def navigate(self, response):
        print self.url_scheme.path+' - navigate'
        return False
