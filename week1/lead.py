def determine_priority(urgency):
    if urgency == "High":
        return "URGENT"
    elif urgency == "Medium":
        return "NORMAL"
    else:
        return "LOW"


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


display_lead(lead)
display_lead(lead2)
display_lead(lead3)
display_lead(lead4)

