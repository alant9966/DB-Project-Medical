from flask import Flask, render_template, request, abort, redirect, url_for, jsonify, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, time as dt_time
import pymysql.cursors
import config

app = Flask(__name__)

app.config.from_object(config)
mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to /login if user is not logged in
login_manager.login_message = "Please log in to access this page."

# Allowed input fields for the 'Patient' table
ALLOWED_PATIENT_FIELDS = [
    'address', 
    'date_of_birth'
]

# Allowed input fields for the 'Insurance' table
ALLOWED_INSURANCE_FIELDS = [
    'insurance_id',
    'company',
    'date_of_expiry'
]

# Allowed input fields for the 'Doctor' table
ALLOWED_DOCTOR_FIELDS = [
    'doctor_address',
    'department_id',
    'years_of_experience'
]


# Represents a User
class User(UserMixin):
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role


# Load a user from the current session
@login_manager.user_loader
def load_user(user_id):
    try:
        # Fetch the appropriate user
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM User
                       WHERE user_id = %s
                    """, (user_id,))
        user_row = cur.fetchone()
        cur.close()
        
        # Load the user if found
        if (user_row):
            return User(
                       id = user_row['user_id'], 
                       email = user_row['email'], 
                       role = user_row['role']
                    )
            
    # Catch any exceptions
    except Exception as e:
        print(f"Error loading user: {e}")
        

# User Registration (Patient)
@app.route('/register-patient', methods=['GET', 'POST'])
def register_patient():
    if (request.method == 'POST'):
        # Retrieve registration form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('date_of_birth')
        address = request.form.get('address')
        
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        try:
            # Check for existing users
            cur.execute("""SELECT user_id
                           FROM User
                           WHERE email = %s
                        """, (email,))
            if (cur.fetchone()):
                flash('That email address is already in use.', 'error')
                return redirect(url_for('register_patient'))

            # Hash the password
            password_hash = generate_password_hash(password)

            # Check if the patient exists in the database
            cur.execute("""SELECT patient_id, user_id
                           FROM patient 
                           WHERE first_name = %s
                               AND last_name = %s
                               AND address = %s
                        """, (first_name, last_name, address))
            patient = cur.fetchone()

            # If the patient exists...
            if (patient):
                # Error: Patient is already registered
                if (patient['user_id'] is not None):
                    flash('Your account is already registered. Please try logging in.', 'warning')
                    return redirect(url_for('login'))
                else:
                    # Create a new User
                    cur.execute("""INSERT INTO User (email, password, role)
                                   VALUES (%s, %s, 'patient')
                                """, (email, password_hash))
                    new_user_id = cur.lastrowid
                    
                    # Link the User and existing Patient
                    cur.execute("""UPDATE patient
                                   SET user_id = %s
                                   WHERE patient_id = %s
                                """, (new_user_id, patient['patient_id']))
                    
                    # Create insurance entry for the patient
                    cur.execute("""INSERT INTO insurance (patient_id)
                                   VALUES (%s)
                                """, (patient['patient_id'],))
                    
                    # Create medical record entry for the patient
                    cur.execute("""INSERT INTO medicalrecord (patient_id)
                                   VALUES (%s)
                                """, (patient['patient_id'],))
                    
                    flash('Account registered! Please log in.', 'success')
                    
            # If the patient does not yet exist...
            else:
                # Create a new User
                cur.execute("""INSERT INTO User (email, password, role)
                               VALUES (%s, %s, 'patient')
                            """, (email, password_hash))
                new_user_id = cur.lastrowid
                
                # Create a new Patient
                cur.execute("""INSERT INTO patient (user_id, first_name,
                                   last_name, date_of_birth, address)
                               VALUES (%s, %s, %s, %s, %s)
                            """, (new_user_id, first_name, last_name, dob, address))
                new_patient_id = cur.lastrowid
                
                # Create insurance entry for the patient
                cur.execute("""INSERT INTO insurance (patient_id)
                               VALUES (%s)
                            """, (new_patient_id,))
                
                # Create medical record entry for the patient
                cur.execute("""INSERT INTO medicalrecord (patient_id)
                               VALUES (%s)
                            """, (new_patient_id,))
                
                flash('Account registered! Please log in.', 'success')

            # Commit changes to the database
            mysql.connection.commit()
            return redirect(url_for('login'))
        
        except Exception as e:
            mysql.connection.rollback()
            flash(f'An error occurred: {e}', 'error')
        
        finally:
            cur.close()

    return render_template('register_patient.html')
        
        
# User Registration (Doctor)
@app.route('/register-doctor', methods=['GET', 'POST'])
def register_doctor():
    if (request.method == 'POST'):
        # Retrieve registration form data
        first_name = request.form.get('doctor_firstname')
        last_name = request.form.get('doctor_lastname')
        department = request.form.get('department_id')
        address = request.form.get('doctor_address')
        
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        try:
            # Check for existing users
            cur.execute("""SELECT user_id
                           FROM User
                           WHERE email = %s
                        """, (email,))
            if (cur.fetchone()):
                flash('That email address is already in use.', 'error')
                return redirect(url_for('register_doctor'))

            # Hash the password
            password_hash = generate_password_hash(password)

            # Check if the doctor exists in the database
            cur.execute("""SELECT doctor_id, user_id
                           FROM doctor 
                           WHERE doctor_firstname = %s
                               AND doctor_lastname = %s
                               AND doctor_address = %s
                               AND department_id = %s
                        """, (first_name, last_name, address, department))
            doctor = cur.fetchone()

            # If the doctor exists...
            if (doctor):
                # Error: Doctor is already registered
                if (doctor['user_id'] is not None):
                    flash('Your account is already registered. Please try logging in.', 'warning')
                    return redirect(url_for('login'))
                else:
                    # Create a new User
                    cur.execute("""INSERT INTO User (email, password, role)
                                   VALUES (%s, %s, 'doctor')
                                """, (email, password_hash))
                    new_user_id = cur.lastrowid
                    
                    # Link the User and existing Doctor
                    cur.execute("""UPDATE doctor
                                   SET user_id = %s
                                   WHERE doctor_id = %s
                                """, (new_user_id, doctor['doctor_id']))
                    
                    flash('Account registered! Please log in.', 'success')
                    
            # If the doctor does not yet exist...
            else:
                # Create a new User
                cur.execute("""INSERT INTO User (email, password, role)
                               VALUES (%s, %s, 'doctor')
                            """, (email, password_hash))
                new_user_id = cur.lastrowid
                
                # Create a new Doctor
                cur.execute("""INSERT INTO doctor (user_id, doctor_firstname,
                                   doctor_lastname, doctor_address, department_id)
                               VALUES (%s, %s, %s, %s, %s)
                            """, (new_user_id, first_name, last_name, address, department))
                
                flash('Account registered! Please log in.', 'success')

            # Commit changes to the database
            mysql.connection.commit()
            return redirect(url_for('login'))
        
        except Exception as e:
            mysql.connection.rollback()
            flash(f'An error occurred: {e}', 'error')
        
        finally:
            cur.close()

    return render_template('register_doctor.html')


# User Login
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is logged in, redirect to the homepage
    if (current_user.is_authenticated):
        if (current_user.role == 'patient'):
            return redirect(url_for('patient_home'))
        elif (current_user.role == 'doctor'):
            return redirect(url_for('doctor_home'))
    
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve the user from the database
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM User
                       WHERE email = %s
                    """, (email,))
        user_row = cur.fetchone()
        cur.close()

        # Check that the user exists, and the password is correct
        if (user_row and check_password_hash(user_row['password'], password)):
            # Log in the user (session start)
            curr_user = User(
                            id = user_row['user_id'],
                            email = user_row['email'],
                            role = user_row['role']
                        )
            login_user(curr_user) # This creates the session
            
            # Redirect to the appropriate homepage
            if (curr_user.role == 'patient'):
                return redirect(url_for('patient_home'))
            elif (curr_user.role == 'doctor'):
                return redirect(url_for('doctor_home'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


# User Logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Route for Patient Homepage
@app.route('/patient/home')
@login_required
def patient_home():
    # Check that the user is a patient
    if (current_user.role != 'patient'):
        abort(403)
    
    # Retrieve data using the user's ID
    cur = mysql.connection.cursor()
    patient_data = None
    upcoming_appointments = []
    
    try:
        cur.execute("""SELECT p.*, i.*
                       FROM patient p
                       LEFT JOIN insurance i
                       ON p.patient_id = i.patient_id
                       WHERE p.user_id = %s""", (current_user.id,))
        patient_data = cur.fetchone()
        
        # Check that the patient exists
        if (not patient_data):
            abort(404)
        
        patient_id = patient_data['patient_id']
        
        # Fetch upcoming appointments in the next 7 days
        today = datetime.now().date()
        seven_days_later = today + timedelta(days=7)
        
        cur.execute("""SELECT a.appointment_id, a.appointment_date, a.appointment_time, 
                              a.description, d.doctor_firstname, d.doctor_lastname, r.room_id
                       FROM appointment a
                       LEFT JOIN doctor d ON a.doctor_id = d.doctor_id
                       LEFT JOIN room r ON a.room_id = r.room_id
                       WHERE a.patient_id = %s
                           AND a.appointment_date >= %s
                           AND a.appointment_date <= %s
                       ORDER BY a.appointment_date ASC, a.appointment_time ASC
                    """, (patient_id, today, seven_days_later))
        appointments_raw = cur.fetchall()
        
        # Convert timedelta objects to time objects for appointment_time
        upcoming_appointments = []
        for appt in appointments_raw:
            if (hasattr(appt, 'keys')):
                appt_dict = dict(appt)
            else:
                appt_dict = appt
            
            if (appt_dict.get('appointment_time')):
                appt_time = appt_dict['appointment_time']
                if (isinstance(appt_time, timedelta)):
                    # Convert timedelta to time
                    total_seconds = int(appt_time.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    appt_dict['appointment_time'] = dt_time(hours, minutes, seconds)
            
            upcoming_appointments.append(appt_dict)
        
    except Exception as e:
        mysql.connection.rollback()
        flash(f'An error occurred: {e}', 'error')
        upcoming_appointments = []
    
    finally:
        cur.close()

    return render_template('patient/home.html', patient=patient_data, appointments=upcoming_appointments)


@app.route('/patient/search-appointments', methods=['POST'])
@login_required
def search_appointments():
    # Check that the user is a patient
    if (current_user.role != 'patient'):
        abort(403)
    
    data = request.json
    search_query = data.get('query', '').strip()
    
    cur = mysql.connection.cursor()
    try:
        # Get patient_id for the logged-in user
        cur.execute("""SELECT patient_id
                       FROM patient
                       WHERE user_id = %s
                    """, (current_user.id,))
        patient = cur.fetchone()
        
        if (not patient):
            abort(404)
        
        patient_id = patient['patient_id']
        
        # Calculate date range (next 7 days)
        today = datetime.now().date()
        seven_days_later = today + timedelta(days=7)
        
        if (search_query):
            # Call the stored procedure
            cur.execute("""CALL search_appointment(%s, %s, %s, %s)""", 
                       (patient_id, today, seven_days_later, search_query))
            results = cur.fetchall()
        else:
            # If no query, return all appointments in next 7 days
            cur.execute("""SELECT a.appointment_id, a.appointment_date, a.appointment_time, 
                                  a.description, d.doctor_firstname, d.doctor_lastname, r.room_id
                           FROM appointment a
                           LEFT JOIN doctor d ON a.doctor_id = d.doctor_id
                           LEFT JOIN room r ON a.room_id = r.room_id
                           WHERE a.patient_id = %s
                               AND a.appointment_date >= %s
                               AND a.appointment_date <= %s
                           ORDER BY a.appointment_date ASC, a.appointment_time ASC
                        """, (patient_id, today, seven_days_later))
            results = cur.fetchall()
        
        # Format the results for JSON response
        appointments = []
        for row in results:
            appointments.append({
                'appointment_id': row.get('appointment_id'),
                'appointment_date': row.get('appointment_date').strftime('%Y-%m-%d') if row.get('appointment_date') else None,
                'appointment_time': str(row.get('appointment_time')) if row.get('appointment_time') else None,
                'description': row.get('description') or 'No description',
                'doctor_firstname': row.get('doctor_firstname', ''),
                'doctor_lastname': row.get('doctor_lastname', ''),
                'room_id': row.get('room_id')
            })
        
        return jsonify({
            "success": True,
            "appointments": appointments
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
    
    finally:
        cur.close()


@app.route('/patient/update', methods=['POST'])
@login_required
def update_patient_info():
    data = request.json
    update_field = data.get('field')
    new_value = data.get('value')
    patient_id = data.get('patient_id') 
    
    cur = mysql.connection.cursor()
    try:
        # Retrieve the logged-in patient
        cur.execute("""SELECT patient_id
                       FROM patient
                       WHERE user_id = %s
                    """, (current_user.id,))
        patient = cur.fetchone()
        
        if (not patient):
            return jsonify({"success": False, "message": "Patient not found."}), 404
        
        # Check that the user is editing their own data
        patient_db_id = patient['patient_id']
        if (str(patient_db_id) != str(patient_id)):
            return jsonify({"success": False, "message": "Authorization error."}), 403

        # Initialize response value
        response_value = new_value
        
        # Update the Patient table
        if (update_field in ALLOWED_PATIENT_FIELDS):
            # Handle date format conversion for date_of_birth
            if (update_field == 'date_of_birth'):
                # Try to parse and convert date formats
                try:
                    # Check if it's already in YYYY-MM-DD format
                    if (len(new_value) == 10 and new_value.count('-') == 2):
                        parts = new_value.split('-')
                        if (len(parts[0]) == 4):  # YYYY-MM-DD format
                            formatted_date = new_value
                        else:  # MM-DD-YYYY format
                            month, day, year = parts
                            formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        return jsonify({"success": False, "message": "Invalid date format. Use MM-DD-YYYY or YYYY-MM-DD."}), 400
                    
                    # Validate the date
                    datetime.strptime(formatted_date, '%Y-%m-%d')
                    new_value = formatted_date
                    
                except ValueError:
                    return jsonify({"success": False, "message": "Invalid date. Please use MM-DD-YYYY or YYYY-MM-DD format."}), 400
            
            cur.execute(f"""UPDATE patient 
                            SET `{update_field}` = %s 
                            WHERE patient_id = %s
                        """, (new_value, patient_db_id))
            
            # Format the response value for date_of_birth
            if (update_field == 'date_of_birth' and new_value):
                try:
                    date_obj = datetime.strptime(new_value, '%Y-%m-%d').date()
                    response_value = date_obj.strftime('%m-%d-%Y')
                except:
                    response_value = new_value
                    
        # (Or) Update the Insurance table
        elif (update_field in ALLOWED_INSURANCE_FIELDS):
            # Handle date format conversion for date_of_expiry
            if (update_field == 'date_of_expiry' and new_value):
                try:
                    # Check if it's already in YYYY-MM-DD format
                    if (len(new_value) == 10 and new_value.count('-') == 2):
                        parts = new_value.split('-')
                        if (len(parts[0]) == 4):  # YYYY-MM-DD format
                            formatted_date = new_value
                        else:  # MM-DD-YYYY format
                            month, day, year = parts
                            formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    else:
                        return jsonify({"success": False, "message": "Invalid date format. Use MM-DD-YYYY or YYYY-MM-DD."}), 400
                    
                    # Validate the date
                    datetime.strptime(formatted_date, '%Y-%m-%d')
                    new_value = formatted_date
                    
                except ValueError:
                    return jsonify({"success": False, "message": "Invalid date. Please use MM-DD-YYYY or YYYY-MM-DD format."}), 400
            
            cur.execute(f"""UPDATE insurance 
                            SET `{update_field}` = %s 
                            WHERE patient_id = %s
                        """, (new_value, patient_db_id))
            
            # Format the response value for date_of_expiry
            if (update_field == 'date_of_expiry' and new_value):
                try:
                    date_obj = datetime.strptime(new_value, '%Y-%m-%d').date()
                    response_value = date_obj.strftime('%m-%d-%Y')
                except:
                    response_value = new_value
        else:
            return jsonify({"success": False, "message": "Invalid field."}), 400
        
        # Commit the queries and send a response
        mysql.connection.commit()
        return jsonify({
            "success": True, 
            "message": "Update successful", 
            "new_value": response_value
        })
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"success": False, "message": f"Error: {e}"}), 500
    
    finally:
        cur.close()


# Route for Patient Appointments
@app.route('/patient/appointments')
@login_required
def patient_appointments():
    # Check that the user is a patient
    if (current_user.role != 'patient'):
        abort(403)
    
    # Retrieve patient data and appointments
    cur = mysql.connection.cursor()
    try:
        # Get patient_id for the logged-in user
        cur.execute("""SELECT patient_id, first_name, last_name
                       FROM patient
                       WHERE user_id = %s
                    """, (current_user.id,))
        patient = cur.fetchone()
        
        if (not patient):
            abort(404)
        
        patient_id = patient['patient_id']
        
        # Fetch all appointments for this patient
        cur.execute("""SELECT a.*, d.doctor_firstname, d.doctor_lastname, r.room_id
                       FROM appointment a
                       LEFT JOIN doctor d ON a.doctor_id = d.doctor_id
                       LEFT JOIN room r ON a.room_id = r.room_id
                       WHERE a.patient_id = %s
                       ORDER BY a.appointment_date DESC, a.appointment_time DESC
                    """, (patient_id,))
        appointments = cur.fetchall()
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        appointments = []
        
    finally:
        cur.close()
    
    return render_template('patient/appointments.html', 
                         patient=patient, 
                         appointments=appointments)


# Route for Doctor Homepage
@app.route('/doctor/home')
@login_required
def doctor_home():
    # Check that the user is a doctor
    if (current_user.role != 'doctor'):
        abort(403)
    
    # Retrieve data using the user's ID
    cur = mysql.connection.cursor()
    cur.execute("""SELECT d.*, dep.*
                   FROM doctor d
                   LEFT JOIN department dep
                   ON d.department_id = dep.department_id
                   WHERE user_id = %s
                """, (current_user.id,))
    doctor_data = cur.fetchone()
    cur.close()
    
    # Check that the doctor exists
    if (not doctor_data):
        abort(404)

    return render_template('doctor/home.html', doctor=doctor_data)


@app.route('/doctor/update', methods=['POST'])
@login_required
def update_doctor_info():
    data = request.json
    update_field = data.get('field')
    new_value = data.get('value')
    doctor_id = data.get('doctor_id')
    
    cur = mysql.connection.cursor()
    try:
        # Retrieve the logged-in doctor
        cur.execute("""SELECT doctor_id
                       FROM doctor
                       WHERE user_id = %s
                    """, (current_user.id,))
        doctor = cur.fetchone()
        
        if (not doctor):
            return jsonify({"success": False, "message": "Doctor not found."}), 404
        
        # Check that the user is editing their own data
        doctor_db_id = doctor['doctor_id']
        if (str(doctor_db_id) != str(doctor_id)):
            return jsonify({"success": False, "message": "Authorization error."}), 403
        
        # Update the Doctor table
        if (update_field in ALLOWED_DOCTOR_FIELDS):
            cur.execute(f"""UPDATE doctor 
                            SET `{update_field}` = %s 
                            WHERE doctor_id = %s
                        """, (new_value, doctor_db_id))
        else:
            return jsonify({"success": False, "message": "Invalid field."}), 400
        
        # Commit the queries and send a response
        mysql.connection.commit()
        return jsonify({
            "success": True, 
            "message": "Update successful", 
            "new_value": new_value
        })
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"success": False, "message": f"Error: {e}"}), 500
    
    finally:
        cur.close()


# Route for Doctor Appointments
@app.route('/doctor/appointments')
@app.route('/doctor/appointment/<int:appointment_id>')
@login_required
def doctor_appointments(appointment_id=None):
    # Check that the user is a doctor
    if (current_user.role != 'doctor'):
        abort(403)
    
    # Get the selected date from query parameter (default to today)
    selected_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    cur = mysql.connection.cursor()
    try:
        # Get doctor_id for the logged-in user
        cur.execute("""SELECT doctor_id
                       FROM doctor
                       WHERE user_id = %s
                    """, (current_user.id,))
        doctor = cur.fetchone()
        
        if (not doctor):
            abort(404)
        
        doctor_id = doctor['doctor_id']
        
        # Determine the selected appointment and date
        selected_appointment = None
        patient = None
        
        # If appointment_id is provided in URL, fetch it first to get its date
        if (appointment_id):
            cur.execute("""SELECT a.appointment_id as id,
                                  a.appointment_time as time,
                                  a.patient_id,
                                  a.doctor_id,
                                  a.room_id,
                                  a.appointment_date as date,
                                  a.description,
                                  a.duration_minutes as duration
                           FROM appointment a
                           WHERE a.appointment_id = %s
                               AND a.doctor_id = %s
                        """, (appointment_id, doctor_id))
            selected_appointment = cur.fetchone()
            
            # Use the appointment's date if found
            if (selected_appointment):
                selected_date = selected_appointment['date'].strftime('%Y-%m-%d')
        
        # Fetch all appointments for this doctor on the selected date
        cur.execute("""SELECT a.appointment_id as id,
                              a.appointment_time as time,
                              CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                              a.patient_id,
                              a.doctor_id,
                              a.room_id,
                              a.appointment_date as date,
                              a.description,
                              a.duration_minutes as duration
                       FROM appointment a
                       LEFT JOIN patient p ON a.patient_id = p.patient_id
                       WHERE a.doctor_id = %s
                           AND a.appointment_date = %s
                       ORDER BY a.appointment_time ASC
                    """, (doctor_id, selected_date))
        appointments = cur.fetchall()
        
        # If no appointment was selected but appointments exist, select the first one
        if (not selected_appointment and appointments):
            selected_appointment = appointments[0]
            appointment_id = selected_appointment['id']
        
        # If an appointment is selected, fetch patient information
        if (selected_appointment):
            cur.execute("""SELECT patient_id as id,
                                  first_name,
                                  last_name,
                                  date_of_birth as dob,
                                  weight_lb as weight,
                                  height_in as height,
                                  age,
                                  address
                           FROM patient
                           WHERE patient_id = %s
                        """, (selected_appointment['patient_id'],))
            patient = cur.fetchone()
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        appointments = []
        selected_appointment = None
        patient = None
        
    finally:
        cur.close()
    
    return render_template('doctor/appointments.html',
                         appointments=appointments,
                         selected_date=selected_date,
                         selected_appointment=selected_appointment,
                         patient=patient)

# Route for Patient Treatments
@app.route('/patient/treatments')
@app.route('/patient/treatments/<int:prescription_id>')
@login_required
def patient_treatments(prescription_id=None):
    # Check that the user is a patient
    if (current_user.role != 'patient'):
        abort(403)
    
    cur = mysql.connection.cursor()
    try:
        # Get patient_id for the logged-in user
        cur.execute("""SELECT patient_id
                       FROM patient
                       WHERE user_id = %s
                    """, (current_user.id,))
        patient = cur.fetchone()
        
        if (not patient):
            abort(404)
        
        patient_id = patient['patient_id']
        
        # If a specific prescription_id is provided, fetch that one
        if (prescription_id):
            cur.execute("""SELECT p.prescription_id as id,
                                  t.treatment_name as name,
                                  t.duration_days as duration,
                                  t.description,
                                  CASE WHEN p.paid = TRUE THEN 0 ELSE t.bill END as total_amount,
                                  p.prescribed_on,
                                  p.notes,
                                  p.paid
                           FROM prescription p
                           JOIN treatment t ON p.treatment_name = t.treatment_name 
                               AND p.duration_days = t.duration_days
                           WHERE p.prescription_id = %s
                               AND p.patient_id = %s
                        """, (prescription_id, patient_id))
            treatment = cur.fetchone()
            
            if (not treatment):
                abort(404)
        else:
            # Fetch the most recent prescription for this patient
            cur.execute("""SELECT p.prescription_id as id,
                                  t.treatment_name as name,
                                  t.duration_days as duration,
                                  t.description,
                                  CASE WHEN p.paid = TRUE THEN 0 ELSE t.bill END as total_amount,
                                  p.prescribed_on,
                                  p.notes,
                                  p.paid
                           FROM prescription p
                           JOIN treatment t ON p.treatment_name = t.treatment_name 
                               AND p.duration_days = t.duration_days
                           WHERE p.patient_id = %s
                           ORDER BY p.prescribed_on DESC, p.prescription_id DESC
                           LIMIT 1
                        """, (patient_id,))
            treatment = cur.fetchone()
        
        # Fetch all prescriptions for the patient (for potential list view)
        cur.execute("""SELECT p.prescription_id as id,
                              t.treatment_name as name,
                              t.duration_days as duration,
                              t.description,
                              CASE WHEN p.paid = TRUE THEN 0 ELSE t.bill END as total_amount,
                              p.prescribed_on,
                              p.notes,
                              p.paid
                       FROM prescription p
                       JOIN treatment t ON p.treatment_name = t.treatment_name 
                           AND p.duration_days = t.duration_days
                       WHERE p.patient_id = %s
                       ORDER BY p.prescribed_on DESC, p.prescription_id DESC
                    """, (patient_id,))
        prescriptions = cur.fetchall()
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        treatment = None
        prescriptions = []
        
    finally:
        cur.close()
    
    return render_template('patient/treatments.html',
                         treatment=treatment,
                         prescriptions=prescriptions)


# Route for Patient Pay Bill
@app.route('/patient/treatments/<int:prescription_id>/pay', methods=['POST'])
@login_required
def patient_pay_bill(prescription_id):
    # Check that the user is a patient
    if (current_user.role != 'patient'):
        abort(403)
    
    cur = mysql.connection.cursor()
    try:
        # Get patient_id for the logged-in user
        cur.execute("""SELECT patient_id
                       FROM patient
                       WHERE user_id = %s
                    """, (current_user.id,))
        patient = cur.fetchone()
        
        if (not patient):
            return jsonify({"success": False, "message": "Patient not found."}), 404
        
        patient_id = patient['patient_id']
        
        # Verify the prescription belongs to this patient and get treatment info
        cur.execute("""SELECT p.prescription_id,
                              p.paid,
                              t.bill
                       FROM prescription p
                       JOIN treatment t ON p.treatment_name = t.treatment_name 
                           AND p.duration_days = t.duration_days
                       WHERE p.prescription_id = %s
                         AND p.patient_id = %s
                    """, (prescription_id, patient_id))
        prescription = cur.fetchone()
        
        if (not prescription):
            return jsonify({"success": False, "message": "Prescription not found or unauthorized."}), 404
        
        # Check if bill is already paid
        if (prescription['paid']):
            return jsonify({"success": False, "message": "Bill is already paid."}), 400
        
        # Update the prescription paid status to TRUE
        cur.execute("""UPDATE prescription
                       SET paid = TRUE
                       WHERE prescription_id = %s
                    """, (prescription_id,))
        
        # Commit the changes
        mysql.connection.commit()
        
        return jsonify({
            "success": True,
            "message": "Bill paid successfully!",
            "new_amount": 0
        })
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
    
    finally:
        cur.close()


# Route for Patient Medical Record
@app.route('/patient/medical-record')
@login_required
def patient_medical_record():
    # Check that the user is a patient
    if (current_user.role != 'patient'):
        abort(403)
    
    # Get search query parameter
    search_query = request.args.get('q', '').strip()
    
    cur = mysql.connection.cursor()
    try:
        # Get patient_id for the logged-in user
        cur.execute("""SELECT patient_id
                       FROM patient
                       WHERE user_id = %s
                    """, (current_user.id,))
        patient = cur.fetchone()
        
        if (not patient):
            abort(404)
        
        patient_id = patient['patient_id']
        
        # Fetch medical records for this patient
        if (search_query):
            # Search in diagnosis and result fields
            cur.execute("""SELECT medicalrecord_id as record_id,
                                  patient_id as account_id,
                                  diagnosis as diagnoses,
                                  result
                           FROM medicalrecord
                           WHERE patient_id = %s
                               AND (diagnosis LIKE %s OR result LIKE %s)
                           ORDER BY medicalrecord_id DESC
                        """, (patient_id, f'%{search_query}%', f'%{search_query}%'))
        else:
            # Fetch all medical records
            cur.execute("""SELECT medicalrecord_id as record_id,
                                  patient_id as account_id,
                                  diagnosis as diagnoses,
                                  result
                           FROM medicalrecord
                           WHERE patient_id = %s
                           ORDER BY medicalrecord_id DESC
                        """, (patient_id,))
        
        medical_records = cur.fetchall()
        
        # Retrieve the most recent medical record for display
        medical_record = medical_records[0] if medical_records else None
        
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        medical_record = None
        medical_records = []
        
    finally:
        cur.close()
    
    return render_template('patient/medical_record.html',
                         medical_record=medical_record,
                         medical_records=medical_records,
                         search_query=search_query) 