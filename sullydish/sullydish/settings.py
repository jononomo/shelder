# Scrapy settings for sullydish project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sullydish'

SPIDER_MODULES = ['sullydish.spiders']
NEWSPIDER_MODULE = 'sullydish.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'sullydish.shelder'
