from flask import Flask, request, render_template
import string

app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/')
def display_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def validate_form():
    chosen_username = request.form['username']
    password = request.form['password']
    verified_password = request.form['verify']
    chosen_email = request.form['email']
    invalidChars = set(' ')
    errors_present = False
    username_error = False
    email_error = False



    # Here we will check the validity of the username. It cannot contain spaces, be empty, be less than 3 character or longer than 20 characters.
    if any(char in invalidChars for char in chosen_username) or  len(chosen_username)<3 or  len(chosen_username)>20 or chosen_username == "":
        username_error_msg = "That is not a valid username"
        errors_present = True
        username_error = True
    else:
        username_error_msg = ""
        username_error = False


    # Here we validate the password. It follows the same rules as the username.
    if any(char in invalidChars for char in password) or  len(password)<3 or  len(password)>20:
        password_error_msg = "That is not a valid password"
        errors_present = True
    else:
        password_error_msg = ""

    # Here we validate the 'verify password' field. If it does not match the passowrd it throws an error
    ver_pass_err_stat = verified_password != password
    if ver_pass_err_stat == True:
        verify_error_msg = "Passwords do not match"
        errors_present = True
    else:
        verify_error_msg = ""

    # Here we validate the email. It can be left blank but if it does contain characters we check to see if it is a valid email by looking for the @ symbol and '.' character
    if chosen_email != "":
        #if any(char in validChars for char not in chosen_email):
        if "@" not in chosen_email or "." not in chosen_email or " " in chosen_email or chosen_email.count('@')>1 or chosen_email.count('.')>1:
            email_error_msg = "That is not a valid email address"
            errors_present = True
            email_error = True
        else:
            email_error_msg = ""
            email_error = False
    else:
        email_error_msg = ""
        email_error = False

    # If there are any errors present it will rerender the form with a blanket display of any present errors. If there are no errors present then it will render the 'Welcome' template instead. 
    if username_error == True:
        returned_username = ""
    else:
        returned_username = chosen_username

    if email_error == True:
        returned_email = ""
    else:
        returned_email = chosen_email

    if errors_present == True:
        return render_template('index.html', 
        username = returned_username,
        username_error = username_error_msg,
        password_error = password_error_msg,
        verify_error = verify_error_msg,
        email = returned_email,
        email_error = email_error_msg
        )
    else:
        
        return render_template('/welcome.html', new_user = chosen_username)



app.run()
