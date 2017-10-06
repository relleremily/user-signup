from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()


def is_correct_char_count(word):
    try:
        if (len(word) > 2 and len(word) < 21):
            return True
    except ValueError:
        return False

def is_num_or_letter(word):
    try:
        for char in word:
            if word.isdigit() or word.isalpha():
                return True
    except ValueError:
        return False

def is_valid_email_characters(word):
    try:
        for char in word:
            if word.isdigit() or word.isalpha() or '@' in word or '.' in word:
                return True
    except ValueError:
        return False

def is_mandatory_characters(word):
    try:
        if '@' and '.' in word:
            return True
    except ValueError:
        return False

def is_same_password(word1, word2):
    try:
        if word1 == word2:
            return True
    except ValueError:
        return False

def is_blank(word):
    try:
        if word == '':
            return True
    except ValueError:
        return False





@app.route('/validate-inputs', methods=['POST'])
def validate_inputs():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    if username == '':
        username_error = 'Required'
    else:
        if not is_correct_char_count(username):
            username_error = 'Username must be between 3 and 20 characters'
            username = ''
        else:
            if not is_num_or_letter(username):
                username_error = 'Username must contain only letters and numbers'
                username = ''


    if password == '':
        password_error = 'Required'
    else:
        if not is_correct_char_count(password):
            password_error = 'Password must be between 3 and 20 characters'
            password = ''
        else:
            if not is_num_or_letter(password):
                password_error = 'Password must contain only letters and numbers'
                password = ''


    if verify_password == '':
        verify_password_error = 'Required'
    else:
        if not is_correct_char_count(verify_password):
            verify_password_error = 'Password must be between 3 and 20 characters'
            verify_password = ''
        else:
            if not is_num_or_letter(verify_password):
                verify_password_error = 'Password must contain only letters and numbers'
                verify_password = ''
            else:
                if not is_same_password(password, verify_password):
                    verify_password_error = 'Passwords do not match'
                    verify_password = ''



    while email == '':
        break
    else:
        if not is_valid_email_characters(email):
            email_error = 'Invalid email'
            email = ''
        else:
            if not is_mandatory_characters(email):
                email_error = 'Invalid email, must contain @ and .'
            else:
                if not is_correct_char_count(email):
                    email_error = 'Invalid email...email is too long or too short'


    if not username_error and not password_error and not verify_password_error and not email_error:
        return redirect('/welcome?username={0}'.format(username))
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email_error=email_error, username=username, email=email)

@app.route('/welcome', methods=['GET'])
def welcome():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)




app.run()