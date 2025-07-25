#!/usr/bin/env python3
"""
Contact Manager Application.

This program implements a simple command‑line contact manager that allows
users to store, view, search, update, and delete contacts. Each contact
record includes a name, phone number, email address, and physical
address. Contacts are persisted between sessions using a JSON file on
disk.

Features:

* **Contact Storage** – Contacts are stored in a JSON file (`contacts.json`)
  so that they persist between program runs. Each contact has a
  unique identifier, a name, a phone number, an email, and an address.

* **Add Contact** – Prompts the user for contact details and adds a new
  contact to the contact list.

* **View Contact List** – Displays all saved contacts with their names
  and phone numbers. The user can see additional details for each
  contact if desired.

* **Search Contact** – Allows searching by name or phone number. The
  search is case-insensitive and returns all matching contacts.

* **Update Contact** – Enables the user to modify any of the details
  associated with a selected contact. Leaving a field blank will
  retain the existing value.

* **Delete Contact** – Removes a selected contact from the list.

* **User Interface** – A simple menu‑driven command‑line interface
  guides the user through the available actions. Input is validated
  where possible to prevent invalid operations.

Usage::

    python contact_manager.py

"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional


DATA_FILE = "contacts.json"


def load_contacts() -> List[Dict[str, str]]:
    """Load contacts from the JSON file.

    Returns an empty list if the file does not exist or is invalid.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                # ensure all entries are dictionaries
                return [dict(entry) for entry in data]
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_contacts(contacts: List[Dict[str, str]]) -> None:
    """Save contacts to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=4, ensure_ascii=False)
    except IOError as exc:
        print(f"Error saving contacts: {exc}")


def generate_new_id(contacts: List[Dict[str, str]]) -> int:
    """Generate a new unique identifier based on existing contacts."""
    if not contacts:
        return 1
    existing_ids = [c.get("id", 0) for c in contacts if isinstance(c.get("id"), int)]
    return max(existing_ids, default=0) + 1


def add_contact(contacts: List[Dict[str, str]]) -> None:
    """Prompt the user for contact details and add the new contact."""
    print("\n=== Add New Contact ===")
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    address = input("Enter address: ").strip()

    if not name or not phone:
        print("Name and phone number are required. Contact not added.")
        return

    new_contact = {
        "id": generate_new_id(contacts),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    }
    contacts.append(new_contact)
    save_contacts(contacts)
    print("Contact added successfully!\n")


def view_contacts(contacts: List[Dict[str, str]]) -> None:
    """Display all contacts with names and phone numbers."""
    print("\n=== Contact List ===")
    if not contacts:
        print("No contacts found.\n")
        return
    for idx, contact in enumerate(contacts, start=1):
        name = contact.get("name", "Unknown")
        phone = contact.get("phone", "")
        print(f"{idx}. {name} – {phone}")
    print("")


def search_contacts(contacts: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Search for contacts by name or phone number.

    Returns a list of matching contacts.
    """
    if not contacts:
        print("\nNo contacts to search.\n")
        return []
    query = input("\nEnter name or phone number to search: ").strip().lower()
    results = [c for c in contacts if query in c.get("name", "").lower() or query in c.get("phone", "").lower()]
    if not results:
        print("No matching contacts found.\n")
    else:
        print("\nSearch Results:")
        for idx, contact in enumerate(results, start=1):
            print(f"{idx}. {contact['name']} – {contact['phone']}")
        print("")
    return results


def select_contact(contacts: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Helper to select a contact from the list via user input.

    Returns the selected contact dictionary or None if no selection is made.
    """
    if not contacts:
        print("No contacts available.")
        return None
    for idx, contact in enumerate(contacts, start=1):
        print(f"{idx}. {contact['name']} – {contact['phone']}")
    while True:
        choice = input("Select a contact by number (or press Enter to cancel): ").strip()
        if choice == "":
            return None
        if choice.isdigit():
            i = int(choice)
            if 1 <= i <= len(contacts):
                return contacts[i - 1]
        print("Invalid selection. Try again.")


def update_contact(contacts: List[Dict[str, str]]) -> None:
    """Update an existing contact's details."""
    print("\n=== Update Contact ===")
    search_results = search_contacts(contacts)
    if not search_results:
        return
    contact = select_contact(search_results)
    if not contact:
        print("Update cancelled.\n")
        return

    print("Leave a field blank to keep the current value.")
    new_name = input(f"New name [{contact['name']}]: ").strip()
    new_phone = input(f"New phone [{contact['phone']}]: ").strip()
    new_email = input(f"New email [{contact['email']}]: ").strip()
    new_address = input(f"New address [{contact['address']}]: ").strip()

    if new_name:
        contact['name'] = new_name
    if new_phone:
        contact['phone'] = new_phone
    if new_email:
        contact['email'] = new_email
    if new_address:
        contact['address'] = new_address

    save_contacts(contacts)
    print("Contact updated successfully!\n")


def delete_contact(contacts: List[Dict[str, str]]) -> None:
    """Delete a contact from the list."""
    print("\n=== Delete Contact ===")
    search_results = search_contacts(contacts)
    if not search_results:
        return
    contact = select_contact(search_results)
    if not contact:
        print("Deletion cancelled.\n")
        return

    confirmation = input(f"Are you sure you want to delete '{contact['name']}'? (y/n): ").strip().lower()
    if confirmation in ("y", "yes"):
        contacts.remove(contact)
        save_contacts(contacts)
        print("Contact deleted successfully!\n")
    else:
        print("Deletion aborted.\n")


def main_menu() -> None:
    """Main loop for the contact manager interface."""
    contacts = load_contacts()
    options = {
        "1": add_contact,
        "2": view_contacts,
        "3": lambda c: search_contacts(c),
        "4": update_contact,
        "5": delete_contact,
        "6": lambda c: exit(0),
    }
    while True:
        print("=== Contact Manager ===")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()
        action = options.get(choice)
        if action:
            action(contacts)
        else:
            print("Invalid selection. Please choose a valid option.\n")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")