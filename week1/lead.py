import json
import re
from datetime import datetime


def load_leads():
    with open("week1/leads.json", "r") as file:
        return json.load(file)


leads = load_leads()


def determine_priority(urgency):
    if urgency == "High":
        return "URGENT"
    elif urgency == "Medium":
        return "NORMAL"
    else:
        return "LOW"


def determine_urgency(message):
    message = message.lower()
    score = 0

    if "freezing" in message:
        score += 2
    if "children" in message:
        score += 1
    if "heater" in message:
        score += 1
    if "flooding" in message:
        score += 3
    if "electrical" in message:
        score += 3
    if "immediately" in message:
        score += 3
    if "today" in message:
        score += 3
    if "emergency" in message:
        score += 3
    if "urgent" in message:
        score += 3
    if "no heat" in message:
        score += 3
    if "no ac" in message:
        score += 3

    if score >= 3:
        return "High"
    elif score >= 1:
        return "Medium"
    else:
        return "Low"


def extract_service(message):
    message = message.lower()

    if re.search(r"\bac\b", message) or "air conditioning" in message:
        return "AC Repair"
    if "plumbing" in message or "pipe" in message or "leak" in message:
        return "Plumbing"
    if "electrical" in message or "outlet" in message or "wiring" in message:
        return "Electrical"
    if "heater" in message or "furnace" in message:
        return "HVAC"

    return "Other"


def extract_name(message):
    message = message.strip()

    if "my name is" in message.lower():
        name = message.lower().split("my name is", 1)[1]
        return name.strip().split(".")[0].title()

    return "Unknown"


def generate_lead_id():
    if len(leads) == 0:
        return 1

    highest_id = 0

    for lead in leads:
        if lead["id"] > highest_id:
            highest_id = lead["id"]
    return highest_id + 1


def create_lead(name, phone, service, urgency, message):
    priority = determine_priority(urgency)
    lead_id = generate_lead_id()

    lead = {
        "id": lead_id,
        "name": name,
        "phone": phone,
        "service": service,
        "message": message,
        "urgency": urgency,
        "priority": priority,
        "status": "New",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return lead


def display_lead(lead):
    print("\nLEAD")
    print("------------------------------")
    print("Lead ID:", lead.get("id", "N/A"))
    print("Name:", lead["name"])
    print("Phone:", lead["phone"])
    print("Service:", lead["service"])
    print("Message:", lead.get("message", "N/A"))
    print("Urgency:", lead["urgency"])
    print("Priority:", lead["priority"])
    print("Status:", lead["status"])
    print("Created:", lead.get("created_at", "N/A"))


def lead_exists(lead):
    for existing_lead in leads:
        if existing_lead["phone"] == lead["phone"]:
            return True

    return False


def process_lead(message, phone):
    name = extract_name(message)
    service = extract_service(message)
    urgency = determine_urgency(message)

    lead = create_lead(
        name,
        phone,
        service,
        urgency,
        message
    )

    return lead


def save_leads():
    with open("week1/leads.json", "w") as file:
        json.dump(leads, file, indent=4)


def view_all_leads():
    if len(leads) == 0:
        print("\nNo leads found.")
        return

    print("\nALL LEADS")
    print("------------------------------")

    for lead in leads:
        display_lead(lead)

def view_urgent_leads():
    print("\nURGENT LEADS")
    print("------------------------------")

    found_urgent = False

    for lead in leads:
        if lead["priority"] == "URGENT":
            display_lead(lead)
            found_urgent = True

    if found_urgent == False:
        print("No urgent leads found.")


def repair_old_leads():
    next_id = 1

    for lead in leads:
        if "id" not in lead:
            lead["id"] = next_id

        next_id += 1

        if "message" not in lead:
            lead["message"] = "Legacy lead - original message unavailable"
        if "created_at" not in lead:
            lead["created_at"] = "Legacy lead - timestamp unavailable"
    save_leads()


def update_lead_status():
    lead_id = input("Enter Lead ID: ")

    for lead in leads:
        if str(lead["id"]) == lead_id:
            print("\nCurrent status:", lead["status"])
            print("1. New")
            print("2. Contacted")
            print("3. Scheduled")
            print("4. Completed")

            status_choice = input("Choose new status: ")

            if status_choice == "1":
                lead["status"] = "New"
            elif status_choice == "2":
                lead["status"] = "Contacted"
            elif status_choice == "3":
                lead["status"] = "Scheduled"
            elif status_choice == "4":
                lead["status"] = "Completed"
            else:
                print("Invalid status choice.")
                return

            save_leads()
            print("Lead status updated.")
            return

    print("Lead not found.")

def display_menu():
    print("\nLOCALFLOW AI")
    print("------------------------------")
    print("1. Add new lead")
    print("2. View all leads")
    print("3. View urgent leads")
    print("4. Update lead status")
    print("5. Exit")

if __name__ == "__main__":
    print("\nLOCALFLOW AI")
    print("------------------------------")
    print("Smart lead intake for local service businesses")

    display_menu()

    choice = input("Choose an option: ")

    if choice == "1":
        message = input("Describe your problem: ")
        phone = input("Enter phone number: ")

        new_lead = process_lead(message, phone)

        display_lead(new_lead)

        if lead_exists(new_lead):
            print("Lead already exists")
        else:
            leads.append(new_lead)
            save_leads()
            print("New lead added")

    elif choice == "2":
        view_all_leads()

    elif choice == "3":
        view_urgent_leads()

    elif choice == "4":
        update_lead_status()

    elif choice == "5":
        print("Goodbye.")

    else:
        print("Invalid option.")