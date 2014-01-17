from exceptions import UrlRegexException, UnscrapeablePageException, AbstractPageException
import re
import selenium


class SeleniumPage(object):
    def __init__(self, the_spider):
        self.spider = the_spider
        self.nav_queue = []
        print 'inital empty self.nav_queue'

    @classmethod
    def accept(cls, web_driver):
        return True #if isinstance(web_driver, selenium.webdriver) else False

    def scrapeable(self):
        return False

    def scrape_items(self):
        raise UnscrapeablePageException('SeleniumSpiderPage is not scrapeable - scrape_items() should be handled by a subclass')

    def navigable(self):
        return True if len(self.nav_queue) > 0 else False

    def navigate(self):
        if len(self.nav_queue) > 0:
            nav_function = self.nav_queue[0]
            self.nav_queue = self.nav_queue[1:]
            # return the result of calling the nav function. This should
            # return another SeleniumHttpPage object, or a subclass of one
            return nav_function()
        else:
            return False

    def print_nav_queue(self):
        for function in self.nav_queue:
            print function

    def prime(self):
        raise AbstractPageException('SeleniumPage should not be directly instantiated - prime() should be handled by a subclass.')
        pass



class SeleniumHttpPage(SeleniumPage):
    @classmethod
    def accept(cls, web_driver):
        # print 'running page_class.accept() on ', cls
        for regex in cls.url_regex():
            if not re.match(regex, web_driver.current_url):
                # print 'rejected by '+cls.__name__+' '+web_driver.current_url
                return False
        # print 'accepted by '+cls.__name__+' '+web_driver.current_url
        return SeleniumPage.accept(web_driver)

    @classmethod
    def url_regex(cls):
        return [r'^http://.*']

    def prime(self):
        raise AbstractPageException('SeleniumHttpPage should not be directly instantiated - prime() should be handled by a subclass.')



class PageRegistry(object):
    page_class_list = []
    active_pages = {}
    def __init__(self):
        # print 'PageRegistry.__init__'
        self.register(SeleniumPage)
        # print 'PageRegistry.__init__  done'
        # self.print_registry()

    def get_page(self, spider):
        # print '- - - - - - - - - - get page - - - - - - - - - - - -'
        # for page_class in reversed(self.page_class_list):
        #     print page_class
        # print '- - - now processing - - - -'
        try:
            for page_class in reversed(self.page_class_list):
                # print 'page_class.accept(driver)'
                # print str(page_class.__name__)+'.accept(driver['+spider.driver.current_url+'])'+'  =  '+str(page_class.accept(spider.driver))
                if page_class.accept(spider.driver):
                    # if we are in here, then a registered page class
                    # has decided to accept responsibility
                    if page_class not in self.active_pages:
                        # print 'building new page object with ', page_class
                        self.active_pages[page_class] = page_class(spider)
                    if not isinstance(self.active_pages[page_class], SeleniumPage):
                        raise Exception('page must be an instance of SeleniumPage')
                    # print 'REGISTRY: ',self.active_pages[page_class].__class__.__name__
                    return self.active_pages[page_class]
        except Exception, e:
            print 'PageRegistry.get_page() EXCEPTION', e
        print 'PageRegistry.get_page() returning None. You should probably add a catch-all, like shelder.SeleniumHttpPage or shelder.SeleniumPage.'
        return None

    def register(self, page_class):
        # print 'registering: ', page_class
        self.page_class_list.append(page_class)

    # def print_registry(self):
    #     print '- - - - - print registry - - - - -'
    #     for page_class in self.page_class_list:
    #         print page_class
    #     print '- - - - end print registry - - - -'


