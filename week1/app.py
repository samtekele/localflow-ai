from flask import Flask, request

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

    return """
    <h1>LocalFlow AI</h1>

    <a href="/dashboard">View Dashboard</a>
    |
    <a href="/urgent">View Urgent Leads</a>

    <br><br>

    <form method="POST">
        <label>Customer Message:</label><br>
        <textarea name="message" rows="6" cols="50"></textarea><br><br>

        <label>Phone Number:</label><br>
        <input type="text" name="phone"><br><br>

        <button type="submit">Submit Lead</button>
    </form>
    """


@app.route("/dashboard")
def dashboard():
    lead_rows = ""

    for lead in leads:
        lead_rows += f"""
        <tr>
            <td>{lead.get("id", "N/A")}</td>
            <td>{lead["name"]}</td>
            <td>{lead["phone"]}</td>
            <td>{lead["service"]}</td>
            <td>{lead["urgency"]}</td>
            <td>{lead["priority"]}</td>
            <td>{lead["status"]}</td>
        </tr>
        """

    return f"""
    <h1>LocalFlow AI Dashboard</h1>

    <a href="/">Add New Lead</a>
    |
    <a href="/urgent">View Urgent Leads</a>

    <br><br>

    <table border="1" cellpadding="8">
        <tr>
            <th>Lead ID</th>
            <th>Name</th>
            <th>Phone</th>
            <th>Service</th>
            <th>Urgency</th>
            <th>Priority</th>
            <th>Status</th>
        </tr>

        {lead_rows}
    </table>
    """


@app.route("/urgent")
def urgent_leads():
    lead_rows = ""

    for lead in leads:
        if lead["priority"] == "URGENT":
            lead_rows += f"""
            <tr>
                <td>{lead.get("id", "N/A")}</td>
                <td>{lead["name"]}</td>
                <td>{lead["phone"]}</td>
                <td>{lead["service"]}</td>
                <td>{lead["priority"]}</td>
                <td>{lead["status"]}</td>
            </tr>
            """

    return f"""
    <h1>Urgent Leads</h1>

    <a href="/dashboard">All Leads</a>
    |
    <a href="/">Add New Lead</a>

    <br><br>

    <table border="1" cellpadding="8">
        <tr>
            <th>Lead ID</th>
            <th>Name</th>
            <th>Phone</th>
            <th>Service</th>
            <th>Priority</th>
            <th>Status</th>
        </tr>

        {lead_rows}
    </table>
    """


if __name__ == "__main__":
    app.run(debug=True)