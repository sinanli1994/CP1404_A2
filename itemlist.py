from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
import operator  # import the operator
import csv  # import the csv file


class Itemlist(App):
    def build(self):
        self.file_opener = open("list.csv")
        self.file_reader = csv.reader(self.file_opener)

        self.list = sorted(self.file_reader, key=operator.itemgetter(2))

        self.title = "Shopping List 2.0"
        self.root = Builder.load_file("list.kv")
        return self.root

    def required(self):
        count = 0
        total = 0

        self.root.ids.entriesBox.clear_widgets()

        required_list = sorted(self.list, key=operator.itemgetter(2))

        self.root.ids.status_label.text = "Click items to mark them as completed"

        for item in required_list:  # using for loop to separate to sorted file
            if "r" in item[3]:  # When "r" in item 3, then count, calculate and show the button of required items
                temp_button = Button(text=item[0])
                temp_button.item = item
                temp_button.bind(on_release=self.handle_mark)
                self.root.ids.entriesBox.add_widget(temp_button)
                count += 1
                total += float(item[1])
        if count == 0:  # If total count = 0, then means no required item
            self.root.ids.top_label.text = "No required items"
            self.root.ids.entriesBox.clear_widgets()
        else:  # Else print total price at the top label
            self.root.ids.top_label.text = "Total expected price for {} items: ${}".format(count, total)
            # Else show the total price of required items at top babel

    def handle_mark(self, instance):
        name = instance.text
        instance.item[3] = "c"
        self.root.ids.status_label.text = ("{} marked as completed".format(name))

    def completed(self):
        count = 0
        total = 0

        self.root.ids.entriesBox.clear_widgets()

        completed_list = sorted(self.list, key=operator.itemgetter(2))

        for item in completed_list:  # using for loop to separate to sorted file
            if "c" in item[3]:  # When "c" in item 3, then count, calculate and show the button of completed items
                temp_button = Button(text=item[0])
                temp_button.item = item
                temp_button.bind(on_release=self.handle_completed)
                self.root.ids.entriesBox.add_widget(temp_button)
                count += 1
                total += float(item[1])
        if count == 0:  # If total count = 0, then means no completed item
            self.root.ids.top_label.text = "No completed items"
            self.root.ids.entriesBox.clear_widgets()
        else:
            self.root.ids.top_label.text = "Total expected price for {} items: ${}".format(count, total)
            # Else show the total price of completed items at top babel

    def handle_completed(self, instance):
        self.root.ids.status_label.text = "{}, ${}, priority{} (completed)".format(instance.item[0], instance.item[1], instance.item[2])

    def handle_add(self):
        item_name = self.root.ids.input_name.text  # Let user enter the item name
        price = self.root.ids.input_price.text  # Let user enter the price of item
        priority = self.root.ids.input_priority.text  # Let user enter the priority of item

        if item_name == "" or price == "" or priority == "":
            self.root.ids.status_label.text = "All fields must be completed"
        else:
            try:
                price = float(self.root.ids.input_price.text)
                priority = int(self.root.ids.input_priority.text)
            except ValueError:
                self.root.ids.status_label.text = "Please enter a valid number"
            else:
                if price <= 0:
                    self.root.ids.status_label.text = "Price must be >= $0"
                elif priority != 1 and priority != 2 and priority != 3:
                    self.root.ids.status_label.text = "Priority must be 1, 2 or 3"
                else:
                    new_item = [item_name, str(price), str(priority), "r"]
                    self.list.append(new_item)
                    self.root.ids.status_label.text = "{}, ${} (priority {}) added to shopping list".format(item_name,
                                                                                                            price,
                                                                                                            priority)
                    # show the added item at the status label
                    self.root.ids.input_name.text = ""
                    self.root.ids.input_price.text = ""
                    self.root.ids.input_priority.text = ""
        # Error check

    def handle_clear(self):
        self.root.ids.input_name.text = ""
        self.root.ids.input_price.text = ""
        self.root.ids.input_priority.text = ""
        # Clear whole input box

Itemlist().run()
