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
    return len(leads) + 1



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
    print("\nNEW LEAD")
    print("------------------------------")
    print("Lead ID:", lead["id"])
    print("Name:", lead["name"])
    print("Phone:", lead["phone"])
    print("Service:", lead["service"])
    print("Message:", lead["message"])
    print("Urgency:", lead["urgency"])
    print("Priority:", lead["priority"])
    print("Status:", lead["status"])
    print("Created:", lead["created_at"])


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


print("\nLOCALFLOW AI")
print("------------------------------")
print("Smart lead intake for local service businesses")
print()



message = input("Describe your problem: ")
phone = input("Enter phone number: ")
new_lead = process_lead(message, phone)

display_lead(new_lead)

if lead_exists(new_lead):
    print("Lead already exists")
else:
    leads.append(new_lead)
    print("New lead added")


save_leads()

