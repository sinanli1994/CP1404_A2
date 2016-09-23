from kivy.app import App  # Import relevant kivy function
from kivy.lang import Builder
from kivy.uix.button import Button
import operator  # import the operator
import csv  # import the csv file


class Itemlist(App):
    def build(self):  # Create the main widget for Kivy program
        self.file_opener = open("list.csv")  # Open the file
        self.file_reader = csv.reader(self.file_opener)  # Read the file

        self.list = sorted(self.file_reader, key=operator.itemgetter(2))  # Sorting the list with priority

        self.title = "Shopping List 2.0"  # Main widget title
        self.root = Builder.load_file("list.kv")  # Load the kivy file
        self.required_mark()
        return self.root

    def required_mark(self):  # Function for required list and mark items to the completed (required button)
        count = 0
        total = 0

        self.root.ids.entriesBox.clear_widgets()  # Clear the list widgets

        required_list = sorted(self.list, key=operator.itemgetter(2))  # Sorting the list with priority

        self.root.ids.status_label.text = "Click items to mark them as completed"  # Prompt at status label

        for item in required_list:  # using for loop to separate to sorted file
            if "r" in item[3]:  # When "r" in item 3, then count, calculate and add the button of required items
                temp_button = Button(text=item[0], background_color=[count-0.5, 0, 1, 1])  # Setting the button text and background color
                temp_button.item = item
                temp_button.bind(on_release=self.handle_mark)  # Setting when user click the button
                self.root.ids.entriesBox.add_widget(temp_button)  # Add widgets for each required item
                count += 1
                total += float(item[1])  # Count the total price
        if count == 0:  # If total count = 0, then means no required item
            self.root.ids.top_label.text = "No required items"  # Show the prompt at the top label
            self.root.ids.entriesBox.clear_widgets()  # Clear the list widgets
        else:  # Else print total price at the top label
            self.root.ids.top_label.text = "Total expected price for {} items: ${}".format(count, total)
            # Else show the total price of required items at top babel

    def handle_mark(self, instance):  # Function when user click the button of the required item (Each required button)
        name = instance.text
        instance.item[3] = "c"  # Using "c" instead of "r" in the list when user chooses the item
        self.root.ids.status_label.text = ("{} marked as completed".format(name))  # Show the marked item at the status label

    def completed(self):  # Function for the completed item (Completed button)
        count = 0
        total = 0

        self.root.ids.entriesBox.clear_widgets()  # Clear the list widgets

        completed_list = sorted(self.list, key=operator.itemgetter(2))

        for item in completed_list:  # using for loop to separate to sorted file
            if "c" in item[3]:  # When "c" in item 3, then count, calculate and add the button of completed items
                temp_button = Button(text=item[0])  # Setting the button text
                temp_button.item = item
                temp_button.bind(on_release=self.handle_completed)  # Setting when user click the button
                self.root.ids.entriesBox.add_widget(temp_button)  # Add widgets for each completed item
                count += 1
                total += float(item[1])  # Count the total price
        if count == 0:  # If total count = 0, then means no completed item
            self.root.ids.top_label.text = "No completed items"  # Show the prompt at the top label
            self.root.ids.entriesBox.clear_widgets()  # Clear the list widgets
        else:
            self.root.ids.top_label.text = "Total expected price for {} items: ${}".format(count, total)
            # Else show the total price of completed items at top babel

    def handle_completed(self, instance):  # Function when user click the button of the completed item (Each conpleted button)
        self.root.ids.status_label.text = "{}, ${}, priority{} (completed)".format(instance.item[0], instance.item[1], instance.item[2])
        # Show the detail of the completed item at the status label

    def handle_add(self):  # Function for adding new item  (Add item button)
        item_name = self.root.ids.input_name.text  # Let user enter the item name
        price = self.root.ids.input_price.text  # Let user enter the price of item
        priority = self.root.ids.input_priority.text  # Let user enter the priority of item

        if item_name == "" or price == "" or priority == "":  # If any field is blank, show error prompt
            self.root.ids.status_label.text = "All fields must be completed"
        else:
            try:  # Using exception let user enter valid number
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
                    new_item = [item_name, str(price), str(priority), "r"]  # Make the new item to the list
                    self.list.append(new_item)  # Appending the new list to the required list
                    self.root.ids.status_label.text = "{}, ${} (priority {}) added to shopping list".format(item_name,
                                                                                                            price,
                                                                                                            priority)
                    # show the added item at the status label
                    self.root.ids.input_name.text = ""
                    self.root.ids.input_price.text = ""
                    self.root.ids.input_priority.text = ""
                    # Clear whole input box after the new item add to the list
        # Error check

    def handle_clear(self):  # Function for clear whole input box (Clear button)
        self.root.ids.input_name.text = ""
        self.root.ids.input_price.text = ""
        self.root.ids.input_priority.text = ""

    def save_item(self):  # Function for saving completed item to the file (Save item button)
        file_writer = open("list.csv", "a")  # Open the file with the correct format
        count = 0

        for item in self.list:  # Find the completed items and write to the file and delete the required items
            if "c" in item[3]:
                count += 1
                if count == 1:
                    file_writer2 = open("list.csv", "w")
                    file_writer2.writelines(item[0] + "," + item[1] + "," + item[2] + "," + "c")
                    file_writer2.close()
                else:
                    file_writer.writelines("\n" + item[0] + "," + item[1] + "," + item[2] + "," + "c")
            else:
                file_writer.writelines("")
        if count == 0:
            file_writer2 = open("list.csv", "w")
            file_writer2.close()

        self.root.ids.status_label.text = "{} items saved to items.csv".format(count)
        # Display how many items which add to the file at the status label
        file_writer.close()
        # Close the file

Itemlist().run()
