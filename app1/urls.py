from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [

	path('home',views.home,name='home'),

	path('go_to_signin', views.go_to_signin, name='go_to_signin'),
	path('signin',views.signin,name='signin'),
	path('go_to_signup', views.go_to_signup, name='go_to_signup'),
	path('signup',views.signup,name='signup'),
	path('go_to_doctors',views.go_to_doctors,name='go_to_doctors'),
	path('go_to_news',views.go_to_news,name='go_to_news'),
	path('go_to_appointments',views.go_to_appointments,name='go_to_appointments'),
	path('go_to_update',views.go_to_update,name='go_to_update'),
	path('go_to_newsdetails',views.go_to_newsdetails,name='go_to_newsdetails'),
	path('appointment',views.appointment,name='appointment'),
	path('update',views.update,name='update'),
	path('delete',views.delete,name='delete'),
	path('go_to_delete',views.go_to_delete,name='go_to_delete'),
	path('go_to_info',views.go_to_info,name='go_to_info'),
	path('signout',views.signout,name='signout'),
	path('go_to_user_appointments', views.go_to_user_appointments, name='go_to_user_appointments'),
	path('go_to_work',views.go_to_work,name='go_to_work'),
	path('work',views.work,name='work'),
	path('go_to_doctor_appointments', views.go_to_doctor_appointments, name='go_to_doctor_appointments'),
	path('go_to_doctor_report', views.go_to_doctor_report, name='go_to_doctor_report'),
	path('report', views.report, name='report'),
	path('go_to_feedback', views.go_to_feedback, name='go_to_feedback'),
	path('post_feedback', views.post_feedback, name='post_feedback'),
	path('cancel_appointment_from_patient', views.cancel_appointment_from_patient, name='cancel_appointment_from_patient'),
	path('go_to_report', views.go_to_report, name='go_to_report'),
	path('generate_report', views.generate_report, name='generate_report'),
	path('go_to_video_chat', views.go_to_video_chat, name='go_to_video_chat'),

]
