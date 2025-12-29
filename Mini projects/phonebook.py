def newbook():
    return {}

def add_contact(phonebook,name,number):
    if type(name) != str or type(number) != str:
        print("Invalid input. Name and number should be strings.")
        return
    phonebook[name.strip()] = number


def remove_contact(phonebook,name):
    if name in phonebook:
        del phonebook[name]
    else:
        print("Contact not found.")


def view_contacts(phonebook):
    entries = dict(sorted(phonebook.items()))
    if not phonebook:
        print("Phonebook is empty.")
    else:
        for name, number in entries.items():
            print(f"{name}: {number}")

def search_contact(phonebook,name):
    if name in phonebook:
        print(f"{name}: {phonebook[name]}")
    else:
        print("Contact not found.")

def main():
    phonebook = newbook()
    while True:
        print("\nPhonebook Menu:")
        print("1. View Contacts")
        print("2. Add Contact")
        print("3. Remove Contact")
        print("4. Search Contact")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            view_contacts(phonebook)
        elif choice == '2':
            name = input("Enter contact name: ")
            number = input("Enter contact number: ")
            add_contact(phonebook, name, number)
            print("Contact added.")
        elif choice == '3':
            name = input("Enter contact name to remove: ")
            remove_contact(phonebook, name)
        elif choice == '4':
            name = input("Enter contact name to search: ")
            search_contact(phonebook, name)
        elif choice == '5':
            print("Exiting the Phonebook application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
