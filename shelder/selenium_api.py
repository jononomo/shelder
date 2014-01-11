from exceptions import UrlRegexException, UnscrapeablePageException, AbstractPageException
import re

class HttpPage(object):
    def __init__(self, selenium_spider):
        self.spider = selenium_spider
        self.driver = selenium_spider.driver
        self.nav_queue = []
        # print self.__class__.__name__
        # print 'about to call init()'
        self.init()

    @classmethod
    def accept(cls, driver):
        # print 'running page_class.accept() on ', cls
        for regex in cls.url_regex():
            if not re.match(regex, driver.current_url):
                print 'rejected by '+cls.__name__+' '+driver.current_url
                return False
        print 'accepted by '+cls.__name__+' '+driver.current_url
        return True

    @classmethod
    def url_regex(cls):
        return [r'^http://']

    def navigable(self):
        return True if len(self.nav_queue) > 0 else False

    def navigate(self):
        if len(self.nav_queue) > 0:
            nav_function = self.nav_queue[0]
            self.nav_queue = self.nav_queue[1:]
            return nav_function()
        else:
            return False

    def scrapeable(self):
        return False

    def scrape_items(self):
        raise UnscrapeablePageException(str(self.__class__)+' is not scrapeable')

    def print_nav_queue(self):
        for function in self.nav_queue:
            print function

    def init(self):
        # raise AbstractPageException('HttpPage should not be directly instantiated')
        pass



class PageRegistry(object):
    page_class_list = []
    active_pages = {}
    def __init__(self):
        # print 'PageRegistry.__init__'
        self.register(HttpPage)
        # print 'PageRegistry.__init__  done'
        # self.print_registry()

    def get_page(self, spider):
        # print '- - - - - - - - - - get page - - - - - - - - - - - -'
        # for page_class in reversed(self.page_class_list):
        #     print page_class
        # print '- - - now processing - - - -'

        for page_class in reversed(self.page_class_list):
            # print 'page_class.accept(driver)'
            # print str(page_class)+'.accept(driver['+driver.current_url+'])'
            # print page_class.accept(driver)
            if page_class.accept(spider.driver):
                if page_class in self.active_pages:
                    return self.active_pages[page_class]
                else:
                    print 'building new page object with ', page_class
                    self.active_pages[page_class] = page_class(spider)
                    return self.active_pages[page_class]
        print 'get_page() returning None'
        return None

    def register(self, page_class):
        # print 'registering: ', page_class
        self.page_class_list.append(page_class)

    def print_registry(self):
        print '- - - - - print registry - - - - -'
        for page_class in self.page_class_list:
            print page_class
        print '- - - - end print registry - - - -'


