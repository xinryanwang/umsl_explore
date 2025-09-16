from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Basic Information
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    date_of_birth = db.Column(db.Date)
    
    # Address
    address_line1 = db.Column(db.String(200))
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(120))
    state = db.Column(db.String(80))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(80))
    
    # School Information
    school = db.Column(db.String(160))
    grade = db.Column(db.String(40))
    gpa = db.Column(db.String(10))
    graduation_year = db.Column(db.String(10))
    
    # Academic Plans
    academic_plan = db.Column(db.Text)  # brief academic goals or interests
    anticipated_major = db.Column(db.String(160))
    anticipated_start_semester = db.Column(db.String(40))  # e.g., Fall, Spring, Summer
    anticipated_start_year = db.Column(db.String(10))
    
    # Event Details
    guests = db.Column(db.Integer, default=0)
    tshirt_size = db.Column(db.String(10))
    dietary_restrictions = db.Column(db.Text)
    
    # Emergency Contact
    emergency_contact_name = db.Column(db.String(120))
    emergency_contact_phone = db.Column(db.String(40))
    emergency_contact_relationship = db.Column(db.String(60))
    
    # Additional Information
    interests = db.Column(db.Text)  # Engineering disciplines of interest
    transportation = db.Column(db.String(100))  # How they plan to get to event
    first_time_attendee = db.Column(db.Boolean, default=True)
    heard_about_event = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    # Parent/Guardian (optional)
    guardian_name = db.Column(db.String(120))
    guardian_email = db.Column(db.String(120))

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Initialized the database.')

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Basic Information
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        date_of_birth = request.form.get('date_of_birth', '').strip()
        
        # Address
        address_line1 = request.form.get('address_line1', '').strip()
        address_line2 = request.form.get('address_line2', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()
        postal_code = request.form.get('postal_code', '').strip()
        country = request.form.get('country', '').strip()
        
        # School Information
        school = request.form.get('school', '').strip()
        grade = request.form.get('grade', '').strip()
        gpa = request.form.get('gpa', '').strip()
        graduation_year = request.form.get('graduation_year', '').strip()
        
        # Academic Plans
        academic_plan = request.form.get('academic_plan', '').strip()
        anticipated_major = request.form.get('anticipated_major', '').strip()
        anticipated_start_semester = request.form.get('anticipated_start_semester', '').strip()
        anticipated_start_year = request.form.get('anticipated_start_year', '').strip()
        
        # Event Details
        guests = request.form.get('guests', '0').strip()
        tshirt_size = request.form.get('tshirt_size', '').strip()
        dietary_restrictions = request.form.get('dietary_restrictions', '').strip()
        
        # Emergency Contact
        emergency_contact_name = request.form.get('emergency_contact_name', '').strip()
        emergency_contact_phone = request.form.get('emergency_contact_phone', '').strip()
        emergency_contact_relationship = request.form.get('emergency_contact_relationship', '').strip()
        
        # Parent/Guardian
        guardian_name = request.form.get('guardian_name', '').strip()
        guardian_email = request.form.get('guardian_email', '').strip()

        # Additional Information
        interests = request.form.get('interests', '').strip()
        transportation = request.form.get('transportation', '').strip()
        first_time_attendee = request.form.get('first_time_attendee') == 'on'
        heard_about_event = request.form.get('heard_about_event', '').strip()
        notes = request.form.get('notes', '').strip()

        # Server-side required field checks
        required_fields = [
            full_name, email, phone, date_of_birth,
            address_line1, address_line2, city, state, postal_code, country,
            school, grade, gpa, graduation_year,
            anticipated_major, anticipated_start_semester, anticipated_start_year, academic_plan,
            guests, tshirt_size, dietary_restrictions,
            emergency_contact_name, emergency_contact_phone, emergency_contact_relationship,
            interests, transportation, heard_about_event, notes,
            guardian_name, guardian_email,
        ]
        if any(f is None or f == '' for f in required_fields):
            flash('Please complete all required fields.', 'error')
            return redirect(url_for("register"))

        try:
            guests_num = int(guests) if guests else 0
        except ValueError:
            guests_num = 0

        # Parse date of birth
        dob = None
        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                pass

        reg = Registration(
            full_name=full_name,
            email=email,
            phone=phone,
            date_of_birth=dob,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            school=school,
            grade=grade,
            gpa=gpa,
            graduation_year=graduation_year,
            academic_plan=academic_plan,
            anticipated_major=anticipated_major,
            anticipated_start_semester=anticipated_start_semester,
            anticipated_start_year=anticipated_start_year,
            guests=guests_num,
            tshirt_size=tshirt_size,
            dietary_restrictions=dietary_restrictions,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            emergency_contact_relationship=emergency_contact_relationship,
            guardian_name=guardian_name,
            guardian_email=guardian_email,
            interests=interests,
            transportation=transportation,
            first_time_attendee=first_time_attendee,
            heard_about_event=heard_about_event,
            notes=notes,
        )
        db.session.add(reg)
        db.session.commit()
        flash('Registration received! We look forward to seeing you.', 'success')
        return redirect(url_for("thank_you"))

    return render_template("register.html")

@app.route('/thank-you')
def thank_you():
    return render_template("thank_you.html")

@app.route('/admin')
def admin():
    regs = Registration.query.order_by(Registration.created_at.desc()).all()
    return render_template("admin.html", regs=regs)

if __name__ == '__main__':
    app.run(debug=True)
