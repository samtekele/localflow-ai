from flask import Flask, request, render_template

from lead import process_lead, lead_exists, leads, save_leads


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        message = request.form["message"]
        phone = request.form["phone"]

        new_lead = process_lead(message, phone)

        if lead_exists(new_lead):
            return """
            <h1>Lead Already Exists</h1>

            <a href="/">Submit Another Lead</a>
            |
            <a href="/dashboard">View Dashboard</a>
            """

        leads.append(new_lead)
        save_leads()

        return f"""
        <h1>Lead Successfully Added!</h1>

        <p><strong>Lead ID:</strong> {new_lead["id"]}</p>
        <p><strong>Name:</strong> {new_lead["name"]}</p>
        <p><strong>Phone:</strong> {new_lead["phone"]}</p>
        <p><strong>Service:</strong> {new_lead["service"]}</p>
        <p><strong>Urgency:</strong> {new_lead["urgency"]}</p>
        <p><strong>Priority:</strong> {new_lead["priority"]}</p>
        <p><strong>Status:</strong> {new_lead["status"]}</p>
        <p><strong>Created:</strong> {new_lead["created_at"]}</p>

        <a href="/">Submit Another Lead</a>
        |
        <a href="/dashboard">View Dashboard</a>
        |
        <a href="/urgent">View Urgent Leads</a>
        """

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    total_leads = len(leads)

    urgent_count = 0
    for lead in leads:
        if lead["priority"] == "URGENT":
            urgent_count += 1

    new_count = 0
    for lead in leads:
        if lead["status"] == "New":
            new_count += 1

    completed_count = 0
    for lead in leads:
        if lead["status"] == "Completed":
            completed_count += 1
    

    return render_template(
        "dashboard.html",
        leads=leads,
        total_leads=total_leads,
        urgent_count=urgent_count,
        new_count=new_count,
        completed_count=completed_count
    )

    
def urgent_leads():
    return render_template("urgent.html", leads=leads)

if __name__ == "__main__":
    app.run(debug=True)