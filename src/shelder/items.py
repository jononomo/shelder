from scrapy.item import Item, Field

# items.pyclass PersonItem(Item):
class PersonItem(Item):
    title = Field()
    firstname = Field()
    middle = Field()
    lastname = Field()
    suffix = Field()
    ss_num = Field()
    birthdate = Field()
    gender = Field()

