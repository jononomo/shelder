from shelder.spiders import InteractiveSeleniumSpider
from sullydish.items import SullydishItem

class DishAndrewsullivanComSpider(InteractiveSeleniumSpider):
    name = "dish.andrewsullivan.com"
    allowed_domains = ["dish.andrewsullivan.com"]
    start_urls = [
        'http://dish.andrewsullivan.com/'
        ]
    page_count = 1

    def scrape_items(self):
        print self.driver.current_url+' - scrape_items'
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
            print sdi
            yield sdi

    def navigate(self):
        self.page_count += 1
        self.driver.get('http://dish.andrewsullivan.com/page/'+str(self.page_count))
        print 'navigated to: '+self.driver.current_url
        return True
