from shelder.spiders import InteractiveSeleniumSpider
from shelder.selenium_api import HttpPage
from sullydish.items import SullydishItem


class DishPage(HttpPage):
    page_count = 1
    def navigate(self):
        self.page_count += 1
        self.driver.get('http://dish.andrewsullivan.com/page/'+str(self.page_count))
        # print 'NAVIGATE: '+self.driver.current_url
        return self

    def scrape_items(self):
        # print 'SCRAPE: '+self.driver.current_url
        main = self.driver.find_element_by_id('main')
        posts = main.find_elements_by_class_name('post')
        for post in posts:
            title = post.find_element_by_class_name('post-title').text
            print title
            entry_content = post.find_element_by_class_name('entry-content').text
            the_time = post.find_element_by_class_name('the-time').text
            sdi = SullydishItem()
            sdi['headline'] = title
            sdi['the_time'] = the_time
            sdi['entry_content'] = entry_content
            # print sdi
            yield sdi

    def navigable(self):
        return True


class DishAndrewsullivanComSpider(InteractiveSeleniumSpider):
    name = "dish.andrewsullivan.com"
    allowed_domains = ["dish.andrewsullivan.com"]
    start_urls = [
        'http://dish.andrewsullivan.com/'
        ]

    def __init__(self):
        super(DishAndrewsullivanComSpider, self).__init__()
        # this list will be searhed in order via the class's accept
        # method, starting at the bottom.  I.e., in reverse order.
        self.register_page(DishPage)

    
