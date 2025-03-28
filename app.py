from flask import Flask, render_template_string, request, redirect
import sqlite3

app = Flask(__name__)

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database (run once)
def initialize_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
initialize_db()

# Route for the home page (view expenses)
@app.route('/')
def index():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()

    # HTML and CSS combined in render_template_string
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Expense Tracker</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    width: 80%;
                    margin: 0 auto;
                    padding: 30px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .expense-form input, .expense-form button {
                    padding: 10px;
                    margin: 10px;
                    width: 100%;
                    box-sizing: border-box;
                }
                .expense-form button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                .expense-form button:hover {
                    background-color: #45a049;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 30px;
                }
                table th, table td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                table th {
                    background-color: #f4f4f4;
                }
                table tr:hover {
                    background-color: #f1f1f1;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Expense Tracker</h1>
                <!-- Add Expense Form -->
                <form action="/add" method="POST" class="expense-form">
                    <input type="text" name="description" placeholder="Description" required>
                    <input type="text" name="category" placeholder="Category" required>
                    <input type="number" name="amount" placeholder="Amount" required>
                    <input type="date" name="date" required>
                    <button type="submit">Add Expense</button>
                </form>

                <!-- Display Expenses -->
                <table>
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th>Category</th>
                            <th>Amount</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for expense in expenses %}
                        <tr>
                            <td>{{ expense['description'] }}</td>
                            <td>{{ expense['category'] }}</td>
                            <td>{{ expense['amount'] }}</td>
                            <td>{{ expense['date'] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
    ''', expenses=expenses)

# Route for adding a new expense
@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form['description']
    category = request.form['category']
    amount = request.form['amount']
    date = request.form['date']

    conn = get_db_connection()
    conn.execute('INSERT INTO expenses (description, category, amount, date) VALUES (?, ?, ?, ?)',
                 (description, category, amount, date))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


