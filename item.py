class Item:
    def __init__(self, name="", price=0, priority=0):
        self.name = name
        self.price = price
        self.priority = priority

    def __str__(self):
        return "{}, ${} (priority {}) added to shopping list".format(self.name, self.price, self.priority)
