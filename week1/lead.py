import json

with open("week1/leads.json", "r") as file:
    leads = json.load(file)

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

    if score >= 3:
        return "High"
    elif score >= 1:
        return "Medium"
    else:
        return "Low"


     


def create_lead(name, phone, service, urgency):
    priority = determine_priority(urgency)
    lead = {
        "name": name,
        "phone": phone,
        "service": service,
        "urgency": urgency,
        "priority": priority,
        "status": "New"
    }
    return lead

def display_lead(lead):
    print("\nNEW LEAD")
    print("------------------------------")
    print("Name:", lead["name"])
    print("Phone:", lead["phone"])
    print("Service:", lead["service"])
    print("Urgency:", lead["urgency"])
    print("Priority:", lead["priority"])
    print("Status:", lead["status"])

lead = create_lead(
    "Sarah Johnson",
    "410-555-7890",
    "Plumbing",
    "Medium"
)


lead2 = create_lead(
    "Mike Davis",
    "301-555-4567",
    "Electrical",
    "High"
)

lead3 = create_lead(
    "Emily Brown",
    "240-555-1234",
    "HVAC",
    "Low"
)

lead4 = create_lead(
    "David Wilson",
    "443-555-9999",
    "AC Repair",
    "High",
)

new_leads = [lead, lead2, lead3, lead4]


display_lead(lead)
display_lead(lead2)
display_lead(lead3)
display_lead(lead4)


def lead_exists(lead):
    for existing_lead in leads:
        if existing_lead["phone"] == lead["phone"]:
            return True
    return False
        

for new_lead in new_leads:
    if lead_exists(new_lead):
        print("Lead already exists:", new_lead["name"])
    else:
        leads.append(new_lead)
        print("Lead added:", new_lead["name"])




print(leads)

name = input("Enter customer name: ")
phone = input("Enter phone number: ")
service = input("Enter service needed: ")
message = input("Describe your problem: ")
urgency = determine_urgency(message)

new_lead = create_lead(
    name,
    phone,
    service,
    urgency
)

display_lead(new_lead)

if lead_exists(new_lead):
    print("Lead already exists")
else:
    leads.append(new_lead)
    print("New lead added")


with open("week1/leads.json", "w") as file:
    json.dump(leads, file, indent=4)