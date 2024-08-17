from colorama import Fore, Back, Style
from address_book import AddressBook, Record
from error_decorator import input_error
from output_formatter import format_success, format_error


@input_error
def contacts_handlers(command, contacts, *arguments):
    no_args_handlers_map = {
        'hello': hello_handler,
        'help': help_handler,
    }

    handlers_map = {
        'add': add_contact_handler,
        'add-email': add_email_handler,
        'change-email': change_email_handler,
        'set-address': set_address,
        'change': change_phone_handler,
        'phone': get_contact_handler,
        'all': get_all_contacts_handler,
        'add-birthday': add_birthday_handler,
        'show-birthday': get_birthday_handler,
        'birthdays': get_all_birthdays_handler,
    }

    if command in no_args_handlers_map:
        return no_args_handlers_map[command]()

    return handlers_map[command](contacts, *arguments)


def hello_handler():
    return 'Hello, how can I help you?'


def help_handler():
    return f'''Possible commands:
{Fore.LIGHTWHITE_EX}{Back.BLUE}help{Style.RESET_ALL} - prints list of available commands
{Fore.LIGHTWHITE_EX}{Back.BLUE}hello{Style.RESET_ALL} - prints a greeting 
{Fore.LIGHTWHITE_EX}{Back.BLUE}add [name] [phone number]{Style.RESET_ALL} - create a contact with a phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-email [name] [email] [is_primary]{Style.RESET_ALL} - Add or change email in contact, or create new contact with email if not exists
{Fore.LIGHTWHITE_EX}{Back.BLUE}change-email [name] [old_email_value] [new_email_value] [is_primary]{Style.RESET_ALL} - Add or change email in contact, or create new contact with email if not exists
{Fore.LIGHTWHITE_EX}{Back.BLUE}set-address [name] [address]{Style.RESET_ALL} - set address into contact
{Fore.LIGHTWHITE_EX}{Back.BLUE}change [name] [phone number]{Style.RESET_ALL} - changes a contact phone number 
{Fore.LIGHTWHITE_EX}{Back.BLUE}phone [name]{Style.RESET_ALL} - prints contacts phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}all{Style.RESET_ALL} - prints all contacts
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-birthday [name] [birthday]{Style.RESET_ALL} - adds birthday to a contact
{Fore.LIGHTWHITE_EX}{Back.BLUE}show-birthday [name]{Style.RESET_ALL} - prints contact's birthday
{Fore.LIGHTWHITE_EX}{Back.BLUE}birthdays{Style.RESET_ALL} - prints all birthdays
{Fore.LIGHTWHITE_EX}{Back.BLUE}close{Style.RESET_ALL} або {Fore.YELLOW}{Back.BLUE}exit{Style.RESET_ALL} - terminates a program
    '''


@input_error
def add_contact_handler(contacts: AddressBook, name: str, phone: str):
    name = name.lower().capitalize()

    try:
        record = contacts.find(name)
    except ValueError:
        record = Record(name)

    record.add_phone(phone)
    contacts[name] = record

    return format_success('Contact added')


@input_error
def add_email_handler(contacts: AddressBook, name: str, email: str, is_primary: str = "False"):
    name = name.lower().capitalize()
    primary = parser_bool_from_str(is_primary)

    record = contacts.find(name)
    if record is None:
        record = Record(name)

    record.add_email(email, primary)
    contacts[name] = record

    return format_success('Email added')


@input_error
def change_phone_handler(contacts: AddressBook, name: str, phone: str):
    name = name.lower().capitalize()
    try:
        record = contacts.find(name)
        record.edit_phone(record.phones[0], phone)

        return format_success('Contact updated.')
    except ValueError:
        return format_error('Contact not found.')


@input_error
def change_email_handler(contacts: AddressBook, name: str, old_email: str, new_email: str, is_primary: str):
    name = name.lower().capitalize()
    primary = parser_bool_from_str(is_primary)

    try:
        record = contacts.find(name)
        record.change_email(old_email, new_email, primary)

        return format_success('Email updated.')
    except ValueError as error:
        return format_error(error)


@input_error
def set_address(contacts: AddressBook, name: str, *args):
    try:
        record = contacts.find(name)
        record.set_address(' '.join(args))

        return format_success('The address is set.')
    except ValueError as error:
        return format_error(error)


@input_error
def get_contact_handler(contacts: AddressBook, name: str, *args):
    try:
        return contacts.find(name.lower().capitalize())
    except ValueError:
        return format_error('Contact not found.')


def get_all_contacts_handler(contacts: AddressBook, *args):
    if len(contacts) == 0:
        return format_error('AddressBook is empty.')
    return '\n'.join(map(lambda name: f'{name}: {contacts[name]}', contacts.keys()))


def add_birthday_handler(contacts: AddressBook, name: str, birthday: str):
    try:
        contacts.find(name.lower().capitalize()).add_birthday(birthday)
        return format_success('Contact updated.')
    except ValueError as error:
        return format_error(error)


def get_birthday_handler(contacts: AddressBook, name: str, *args):
    try:
        return contacts.find(name.lower().capitalize()).birthday
    except ValueError:
        return format_error('Contact not found.')


def get_all_birthdays_handler(contacts: AddressBook, *args):
    return '\n'.join(map(lambda name: f'{name}: {contacts[name].birthday}', contacts.keys()))


def parser_bool_from_str(val: str) -> bool:
    return val.lower() == 'true'
