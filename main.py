from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

    def validate(self, value):
        return bool(re.fullmatch(r"\d{10}", value))


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YY instead")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return "Phone not found."

    def __str__(self):
        return f"Contact name: {self.name.value}, contact birthday: {datetime.strftime(self.birthday.value, "%d.%m.%Y")} phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, "Contact not found.")

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                # current year birthdays
                birthday_this_year = record.birthday.value.replace(year=today.year)

                # if birthday already passed this year, check next year's date
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                # Check if the birthday is within the next week
                if today <= birthday_this_year <= next_week:
                    upcoming_birthdays.append(record.name.value)

        return upcoming_birthdays

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            return "Contact not found."


# Example usage
if __name__ == "__main__":
    # Create new address book
    book = AddressBook()

    # Create new record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_birthday("7.11.1998")

    book.add_record(john_record)
    print(book.get_upcoming_birthdays())

    # Show all contacts in the contact book
    for name, record in book.data.items():
        print(record)
