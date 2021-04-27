from django.shortcuts import render
from django.http import HttpResponse
from .models import myusers
from django.contrib import messages
from mysql.connector import connection
import random
import string
import re

#############################################################################################
cnx = connection.MySQLConnection(user='root', password='7aMoudi72571',  # need to specify password here
								 host='localhost', database='online_consultation',
								 auth_plugin='mysql_native_password')
#############################################################################################

if cnx.is_connected():
	print("connected to MySQL database")


def CheckIfUserAlreadyExists(email):
	"""
    Parameters
    ----------
    email : TYPE string

    Returns
    -------
    email_found : TYPE string
    "yes" if the email already exists in the database
    "no" otherwise
    """
	cursor = cnx.cursor()
	query = "SELECT email FROM users"
	cursor.execute(query)
	result = cursor.fetchall()
	emails_list = [item[0] for item in result]

	email_found = "no"
	for i in range(len(emails_list)):
		if email and email == emails_list[i]:
			email_found = "yes"
			break
	return email_found


###############
# we can define a function IsValidEmail that takes in the email as input to check if the email is valid
# we can define a function IsValidPassword that takes in the password as input to check if the password is valid
###############
def RegisterUser(first_name, last_name, birth_date, gender, email, password, re_password, country, city, medical_records):
	"""
    RegisterUser: function to register a user and add them to the database
    ----------------
    Parameters:
        takes first_name, last_name, birth_date, gender, email, password, re_password, country, city
    ----------------
    Returns String
    "Registration Successful" if the user is added to the database
    "Registration not successful, try again" if the user is not added to the database
    "email already exists" if the email already exists
    "passwords do not match" if password and re_password are not the same
    "birthdate should not be empty"
    """
	cursor = cnx.cursor()
	cursor1 = cnx.cursor()
	birth_date = str(birth_date)
	# changing birthday to correct type: YYYY-MM-DD instead of MM-DD-YYYY

	#if len(birth_date) >= 10:
	#	str1 = str[6:10]
	#	str2 = str[0:5]
	#	print(str1)
	#	print(str2)
	#	birth_date = str1 + "-" + str2


	# checking if password and re_password are matching
	if password != re_password:
		print("passwords do not match")
		return "passwords do not match"

	if birth_date == "":
		return "birthdate should not be empty"

	check_if_email_already_exists = CheckIfUserAlreadyExists(email)
	if check_if_email_already_exists == "yes":
		print("email already exists")
		return "email already exists"

	#############################
	# we can add here the functions IsValidEmail and IsValidPassword
	#############################
	try:
		location = str(country) + " " + str(city)
	except Exception as e:
		print("there is something wrong with country or city", e.args)
	is_patient_added = "Registration not successful, try again"
	try:
		query = "INSERT INTO online_consultation.users (email, pass, first_name, last_name, dob, gender, location) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		query1 = "INSERT INTO online_consultation.patients (email, medical_records) VALUES (%s,%s)"
		if location == " ":
			query = "INSERT INTO online_consultation.users (email, pass, first_name, last_name, dob, gender) VALUES (%s,%s,%s,%s,%s,%s)"
			cursor.execute(query, (email, password, first_name, last_name, birth_date, gender))
			cnx.commit()
			is_patient_added = "Registration Successful"
			print("user added to the database")
		else:
			cursor.execute(query, (email, password, first_name, last_name, birth_date, gender, location))
			cnx.commit()
			is_patient_added = "Registration Successful"
			print("user added to the database")
		cursor1.execute(query1, (email, medical_records))
		cnx.commit()
	except Exception as e:
		print("Registration not successful, try again", e.args)

	return is_patient_added


def AuthenticateSignIn(email, password):
	"""
    AuthenticateSignIn: function to check if the credentials of a user are correct when signing in
    ----------------
    Parameters:
        takes email, password
    ----------------
    Returns String
    "wrong email" if the email is wrong
    "wrong password" if the password is wrong
    "correct credentials" if the credentials are correct
    """
	cursor = cnx.cursor()
	query = "SELECT email, pass FROM users"
	cursor.execute(query)
	result = cursor.fetchall()
	emails_list = [item[0] for item in result]
	passwords_list = [item[1] for item in result]

	email_found = "no"
	password_found = "no"
	record_index = -10
	for i in range(len(emails_list)):
		if email and email == emails_list[i]:
			email_found = "yes"
			record_index = i
			print("email found")
			break

	if email_found == "yes" and password and password == passwords_list[record_index]:
		password_found = "yes"
		print("password found")
		return "correct credentials"

	elif email_found == "no":
		return "wrong email"
	elif password_found == "no":
		return "wrong password"

try:
	# Create your views here.
	def home(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		return render(request, 'home.html', {'fn': fn})

	def go_to_signin(request):
		return render(request, 'signin.html')

	def go_to_signup(request):
		return render(request, 'signup.html')

	def go_to_doctors(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		doctors_info_array = get_doctors(request)
		n = len(doctors_info_array)
		return render(request, 'Doctors.html', {'fn': fn, 'doctors': doctors_info_array, 'n': range(n)})

	def go_to_news(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		return render(request, 'News.html', {'fn': fn})

	def go_to_appointments(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		names_list = dropdown_doctors(request)
		return render(request, 'Appointment.html', {'names_list': names_list ,'fn': fn})

	def go_to_update(request):
		return render(request, 'update.html')

	def go_to_newsdetails(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		return render(request, 'news-detail.html', {'fn': fn})

	def go_to_delete(request):
		return render(request, 'delete.html')

	def go_to_work(request):
		return render(request, 'work.html')

	def go_to_doctor_report(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		return render(request, 'report.html', {'fn': fn})

	def generate_report(request):
		emailtobeused = request.session.get('patient')
		fn = name(request, emailtobeused)
		id = request.POST['id']
		cursor = cnx.cursor()
		query = "select prescription,descriptions,additional_message from reports where app_id =%s"
		cursor.execute(query, (id,))
		results = cursor.fetchall()
		pres = [item[0] for item in results]
		desc = [item[1] for item in results]
		msg = [item[2] for item in results]
		query_doc = "Select email_doctor from appointments where id=%s"
		cursor.execute(query_doc, (id,))
		doctor_email = cursor.fetchall()
		doctor_email = doctor_email[0][0]
		doctor_name = fullname(request, doctor_email)
		return render(request, 'report_generated.html', {'fn': fn, 'id': id, 'prescription':pres[0],'descriptions':desc[0],'Additional_Message': msg[0], 'doctor_name':doctor_name})

	def go_to_feedback(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		id = request.POST['id1']
		return render(request, 'Feedback.html', {'fn': fn, 'id':id})

	def go_to_video_chat(request):
		if 'patient' in request.session:
			emailtobeused = request.session.get('patient')
			user_type = "Patient"
		elif 'doctor' in request.session:
			emailtobeused = request.session.get('doctor')
			user_type = "Doctor"
		else:
			emailtobeused = None
		fn = name(request, emailtobeused)
		id = request.POST['id1']
		print(id)
		return render(request, 'homevideo.html', {'fn': fn, 'user_type': user_type, 'id1': id})

	def go_to_report(request):
		emailtobeused = request.session.get('doctor')
		fn = name(request, emailtobeused)
		id = request.POST['id1']
		print(id)
		return render(request, 'report.html', {'fn': fn, 'id':id})

	def get_doctors(request):
		cursor = cnx.cursor()
		query = "select email,speciality,total_ratings,avg_rating from online_consultation.doctors where speciality <> 'Nurse' and speciality <> 'IT'"

		cursor.execute(query,)
		array_info = cursor.fetchall()
		result = [list(x) for x in array_info]
		#print(result)
		FINAL_array = []
		for array in result:
			doctor_email = array[0]
			current_doctor_name = fullname(request, doctor_email)
			array.insert(0, current_doctor_name)
			#array_string = "‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎| ‎‏‏‎ ‎".join(array)
			totalfixed = str(array[3])
			avgfixed = str(array[4])
			array[3] = totalfixed
			array[4] = avgfixed
			FINAL_array.append(array)

		print(FINAL_array)
		return FINAL_array

	def post_feedback(request):
		"""
    after submitting feedback

    Parameters
    ----------
    request : TYPE
        String

    Returns
    -------
    Render feedback page : "error while submitting feedback"
            			if some problem occured

    Render home page : "feedback has been successfully submitted"
						if no problem occured
    """
		problem = 0
		noproblem = 0
		if request.method == 'POST':
			q1 = request.POST['question1']
			q2 = request.POST['question2']
			q3 = request.POST['question3']
			q4 = request.POST['question4']
			q5 = request.POST['question5']
			app_id = request.POST['hidden_id']
			if 'patient' in request.session:
				emailtobeused = request.session.get('patient')
			elif 'doctor' in request.session:
				emailtobeused = request.session.get('doctor')

			fn = name(request, emailtobeused)
			cursor = cnx.cursor()
			current_avg = (int(q1) + int(q2) + int(q3) + int(q4) + int(q5)) / 5.0
			doctor_email_query = "Select email_doctor from appointments where id=%s"
			cursor.execute(doctor_email_query, (app_id,))
			doctor_email = cursor.fetchall()
			doctor_email = doctor_email[0][0]
			result = "Select total_ratings,avg_rating from doctors where email = %s"
			cursor.execute(result, (doctor_email,))
			ratings = cursor.fetchall()
			old_numb_of_ratings = int(ratings[0][0])
			#print(old_numb_of_ratings)
			old_avg_rating = float(ratings[0][1])
			#print(old_avg_rating)

			new_numb_of_ratings = int(old_numb_of_ratings) + 1
			new_avg_rating = (old_avg_rating*old_numb_of_ratings + current_avg) / new_numb_of_ratings
			print(new_avg_rating)
			print(new_numb_of_ratings)
			feedback_input = feedback_result(new_numb_of_ratings,new_avg_rating,doctor_email)
			fn = name(request, emailtobeused)

			if (feedback_input == "error while submitting feedback"):
				problem = 1
				return render(request, 'Feedback.html', {"result": feedback_input, 'flag': problem, 'fn':fn })

			else:
				noproblem = 1
				return render(request, 'home.html', {"result": feedback_input, 'flag':noproblem, 'fn':fn })

		else:
			return render(request, 'home.html')

	def feedback_result(numb_ratings,avg_ratings,doctor_email):
		"""
		feedback SQL query to Insert feedback results into the doctors table

		Parameters
		----------
		doctor_email : TYPE
				String
		number of ratings : TYPE
				Int
		Average Rating (over 5) : TYPE
				Int

		Returns
		-------
		"error while submitting feedback"
				if some problem occured

		"feedback has been successfully submitted"
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "update doctors set total_ratings = %s, avg_rating = %s WHERE email = %s"
			cursor.execute(query, (numb_ratings,avg_ratings,doctor_email,))
			cnx.commit()
			return "feedback has been successfully submitted"

		except Exception as e:
			return "error while submitting feedback"
			print("error", e.args)


	def report(request):
		"""
		Doctor gives report to the patient

		Parameters
		----------
		request : TYPE
			String

			Returns
			-------
			Render report.html : "error while submitting the report"
						if some problem occured

			Render home.html : "report has been successfully submitted"
						if no problem occured
		"""
		problem = 0
		noproblem = 0

		if request.method == 'POST':
			prescription = request.POST['Prescription']
			description = request.POST['Description']
			add_message = request.POST['Additional Message']
			attachments = request.POST['myfile']
			app_id = request.POST['hidden_id']

			emailtobeused = request.session.get('doctor')

			email_doctor = emailtobeused

			gen_report = report_result(app_id, prescription, description, add_message, attachments)

			fn = name(request, emailtobeused)

			if (gen_report == "error while submitting the report"):
				problem = 1
				return render(request, 'report.html', {"result": gen_report, 'flag': problem, 'fn': fn})

			else:
				noproblem = 1
				return render(request, 'home.html', {"result": gen_report, 'flag': noproblem, 'fn': fn})
		# return
		else:
			return render(request, 'home.html')


	def report_result(app_id, prescription, description, add_message, attachments):
		"""
		add report to SQL databse of reports

		Parameters
		----------
		app_id : TYPE
				Int
		perscription : TYPE
				String
		description : TYPE
				String
		add_message : TYPE
				String
		attachments : TYPE
				BLOB

		Returns
		-------
		"error while submitting the report"
					if some problem occured

		"report has been successfully submitted"
					if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "update reports set prescription=%s,descriptions=%s,additional_message=%s,attachments=%s where app_id = %s"
			cursor.execute(query, (prescription, description, add_message, attachments, app_id, ))
			cnx.commit()
			return "report has been successfully submitted"

		except Exception as e:
			return "error while submitting the report"
			print("error", e.args)

	def cancel_appointment_from_patient(request):
		"""
		cancel an appointment

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
			if some problem occured

		Render: My appointments page with updated table
					if no problem occured
		"""

		if request.method == 'POST':
			app_id = request.POST['id']

		try:
			cursor = cnx.cursor()
			query = "delete from online_consultation.appointments where id=%s"
			cursor.execute(query, (app_id,))
			cnx.commit()
			return go_to_user_appointments(request)

		except Exception as e:
			print("error", e.args)

	def dropdown_doctors(request):
		"""
		dropdown list of doctors from the database to display in "Make An Appointment" page

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
				if some problem occured

		final_result: list of doctor names
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "SELECT email FROM doctors"
			query1 = "SELECT first_name, last_name FROM users where email = %s"
			cursor.execute(query)
			result = cursor.fetchall()
			emails_list = [item[0] for item in result]
			print(emails_list)

			final_result = []
			for email in emails_list:
				doc_email = email
				cursor.execute(query1, (doc_email,))
				result2 = cursor.fetchall()
				fn = result2[0][0]
				ln = result2[0][1]
				name = fn + " " + ln
				final_result.append(name)

			return final_result

		except Exception as e:
			print("error", e.args)

	def go_to_user_appointments(request):
		"""
		display my appointments page from the patient's side

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
				if some problem occured

		Render: my appointments page with the list of user appointments with the designated doctors
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "SELECT email_doctor, appointment_date, appointment_time FROM appointments WHERE email_patient= %s order by appointment_date desc"
			emailtobeused = request.session.get('patient')
			cursor.execute(query, (emailtobeused,))
			result1 = cursor.fetchall()
			result = [list(x) for x in result1]
			#print (result1)
			#print (result)
			final_result = [ ", ".join(array) for array in result]
			#print(final_result)
			email_doctor = [item[0] for item in result]

			doctor_name = fullname(request, email_doctor[0])

			FINAL_array = []
			for array in result:
				doctor_email = array[0]
				current_doctor_name = fullname(request, doctor_email)
				array.insert(0,current_doctor_name)
				array_string = "‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎| ‎‏‏‎ ‎".join(array)
				FINAL_array.append(array_string)
			#print(FINAL_array)

			#app_date = [item[1] for item in result]
			#app_time = [item[2] for item in result]

			emailtobeused = request.session.get('patient')

			fn = name(request, emailtobeused)
			#print(email_doctor[0], app_date[0], app_time[0], doctor_name)
			#context =  {
					#'fn': fn,
					#'doctor_name': doctor_name,
					#'app_date': app_date[0],
					#'app_time': app_time[0],
				#}


			ids = getid(emailtobeused)

			mylist = zip(FINAL_array, ids)
			#print(mylist)
			#print(ids)
			query2 = "select app_id from online_consultation.reports where prescription is NULL"
			cursor.execute(query2,)
			result2 = cursor.fetchall()
			result2 = [list(x) for x in result2]
			result2 = [item[0] for item in result2 ]
			print(result2)


			return render(request, "userappointments.html", {'final_result' : FINAL_array, 'fn':fn, 'id':ids, 'mylist' : mylist, 'id_list': result2})
		except Exception as e:
			emailtobeused = request.session.get('patient')
			fn = name(request, emailtobeused)
			noapp = "No Appointments Set"
			return render(request, "userappointments.html", {'noapp' : noapp,'fn':fn})

	def getid(email):
		try:
			cursor = cnx.cursor()
			query = "select id from appointments where email_patient = %s order by appointment_date desc"

			cursor.execute(query, (email,))
			result = cursor.fetchall()

			final_array = []
			for i in range(len(result)):
				id = result[i][0]
				final_array.append(id)

			return final_array

		except Exception as e:
			return ("error", e.args)


	def getiddoc(email):
		try:
			cursor = cnx.cursor()
			query = "select id from appointments where email_doctor = %s order by appointment_date desc"
			cursor.execute(query, (email,))
			result = cursor.fetchall()

			final_array = []
			for i in range(len(result)):
				id = result[i][0]
				final_array.append(id)

			return final_array

		except Exception as e:
			return ("error", e.args)

	def go_to_doctor_appointments(request):
		"""
		display my appointments page from the doctor's side

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
				if some problem occured

		Render: my appointments page with the list of user appointments with the designated patients
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "SELECT email_patient, appointment_date, appointment_time FROM appointments WHERE email_doctor= %s order by appointment_date desc"
			emailtobeused = request.session.get('doctor')
			cursor.execute(query, (emailtobeused,))
			result1 = cursor.fetchall()
			result = [list(x) for x in result1]
			#print (result1)
			#print (result)
			final_result = [ ", ".join(array) for array in result]
			#print(final_result)
			email_patient = [item[0] for item in result]

			patient_name = fullname(request, email_patient[0])

			FINAL_array = []
			for array in result:
				patient_email = array[0]
				current_patient_name = fullname(request, patient_email)
				array.insert(0,current_patient_name)
				array_string = "‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎| ‎‏‏‎ ‎".join(array)
				FINAL_array.append(array_string)
			#print(FINAL_array)

			#app_date = [item[1] for item in result]
			#app_time = [item[2] for item in result]

			emailtobeused = request.session.get('doctor')

			fn = name(request, emailtobeused)
			#print(email_patient[0], app_date[0], app_time[0], patient_name)
			#context =  {
			#		'fn': fn,
			#		'patient_name': patient_name,
			#		'app_date': app_date[0],
			#		'app_time': app_time[0],
			#	}



			ids = getiddoc(emailtobeused)
			mylist = zip(FINAL_array, ids)

			query2 = "select app_id from online_consultation.reports where prescription is NULL"
			cursor.execute(query2,)
			result2 = cursor.fetchall()
			result2 = [list(x) for x in result2]
			result2 = [item[0] for item in result2 ]
			print(result2)

			return render(request, "userappointments.html", {'mylist' : mylist, 'fn':fn, 'id_list': result2})

		except Exception as e:
			emailtobeused = request.session.get('doctor')
			fn = name(request, emailtobeused)
			noapp = "No Appointments Set"
			return render(request, "userappointments.html", {'noapp' : noapp,'fn':fn})

	def work(request):
		"""
		Add staff members to the database with randomized passwords

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
				if some problem occured

		"Staff was not added to the database"
				if some problem occured

		"email already exists"
				if some problem occured

		"birthdate should not be empty"
				if some problem occured

		Render: home page, "Staff added to the database"
				if no problem occured
		"""
		if request.method == 'POST':
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			birth_date = request.POST['birth_date']
			gender = request.POST['gender']
			email = request.POST['email']
			password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
			Country = request.POST['Country']
			City = request.POST['City']
			speciality = request.POST['role']

			last_name = last_name.split()
			last_name = "-".join(last_name)

			work = work_result(first_name, last_name, birth_date, gender, email, password, Country, City, speciality)

			problem = 0

			noproblem = 0

			if ((work == "Staff was not added to the database") or (work == "email already exists") or (work == "birthdate should not be empty") ):
				problem = 1
				return render(request, 'work.html', {"result": work, 'flag': problem })

			else:
				noproblem = 1
				return render(request, 'home.html', {"result": work, 'flag':noproblem })
			#return
		else:
			return render(request, 'home.html')

	def go_to_info(request):
		"""
		Go to info page which displays all info about the user

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
				if some problem occured

		Render: info page with the information of the user
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "SELECT first_name AS First, last_name AS Last, dob AS DOB, location AS LOC FROM users WHERE email= %s"

			if 'patient' in request.session:
				NEW_email = request.session.get('patient')
			elif 'doctor' in request.session:
				NEW_email = request.session.get('doctor')
			#elif (request.session['doctor']):

			cursor.execute(query, (NEW_email,))
			result = cursor.fetchall()
			print (result)
			fn = [item[0] for item in result]
			ln = [item[1] for item in result]
			dob = [item[2] for item in result]
			loc = [item[3] for item in result]
			print(fn[0], ln[0], dob[0], loc[0])

			if (role(request, NEW_email) == "patient"):
				query2 = "select count(*) from appointments where email_patient = %s "
				cursor.execute(query2, (NEW_email,))
				result2 = cursor.fetchall()
				return render(request, "info.html", {
					'fn': fn[0],
					'ln': ln[0],
					'dob': dob[0],
					'loc': loc[0],
					'consultations': result2[0][0],
				})

			else:
				try:
					query1 = "SELECT speciality,total_ratings,avg_rating FROM doctors WHERE email = %s"
					cursor.execute(query1, (NEW_email,))
					result1 = cursor.fetchall()
					spec = [item[0] for item in result1]
					total_ratings =  [item[1] for item in result1]
					avg_rating = [item[2] for item in result1]
					return render(request, "info.html", {
						'fn': fn[0],
						'ln': ln[0],
						'dob': dob[0],
						'loc': loc[0],
						'speciality': spec[0],
						'numb_of_ratings': total_ratings[0],
						'average_rating': avg_rating[0],
						'speciality': spec[0]
					})
				except Exception as e:
					print("error", e.args)

		except Exception as e:
			print("error", e.args)


	def signup(request):
		"""
		Sign-Up adds patients to the database

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"error": exception
				if some problem occured

		"user was not added to the database"
				if some problem occured

		"email already exists"
				if some problem occured

		"birthdate should not be empty"
				if some problem occured

		"passwords do not match"
				if some problem occured

		Render: home page, "Registration Successful"
				if no problem occured
		"""
		if request.method == 'POST':
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			birth_date = request.POST['birth_date']
			gender = request.POST['gender']
			email = request.POST['email']
			password = request.POST['password']
			re_password = request.POST['re_password']
			Country = request.POST['Country']
			City = request.POST['City']
			medical_records = request.POST['myfile']

			regexmail = '^(([a-zA-Z0-9]{1,})|([_\-\.]{1}[a-zA-Z0-9]{1,}))+@(([a-zA-Z0-9\-])+\.)+[a-zA-Z]{2,}$'
			regexpass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
			if not re.search(regexmail, email):
				registration_result = "Email format is invalid."
				problem = 1
				return render(request, 'signup.html', {"result": registration_result, 'flag': problem})
			if not re.search(regexpass, password):
				registration_result = "Password should have at least one number, one uppercase and lowercase characters, one special symbol from (@$!%*#?&), and it should be between 6 and 20 characters long."
				problem = 1
				return render(request, 'signup.html', {"result": registration_result, 'flag': problem})

			registration_result = RegisterUser(first_name, last_name, birth_date, gender, email, password, re_password, Country, City, medical_records)

			problem = 0

			noproblem = 0

			if ((registration_result == "Registration not successful, try again") or (registration_result == "email already exists") or (registration_result == "passwords do not match") or (registration_result == "birthdate should not be empty") ):
				problem = 1
				return render(request, 'signup.html', {"result": registration_result, 'flag': problem })

			else:
				emailtobeused = email
				fn = name(request, emailtobeused)
				request.session['patient']=emailtobeused
				noproblem = 1
				return render(request, 'home.html', {"result": registration_result, 'flag':noproblem, 'fn':fn })
			#return
		else:
			return render(request, 'home.html')
		#return render(request, 'home.html', {'name': name})

	def work_result(first_name, last_name, birth_date, gender, email, password, country, city, speciality):
		"""
		Add staff members to the database

		Parameters
		----------
		first_name : TYPE
			String
		last_name : TYPE
			String
		birth_date : TYPE
			String
		gender : TYPE
			String
		email : TYPE
			String
		password : TYPE
			String
		country : TYPE
			String
		city : TYPE
			String
		speciality : TYPE
			String

		Returns
		-------
		"Staff not added, try again": exception
					if some problem occured

		"email already exists"
				if some problem occured

		"birthdate should not be empty"
				if some problem occured

		"passwords do not match"
				if some problem occured

		Render: home page, "Staff added to the database"
				if no problem occured
		"""
		cursor = cnx.cursor()
		cursor1 = cnx.cursor()
		birth_date = str(birth_date)
		# changing birthday to correct type: YYYY-MM-DD instead of MM-DD-YYYY

		#if len(birth_date) >= 10:
		#	str1 = str[6:10]
		#	str2 = str[0:5]
		#	print(str1)
		#	print(str2)
		#	birth_date = str1 + "-" + str2


		if birth_date == "":
			return "birthdate should not be empty"

		check_if_email_already_exists = CheckIfUserAlreadyExists(email)
		if check_if_email_already_exists == "yes":
			print("email already exists")
			return "email already exists"


		try:
			location = str(country) + " " + str(city)
		except Exception as e:
			print("there is something wrong with country or city", e.args)
		is_staff_added = "Staff was not added to the database"
		try:
			query = "INSERT INTO online_consultation.users (email, pass, first_name, last_name, dob, gender, location) VALUES (%s,%s,%s,%s,%s,%s,%s)"
			query1 = "INSERT INTO online_consultation.doctors (email, speciality, total_ratings, avg_rating) VALUES (%s,%s,%s,%s)"
			if location == " ":
				query = "INSERT INTO online_consultation.users (email, pass, first_name, last_name, dob, gender) VALUES (%s,%s,%s,%s,%s,%s)"
				cursor.execute(query, (email, password, first_name, last_name, birth_date, gender))
				cnx.commit()
				is_staff_added = "Staff added to the database"
				print("Staff added to the database")
			else:
				cursor.execute(query, (email, password, first_name, last_name, birth_date, gender, location))
				cnx.commit()
				is_staff_added = "Staff added to the database"
				print("Staff added to the database")
			cursor1.execute(query1, (email, speciality, 0, 0))
			cnx.commit()
		except Exception as e:
			print("Staff not added, try again", e.args)

		return is_staff_added

	def signin(request):
		"""
		Sign-In by cheching for email and password authentication in the database and creating a session

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		"your credentials are incorrect": exception, render signin page again
					if some problem occured

		Render: home page, "correct credentials" and create session
				if no problem occured
		"""
		noproblem = 0
		problem = 0
		if request.method == 'POST':
			email = request.POST["email"]
			password = request.POST["password"]
		signin_result = AuthenticateSignIn(email, password)
		print(signin_result)
		print(role(request, email))
		fn = name(request, email)

		if signin_result == "correct credentials" and role(request, email) == "patient":
			result = "you successfully signed in"
			noproblem = 1
			request.session['patient'] = email
			print (request.session['patient'])
			return render(request, 'home.html', {'name': signin_result, 'flag' : noproblem, 'result':result, 'fn': fn})

		elif signin_result == "correct credentials" and role(request, email) == "doctor":
			result = "you successfully signed in"
			noproblem = 1
			request.session['doctor']=email
			print (request.session['doctor'])
			return render(request, 'home.html', {'name': signin_result, 'flag' : noproblem, 'result':result, 'fn': fn})

		else:
			result = "your credentials are incorrect"
			problem = 1
			return render(request, 'signin.html', {'name': signin_result, 'flag': problem, 'result': result})

	def role(request, email):
		"""
		Check if the signed in user is a doctor/staff or a patient

		Parameters
		----------
		request : TYPE
			String
		email : TYPE
			String

		Returns
		-------
		exception
			if some problem occured

		email_found: "patient"
				if no problem occured

		email_found: "doctor"
				if no problem occured
		"""

		email_found = "no"
		try:
			cursor = cnx.cursor()
			query = "select email from online_consultation.users where email = %s"
			query1 = "select email from online_consultation.patients where email = %s"
			query2 = "select email from online_consultation.doctors where email = %s"
			cursor.execute(query, (email,))
			user = cursor.fetchall()
			cursor.execute(query1, (email,))
			patient = cursor.fetchall()
			cursor.execute(query2, (email,))
			doctor = cursor.fetchall()
			email_user = [item[0] for item in user]
			email_patient = [item[0] for item in patient]
			email_doctor = [item[0] for item in doctor]
			print(email_user, email_patient, email_doctor, email)
			if (email_patient == email_user):
				email_found = "patient"
				print("user is patient")
				return email_found
			elif (email_doctor == email_user):
				email_found = "doctor"
				print("user is doctor")
				return email_found
		except Exception as e:
			pass

	def name(request, email):
		"""
		Get the first name from the database using the email

		Parameters
		----------
		request : TYPE
			String
		email : TYPE
			String

		Returns
		-------
		None: exception
			if some problem occured

		fn[0]: first name as a string
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "select first_name from online_consultation.users where email = %s"
			cursor.execute(query, (email,))
			name = cursor.fetchall()
			fn = [item[0] for item in name]
			print (fn[0])
			return fn[0]
		except Exception as e:
			return None

	def fullname(request, email):
		"""
		Get the full name from the database using the email

		Parameters
		----------
		request : TYPE
			String
		email : TYPE
			String

		Returns
		-------
		None: exception
			if some problem occured

		full_name: full name as a string
				if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "select first_name, last_name from online_consultation.users where email = %s"
			cursor.execute(query, (email,))
			name = cursor.fetchall()
			fn = [item[0] for item in name]
			ln = [item[1] for item in name]
			full_name = fn[0] + " " + ln[0]
			return full_name
		except Exception as e:
			return None

	def doctorname(request, name):
		"""
    find the email given the name of a doctor

    Parameters
    ----------
    request : TYPE
        String
    name : TYPE
        String

    Returns
    -------
    "problem occured while retrieving the doctor email, check if the name exists in the database"
            if some problem occured

    the specified doctor email, given the name of the doctor otherwise
    """
		try:
			cursor = cnx.cursor(buffered=True)
			names = []
			names = name.split()
			first = names[0]
			last = names[1]
			query = "select email from online_consultation.users where first_name = %s AND last_name = %s"
			cursor.execute(query, (first, last,))
			cnx.commit()
			doctor = cursor.fetchall()
			email_doctor = [item[0] for item in doctor]
			return email_doctor[0]
		except Exception as e:
			print("problem occured while retrieving the doctor email, check if the name exists in the database", e.args)
			return "problem occured while retrieving the doctor email, check if the name exists in the database"

	def signout(request):
		"""
		Signs out the user and flushes the session

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		pass
			if some problem occured

		"successfully signed out"
			if no problem occured
		"""
		signout = 0
		result = ""
		try:
			if request.session.has_key('patient'):
				request.session.flush()
				result = "successfully signed out"
				signout = 1
			elif request.session.has_key('doctor'):
				request.session.flush()
				result = "successfully signed out"
				signout = 1
		except:
			pass
		return render(request, 'home.html', {'result': result, 'flag' : signout})

	def update(request):
		if request.method == 'POST':

			update_done = 0
			update_not_done = 0
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			if 'patient' in request.session:
				emailtobeused = request.session.get('patient')
			elif 'doctor' in request.session:
				emailtobeused = request.session.get('doctor')
			current_email = emailtobeused
			birth_date = request.POST['birth_date']
			old_password = request.POST['oldpassword']
			password = request.POST['password']
			new_password = request.POST['re_password']
			country = request.POST['Country']
			city = request.POST['City']

			if password != new_password:
				print("passwords do not match")
				result =  "passwords do not match"
				update_not_done = 1
				return render(request, "update.html", {'result': result, 'flag':update_not_done})

			if password != "":
				regexpass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
				if not re.search(regexpass, password):
					result = "Password should have at least one number, one uppercase and lowercase characters, one special symbol from (@$!%*#?&amp;), and it should be between 6 and 20 characters long."
					update_not_done = 1
					return render(request, "update.html", {'result': result, 'flag': update_not_done})


			result = UpdateUser(first_name, last_name, birth_date, current_email, old_password, new_password, country, city)

			if (result == "current credentials are not correct ") or (result == "patient info not updated, try again") :
				update_not_done = 1
				return render(request, "update.html", {'result': result, 'flag':update_not_done})
			else:
				update_done = 1
				return go_to_info(request)


		else:
			return render(request, 'update.html')

	def delete(request):
		if request.method == 'POST':

			del_done = 0
			del_not_done = 0
			current_password = request.POST['del_password']
			re_current_password = request.POST['re_del_password']

			if 'patient' in request.session:
				emailtobeused = request.session.get('patient')
			elif 'doctor' in request.session:
				emailtobeused = request.session.get('doctor')

			current_email = emailtobeused

			if current_password != re_current_password:
				print("passwords do not match")
				result =  "passwords do not match"
				del_not_done = 1
				return render(request, "delete.html", {'result': result, 'flag':del_not_done})

			result = DeleteUser(request, current_email, current_password)


			if (result == "user was not deleted from the database, try again") or (result == "current credentials are not correct"):
				del_not_done = 1
				return render(request, "delete.html", {'result': result, 'flag':del_not_done})
			else:
				try:
					if request.session.has_key('patient'):
						request.session.flush()
					else:
						request.session.flush()

				except:
					pass
				del_done = 1
				return render(request, "home.html", {'result': result, 'flag':del_done})


		else:
			return render(request, 'delete.html')

	def appointment(request):
		"""
		Book an appointment and insert the appointment info into the database and check if an appointment is taken

		Parameters
		----------
		request : TYPE
			String

		Returns
		-------
		appointment_result: "Appointment not set, please try again" and render appointments page
						if some problem occured

		isapptaken: "appointment already taken" and render appointments page
						if some problem occured

		isapptaken: "appointment available" and add appointment to database
						if no problem occured

		appointment_result: "Appointment has been set" and render homepage
						if no problem occured
		"""
		if request.method == 'POST':
			app_done = 0
			app_not_done = 0
			doctor = request.POST["select_doctor"]
			appointment_date = request.POST["date"]
			appointment_time = request.POST["select_time"]
			Additional_Message = request.POST["message"]
			appointment_report = None


			emailtobeused = request.session.get('patient')

			email_patient = emailtobeused
			email_doctor = doctorname(request, doctor)
			print(email_doctor)
			fn = name(request, emailtobeused)

		isapptaken = CheckIfAppointmentTaken(request, doctor, appointment_date, appointment_time)
		print(isapptaken)
		names_list = dropdown_doctors(request)
		fn = name(request, emailtobeused)

		if isapptaken == "appointment available":
			appointment_result = AppointmentDB(request, email_doctor, email_patient, appointment_date, appointment_time, Additional_Message, appointment_report)

		else:
			appointment_result = "appointment already taken"
			app_not_done = 1
			return render(request, 'Appointment.html', {'result' : appointment_result, 'flag' : app_not_done, 'names_list': names_list, 'fn': fn})

		if (appointment_result == "Appointment has been set"):
			app_done = 1
			return render(request, 'home.html', {'result':appointment_result, 'flag':app_done, 'names_list': names_list, 'fn': fn})
		else:
			app_not_done = 1
			return render(request, 'Appointment.html', {'result' : appointment_result, 'flag' : app_not_done, 'names_list': names_list, 'fn': fn})

	def AppointmentDB(request, email_doctor, email_patient, appointment_date, appointment_time, Additional_Message, appointment_report):
		"""
		Insert appointment info into the database

		Parameters
		----------
		request : TYPE
			String
		email_doctor : TYPE
			String
		email_patient : TYPE
			String
		appointment_date : TYPE
			String
		appointment_time : TYPE
			String
		Additional_Message : TYPE
			String
		appointment_report : TYPE
			String

		Returns
		-------
		appointment_result: "Appointment not set, please try again"
						if some problem occured

		appointment_result: "Appointment has been set"
						if no problem occured
		"""
		try:
			cursor = cnx.cursor()
			query = "INSERT INTO online_consultation.appointments (email_doctor, email_patient, appointment_date, appointment_time, Additional_Message, appointment_report) VALUES (%s,%s,%s,%s,%s,%s)"
			cursor.execute(query, (email_doctor, email_patient, appointment_date, appointment_time, Additional_Message, appointment_report))
			cnx.commit()

			query1 = "SELECT id from appointments where email_doctor=%s AND email_patient=%s AND appointment_date = %s AND appointment_time=%s AND Additional_Message = %s"
			cursor.execute(query1, (email_doctor, email_patient, appointment_date, appointment_time, Additional_Message))
			result = cursor.fetchall()
			id = result[0][0]
			query2 = "INSERT INTO online_consultation.reports (app_id) VALUES (%s)"
			cursor.execute(query2, (id,))
			cnx.commit()


			appointment_result = "Appointment has been set"
			print("Appointment has been set")
		except Exception as e:
			print("Appointment not set, please try again", e.args)
			appointment_result = "Appointment not set, please try again"

		return appointment_result


	def CheckIfAppointmentTaken(request, dr_name, adate, atime):
		"""
		check if an appointment is taken

		Parameters
		----------
		dr_name : TYPE
			String
		adate : TYPE
			String
		atime : TYPE
			String

		Returns
		-------
		"appointment already taken" if the appointment with the doctor at the requested date and time is taken
		"appointment available" if the appointment with the doctor at the requested date and time is not taken
		"""

		cursor = cnx.cursor()

		"""
		#search for dr. with name given
		name = dr_name.split()
		try:
			first_name = name[0]
			last_name = name[1]
		except Exception as e:
			print("something wrong with the dr. name", e.args)
			"""
		dr_email = doctorname(request, dr_name)
		query = "SELECT email_doctor, appointment_date, appointment_time FROM online_consultation.appointments where email_doctor = %s;"
		try:
			appointment_taken = 0
			cursor.execute(query, (dr_email,))
			result = cursor.fetchall()
			doctor_email = [item[0] for item in result]
			print(doctor_email)
			adates = [item[1] for item in result]
			atimes = [item[2] for item in result]
			for i in range(len(doctor_email)):
				if(adates[i] == adate and atimes[i] == atime):
					appointment_taken = 1
					break
			if appointment_taken == 1:
				return "appointment already taken"
			else:
				return "appointment available"
		except Exception as e:
			print(e.args)


	def UpdateUser(first_name, last_name, birth_date, current_email, old_password, new_password, country, city):
		"""
		UpdateUser: function to update the information about a user
		----------------
		Parameters:
				takes first_name, last_name, birth_date, current_email, old_password, new_password, country, city
		----------------
		Returns String
		"user info updated" if the user info are updated
		"current credentials are not correct " if the current username and/or password are not correct
		"patient info not updated, try again" if a problem occured while updating patient info

		"""
		cursor = cnx.cursor()
		is_patient_updated = ""
	    #first_name_status
		fn = 0
	    #last_name_status
		ln = 0
	    #birth_date_status
		bd = 0
	    #new_password_status
		np = 0
	    #country_status
		co = 0
	    #city_status
		ci = 0
		location = ""
		if first_name != "" and first_name != None:
			fn = 1
		if last_name != "" and last_name != None:
			ln = 1
		if birth_date != "" and birth_date != None:
			bd = 1
			birth_date = str(birth_date)
		if new_password != "" and new_password != None:
			np = 1
		if country != "" and country != None:
			co = 1
			location = location + str(country)
		if city != "" and city != None:
			ci = 1
			location = location + " " + str(city)


		check_authenticate_user = AuthenticateSignIn(current_email, old_password)

		if check_authenticate_user != "correct credentials":
			print("current credentials are not correct ")
			return("current credentials are not correct ")
		else:
			print("current credentials are correct")

		try:
			query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, dob=%s, pass=%s, location=%s WHERE email=%s"
			if fn == 0 and ln ==0 and bd == 0 and np == 0 and location == "":
				print("nothing changed")

			elif fn == 1 and ln ==1 and bd == 1 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, dob=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, birth_date, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==1 and bd == 1 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, dob=%s, location=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, birth_date, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==1 and bd == 0 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 1 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s, dob=%s, pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (first_name, birth_date, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 1 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET last_name=%s, dob=%s, pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (last_name, birth_date, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 1 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET last_name=%s, dob=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (last_name, birth_date, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 1 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, dob=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (first_name, birth_date, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==1 and bd == 0 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==1 and bd == 1 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, dob=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, birth_date, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==1 and bd == 0 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s, location=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 1 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET last_name=%s, dob=%s, location=%s WHERE email=%s"
				cursor.execute(query, (last_name, birth_date, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 1 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET dob=%s, pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (birth_date, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 1 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s, dob=%s, location=%s WHERE email=%s"
				cursor.execute(query, (first_name, birth_date, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 0 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s, pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (first_name, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 0 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET last_name=%s, pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (last_name, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 0 and np == 1 and location != "":
				query = "UPDATE online_consultation.users SET pass=%s, location=%s WHERE email=%s"
				cursor.execute(query, (new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 1 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET dob=%s, location=%s WHERE email=%s"
				cursor.execute(query, (birth_date, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 1 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET dob=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (birth_date, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 0 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET last_name=%s, location=%s WHERE email=%s"
				cursor.execute(query, (last_name, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 0 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET last_name=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (last_name, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 1 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET last_name=%s, dob=%s WHERE email=%s"
				cursor.execute(query, (last_name, birth_date, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 0 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET first_name=%s location=%s WHERE email=%s"
				cursor.execute(query, (first_name, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 0 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, pass=%s WHERE email=%s"
				cursor.execute(query, (first_name, new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 1 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, dob=%s WHERE email=%s"
				cursor.execute(query, (first_name, birth_date, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==1 and bd == 0 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s, last_name=%s WHERE email=%s"
				cursor.execute(query, (first_name, last_name, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 1 and ln ==0 and bd == 0 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET first_name=%s WHERE email=%s"
				cursor.execute(query, (first_name, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==1 and bd == 0 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET last_name=%s WHERE email=%s"
				cursor.execute(query, (last_name, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 1 and np == 0 and location == "":
				query = "UPDATE online_consultation.users SET dob=%s WHERE email=%s"
				cursor.execute(query, (birth_date, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 0 and np == 1 and location == "":
				query = "UPDATE online_consultation.users SET pass=%s WHERE email=%s"
				cursor.execute(query, (new_password, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			elif fn == 0 and ln ==0 and bd == 0 and np == 0 and location != "":
				query = "UPDATE online_consultation.users SET location=%s WHERE email=%s"
				cursor.execute(query, (location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
			else:
				cursor.execute(query, (first_name, last_name, birth_date, new_password, location, current_email))
				cnx.commit()
				is_patient_updated = "patient info updated"
				print("patient info updated")
		except Exception as e:
			print("patient info not updated, try again", e.args)
			is_patient_updated = "patient info not updated, try again"
		return is_patient_updated


	def DeleteUser(request, current_email, current_password):
		"""
		DeleteUser: function to delete a user from the database
		----------------
		Parameters:
		takes email, password
		----------------
		Returns String
		"user deleted" if the user is deleted from database
		"user was not deleted from the database, try again" if the user is not deleted from the database
		"current credentials are not correct" if the current username and/or password are not correct
		"""

		cursor = cnx.cursor()
		check_authenticate_user = AuthenticateSignIn(current_email, current_password)

		if check_authenticate_user != "correct credentials":
			print("current credentials are not correct")
			return("current credentials are not correct")
		else:
			print("current credentials are correct")

		is_patient_deleted = ""

		try:
			query = "delete from online_consultation.users where email = %s"
			query1 = "delete from online_consultation.patients where email = %s"
			query2 = "delete from online_consultation.appointments where email_patient = %s"
			cursor.execute(query2, (current_email,))
			cnx.commit()
			cursor.execute(query1, (current_email,))
			cnx.commit()
			cursor.execute(query, (current_email,))
			cnx.commit()
			is_patient_deleted = "user deleted"
			print("user deleted")
			return is_patient_deleted
		except Exception as e:
			print("user was not deleted from the database, try again", e.args)
			is_patient_deleted = "user was not deleted from the database, try again"
			return is_patient_deleted

	def DeleteDoctor(request, current_email, current_password):
		"""
		DeleteUser: function to delete a user from the database
		----------------
		Parameters:
		takes email, password
		----------------
		Returns String
		"user deleted" if the user is deleted from database
		"user was not deleted from the database, try again" if the user is not deleted from the database
		"current credentials are not correct" if the current username and/or password are not correct
		"""

		cursor = cnx.cursor()
		check_authenticate_user = AuthenticateSignIn(current_email, current_password)

		if check_authenticate_user != "correct credentials":
			print("current credentials are not correct")
			return("current credentials are not correct")
		else:
			print("current credentials are correct")

		is_patient_deleted = ""

		try:
			query = "delete from online_consultation.users where email = %s"
			query1 = "delete from online_consultation.doctors where email = %s"
			query2 = "delete from online_consultation.appointments where email_doctor = %s"
			cursor.execute(query2, (current_email,))
			cnx.commit()
			cursor.execute(query1, (current_email,))
			cnx.commit()
			cursor.execute(query, (current_email,))
			cnx.commit()
			is_patient_deleted = "user deleted"
			print("user deleted")
			return is_patient_deleted
		except Exception as e:
			print("user was not deleted from the database, try again", e.args)
			is_patient_deleted = "user was not deleted from the database, try again"
			return is_patient_deleted


except Exception as e:
	print("problem occured", e.args)
