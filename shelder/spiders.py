from scrapy.spider import BaseSpider
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from urlparse import urlparse
from exceptions import UrlRegexException, UnscrapeablePageException, AbstractPageException
from selenium_api import PageRegistry, HttpPage
import re
import os
import datetime
import time

class AbstractSeleniumSpider(BaseSpider):
    name = 'AbstractSeleniumSpider'
    allowed_domains = ['google.com']


    def __init__(self, *args, **kwargs):
        super(AbstractSeleniumSpider, self).__init__(*args, **kwargs)
        self.baseurl = self.allowed_domains[0]
        if self.baseurl[0:7] != "http://":
            self.baseurl = "http://"+self.baseurl
        self.driver = webdriver.Firefox()
        # this dispatcher line is crucial to shutting the Selenium
        # process down when the spider exits so we don't leave
        # orphan browser windows.
        dispatcher.connect(self.shutdown, signals.spider_closed)
        self.driver.get(self.baseurl)
        print 'Firefox webdriver started: '+self.driver.current_url
        self.loop_count = 0


    def parse(self, response):
        self.driver.get(response.url)

        while True:
            self.loop_count += 1
            print '\n'
            print ('-'*30) + ' PARSE LOOP '+str(self.loop_count)+' '+('-'*30)
            if self.shell():
                for item in self.scrape_items():
                    yield item
                if not self.navigate():
                    break
            else:
                break
            print ('-'*28) + ' END PARSE LOOP '+str(self.loop_count)+' '+('-'*28)+'\n\n'
        print ('-'*27) + ' END PARSE METHOD '+str(self.loop_count)+' '+('-'*27)+'\n\n'


    def shutdown(self, spider=None):
        print 'shutdown spider: ',spider
        if self.driver:
            print 'self.driver.quit()'
            self.driver.quit()
            self.driver = None

    def shell(self):
        return True
        # if this method returns false, then the spider will exit.
        # it is basically provided as a way to hook into the spider
        # as soon as Selenium starts up and the parse() method is
        # called. The idea is that custom logic can be implemented
        # here, perhaps including an interactive user shell
        # environment. 

    # should be implemented by sub-class
    # def scrape_items(self):
        # a generator that returns items scraped from Selenium
        # via self.driver, which is the API interface to the 
        # browser

    # should be implemented by sub-class
    # def navigate(self):
        # examines self.driver and takes some navigation action in
        # order to find more elements.  Returns True if it thinks 
        # more elements will now be found (i.e., it navigated somewhere
        # fertile). Returns False if it thinks there is nothing more to
        # be found and it is time to end the spider.


class InteractiveSeleniumSpider(AbstractSeleniumSpider):
    name = 'InteractiveSeleniumSpider'
    load_time = -1.0

    def __init__(self):
        # try:
        # print '-- A'
        self.selenium_api_registry = PageRegistry()
        # print '-- B'
        self.RUN = False # when False, it will expect command prompt interaction.
        self.KEEP_CRAWLING = True
        # print '-- C'
        start_load_time = time.time()
        super(InteractiveSeleniumSpider, self).__init__()
        finish_load_time = time.time()
        self.load_time = finish_load_time - start_load_time
        # print '-- D'
        self.shell_local_context = { 'self': self, 'time': self.load_time}
        # except Exception, e:
        #     self.shutdown()
        #     raise e

    def shell(self):
        self.RUN = False
        self.print_shell_message()
        while not self.RUN:
            # this next line will set 'PAGE' in self.shell_local_context
            self.get_page()
            rawinput = self.get_shell_input() # results in ['command', 'the args']
            if len(rawinput) == 0: continue
            command = rawinput[0]
            argument = None
            if len(rawinput) > 1: argument = rawinput[1]
            self.handle(command, argument)
        return self.KEEP_CRAWLING

    def get_page(self):
        self.shell_local_context['PAGE'] = self.selenium_api_registry.get_page(self)
        return self.shell_local_context['PAGE']

    def register_page(self, page_class):
        self.selenium_api_registry.register(page_class)

    def get_shell_input(self):
        return raw_input('SHELDER> ').split(None,1) # results in ['command', 'the args']


    def scrape_items(self):
        page = self.get_page()
        item_count = 0
        if page.scrapeable():
            for item in page.scrape_items():
                item_count += 1
                yield item
        print str(self.loop_count)+'shell-SCRAPED : '+str(item_count)+' items from '+str(page.__class__)
        

    def navigate(self):
        page = self.get_page()
        if page.navigable():
            a_load_time = time.time()
            page = page.navigate()
            b_load_time = time.time()
            self.load_time = b_load_time - a_load_time
            self.shell_local_context['time'] = self.load_time
            print str(self.loop_count)+'shell-NAVIGATE: '+self.driver.current_url
            # print self.load_time
            return True
        else:
            # nav_div = self.mainContent.find_element_by_id('WebPartWPQ2')
            # link = nav_div.find_element_by_link_text('Salary Search')
            print str(self.loop_count)+'shell-NAV NO HELP...'
            return False


    def print_shell_message(self):
        print '\n=========================================================================================='
        print 'You should have access to a variable called self, which is the Python spider object.'
        print 'self.driver is the object with the Selenium browser API.  There is a variable called'
        print 'PAGE that is in the shell context.  This holds the result of calling self.get_page()'
        print 'which basically gets the matching page from self.selenium_api_registry for the current'
        print 'driver state. The Selenium API registry is just an an object which maintains a cache'
        print 'of all the current page objects that have been created to represent different states'
        print 'that the web driver has been found in.  Each page object declares whether or not it'
        print 'considers itself suitable for servicing a certain web driver object. All page objects'
        print 'inherit from SeleniumHttpPage, which only accepts if the driver.current_url begins'
        print 'with "http://".  Every class is the page heirarchy is expected to be able to answer'
        print 'the question "are you a suitable api for this web driver object" with a @classmethod'
        print 'called accept().  SeleniumHttpPage.accept() merely matches the current_url against'
        print 'every regular expression in the list returned from calling cls.url_regex(), so a'
        print 'shortcut is just to override the url_regex() method, appending your own url rules to'
        print 'those of the page class you immediately inherit from. Overriding the accept() method'
        print 'permits a class to accept drivers with url\'s that do not begin with "http://" and,' 
        print 'in fact, to accept or reject a driver based on any kind of custom logic whatsoever.\n'
        self.print_help()
        print '\n> vars'
        self.print_local_context()


    def handle(self, command, args):
        arg1 = '' if not args else args.split()[0]
        if   command == 'run'      : self.RUN = True
        elif command == 'exit'     : self.exit()
        elif command == 'help'     : self.print_help()
        elif command == 'vars'     : self.print_local_context()
        elif command == 'time'     : self.ptime()
        elif command == 'sshot'    : print self.save_screenshot()
        # elif command == 'jump'     : print self.driver.get(arg1)
        elif command == 'info'     : print eval('help(PAGE)', {}, self.shell_local_context)
        else: self.eval_or_exec(' '.join([command, ('' if not args else args)]))

    def ptime(self):
        print 'The last recorded page.load_time for spider['+self.name+'] is: %2.1f seconds' % self.load_time

    def exit(self):
        # perhaps counter-intuitively, we want to "run", meaning exit the shell and go back
        # to the automatic spider control, but we want the spider to then stop crawling.
        self.RUN = True
        self.KEEP_CRAWLING = False

    def print_local_context(self):
        for key in self.shell_local_context:
            print key.rjust(9),'=', self.shell_local_context[key]

    def eval_or_exec(self, cmd_line):
        # print '============|EVAL|=========='
        # print '------------+    +----------'
        try:
            print eval(cmd_line, {}, self.shell_local_context)
        except Exception, e:
            #print 'eval exception: ', e
            try:
                exec(cmd_line, {}, self.shell_local_context)
            except Exception, e1:
                print e
                print 'evan and exec exceptions...'
                #traceback.print_exc()

    def print_help(self):
        print '+===============+===========================================================+'
        print '|      COMMAND  |                    DESCRIPTION                            |'
        print '+===============+===========================================================+'
        print '|           run | tell the spider to go back to scraping and navigating     |'
        print '|          exit | exit the spider, shutdown the Selenium browser, and quit  |'
        print '|          vars | list the variables in the shell context                   |'
        print '|          help | print this help message                                   |'
        print '|          info | documentation for the current shelder page                |'
        print '|         sshot | take a screenshot - saved in $SHELDER_OUTPUT/sshots/      |'
        print '|          time | how long it took the current page to load, in secs        |'
        print '|          back | the \'back\' button in the browser                          |'
        print '|       forward | the \'forward\' button in the browser                       |'
        # print '|    jump <url> | jumps directly to the page at the given url               |'
        print '+---------------+-----------------------------------------------------------+'
        print '\nAny input that does not begin with one of the commands above will be'
        print 'forwarded to python and expected to be a valid python statement within the'
        print 'spider\'s shell context.  Variables that are available to you can be examined'
        print 'with the \'vars\' command.'

    def save_screenshot(self):
        page = self.shell_local_context['PAGE']
        output_dir = os.environ['SHELDER_OUTPUT'] if 'SHELDER_OUTPUT' in os.environ else '.'
        sshot_dir = os.path.join(output_dir, 'sshots')
        if not os.path.exists(sshot_dir): os.mkdir(sshot_dir) 
        stamp = datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:19]
        filename = self.name+'.'+stamp+'.png'
        success = self.driver.save_screenshot(os.path.join(sshot_dir,filename))
        return {'success': success, 'filename': filename }
