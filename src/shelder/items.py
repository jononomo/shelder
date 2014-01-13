from scrapy.item import Item, Field

class ShelderItem(Item):
    shelder_meta = Field()

# items.pyclass PersonItem(Item):
class PersonItem(ShelderItem):
    raw_name = Field()
    title = Field()
    firstname = Field()
    middle = Field()
    lastname = Field()
    suffix = Field()
    ss_num = Field()
    birthdate = Field()
    gender = Field()

