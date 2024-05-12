from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate_phone(self):
        return len(str(self.value)) == 10

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj.validate_phone():
            self.phones.append(phone_obj)
        else:
            print("Неправильний номер телефону")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones_str}{birthday_str}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday and record.birthday.value.month == next_week.month and record.birthday.value.day == next_week.day:
                upcoming_birthdays.append(record)

        return upcoming_birthdays

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_birthday("15.04.1990")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("20.04.1995")
book.add_record(jane_record)

print("Upcoming birthdays:")
for record in book.get_upcoming_birthdays():
    print(record)
