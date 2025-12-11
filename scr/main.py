from colorama import Fore, Style, init
init(autoreset=True)

import json
import os
import csv

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    
    with open(CONTACTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

def show_menu():
    print(Fore.CYAN + "\n===== CONTACT BOOK MENU =====")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Export Contacts to CSV")
    print("7. Exit")
    print(Fore.CYAN + "=============================")

def add_contact(contacts):
    print(Fore.CYAN + "\n--- Add New Contact ---")
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    email = input("Enter email: ").strip()

    contact = {
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)
    print(Fore.GREEN + "Contact added successfully!")

def view_contact(contacts):
    print(Fore.CYAN + "\n--- All Contacts ---")

    if not contacts:
        print(Fore.RED + "No contacts found.")
        return
    
    for i, contact in enumerate(contacts, start=1):
        print(f"\nContact {i}:")
        print(f"Name : {contact['name']}")
        print(f"Phone : {contact['phone']}")
        print(f"Email : {contact['email']}")

def search_contact(contacts):
    print(Fore.CYAN + "\n--- Search Contact ---")
    keyword = input("Enter name, phone, or email to search: ").strip().lower()
    
    results = []
    for contact in contacts:
        if(
            keyword in contact['name'].lower() or
            keyword in contact['phone'].lower() or
            keyword in contact['email'].lower()
        ):
            results.append(contact)

    if not results:
        print(Fore.RED + "No matching contact found.")
        return
    
    print(f"\nFound {len(results)} contact(s):")
    for i, contact in enumerate(results, start=1):
        print(f"\nResult {i}:")
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email']}")

def update_contact(contacts):
    print(Fore.CYAN + "\n--- Update Contact ---")
    keyword = input("Enter name, phone, or email of the contact to update: ").strip().lower()

    matches = [c for c in contacts if 
               keyword in c["name"].lower() or
               keyword in c["phone"].lower() or
               keyword in c["email"].lower()]
    
    if not matches:
        print(Fore.RED + "No matching contact found.")
        return
    
    print(f"\nFound {len(matches)} matching contact(s):")
    for i, c in enumerate(matches, start=1):
        print(f"{i}. {c['name']} - {c['phone']} - {c['email']}")

    choice = int(input("\nEnter the number of the contact to update: ").strip())

    if choice < 1 or choice > len(matches):
        print(Fore.RED + "Invalid selection.")
        return
    
    contact = matches[choice - 1]

    print("\nPress Enter to keep existing value.\n")

    new_name = input(f"New name [{contact['name']}]: ").strip()
    new_phone = input(f"New phone [{contact['phone']}]: ").strip()
    new_email = input(f"New email [{contact['email']}]: ").strip()

    if new_name:
        contact["name"] = new_name
    if new_phone:
        contact["phone"] = new_phone
    if new_email:
        contact['email'] = new_email

    save_contacts(contacts)
    print(Fore.GREEN + "Contact updated successfully!")

def delete_contact(contacts):
    print(Fore.CYAN + "\n--- Delete Contact ---")
    keyword = input("Enter name, phone, or email of the contact to delete: ").strip().lower()

    matches = [c for c in contacts if
               keyword in c['name'].lower() or
               keyword in c['phone'].lower() or
               keyword in c['email'].lower()]
    
    if not matches:
        print(Fore.RED + "No matching contact found.")
        return
    
    print(f"\nFound {len(matches)} matching contact(s):")
    for i, c in enumerate(matches, start=1):
        print(f"{i}. {c['name']} - {c['phone']} - {c['email']}")

    choice = int(input("\nEnter the number of the contact to delete: ").strip())

    if choice < 1 or choice > len(matches):
        print(Fore.RED + "Invalid selection.")
        return
    
    contact_to_delete = matches[choice - 1]
    contacts.remove(contact_to_delete)

    save_contacts(contacts)
    print(Fore.GREEN + "Contact deleted successfully!")

def export_to_csv(contacts):
    print(Fore.CYAN + "\n--- Export Contacts to CSV ---")

    if not contacts:
        print(Fore.RED + "No contactsto export.")
        return
    
    filename = "contacts_export.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
        writer.writeheader()
        writer.writerows(contacts)

    print(Fore.GREEN + f"Contacts exported successfully to {filename}!")

def main():
    contacts = load_contacts()
    
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contact(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            export_to_csv(contacts)
        elif choice == "7":
            print(Fore.YELLOW + "Exiting Contact Book. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice! Please try again.")
        

if __name__ == "__main__":
    main()