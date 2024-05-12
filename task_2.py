from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format. Please use 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def parse_input(user_input):
    tokens = user_input.split()
    if not tokens:
        return None, None
    command = tokens[0].lower()
    arguments = tokens[1:]
    return command, arguments

def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name, phone = args
            record = book.find(name)
            message = "Contact updated."
            if record is None:
                record = Record(name)
                book.add_record(record)
                message = "Contact added."
            if phone:
                record.add_phone(phone)
            print(message)

        elif command == "change":
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                for phone in record.phones:
                    if str(phone) == old_phone:
                        phone.value = new_phone
                        print("Contact updated.")
                        break
                else:
                    print("Phone number not found for contact.")
            else:
                print("Contact not found.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            if record:
                if record.phones:
                    print(f"Phone numbers for {name}: {', '.join(str(p) for p in record.phones)}")
                else:
                    print(f"No phone numbers found for {name}.")
            else:
                print("Contact not found.")

        elif command == "all":
            if book.data:
                print("All contacts:")
                for record in book.data.values():
                    print(record)
            else:
                print("No contacts found.")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()