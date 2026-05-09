from flask import Flask, render_template, request
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()


# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# ADMIN LOGIN PAGE
@app.route('/admin')
def admin():
    return render_template('admin_login.html')


# ADMIN DASHBOARD
@app.route('/admin_dashboard', methods=['POST'])
def admin_dashboard():

    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "admin123":
        return render_template('index.html')

    return "Invalid Admin Login"


# ADD STUDENT RECORD
@app.route('/add_student', methods=['POST'])
def add_student():

    student_data = {
        'name': request.form['name'],
        'usn': request.form['usn'],
        'department': request.form['department'],
        'marks': request.form['marks']
    }

    previous_block = blockchain.get_previous_block()
    previous_hash = previous_block['hash']

    blockchain.create_block(previous_hash, student_data)

    return '''
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>

        <div class="container">

            <div class="logo">✅</div>

            <h1>Student Record Added Successfully!</h1>

            <br>

            <a href="/">
                <button>Go Back Home</button>
            </a>

        </div>

    </body>
    </html>
    '''


# STUDENT LOGIN PAGE
@app.route('/student')
def student():
    return render_template('student_login.html')


# STUDENT DASHBOARD
@app.route('/student_dashboard', methods=['POST'])
def student_dashboard():

    usn = request.form['usn']

    for block in blockchain.chain:

        student_data = block['student_data']

        if student_data.get('usn') == usn:

            return f'''
            <html>

            <head>

                <title>Student Record</title>

                <link rel="stylesheet" href="/static/style.css">

            </head>

            <body>

                <div class="container">

                    <div class="logo">📄</div>

                    <h1>Student Record</h1>

                    <div class="card">

                        <p><b>Name:</b> {student_data['name']}</p>

                        <p><b>USN:</b> {student_data['usn']}</p>

                        <p><b>Department:</b> {student_data['department']}</p>

                        <p><b>Marks:</b> {student_data['marks']}</p>

                    </div>

                    <br>

                    <a href="/">
                        <button>Back Home</button>
                    </a>

                </div>

            </body>

            </html>
            '''

    return '''
    <html>

    <head>

        <link rel="stylesheet" href="/static/style.css">

    </head>

    <body>

        <div class="container">

            <div class="logo">❌</div>

            <h1>Student Record Not Found</h1>

            <br>

            <a href="/student">
                <button>Try Again</button>
            </a>

        </div>

    </body>

    </html>
    '''


# VIEW BLOCKCHAIN
@app.route('/chain')
def chain():
    return {
        'chain': blockchain.chain
    }


if __name__ == '__main__':
    app.run(debug=True)