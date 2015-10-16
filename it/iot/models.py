from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
import datetime

class Visitors(models.Model):

    POSSIBLE_ACTIONS = (
 			 ('REGISTRATION', 'REGISTRATION'),                       ('LOGIN_TRY', 'LOGIN_TRY'),
                         ('REGISTRATION_OR_UPDATE', 'REGISTRATION_OR_UPDATE'),   ('LOGGED_IN', 'LOGGED_IN'),
			 ('DELETE_ON_IOS', 'DELETE_ON_IOS'), 	 		 ('LOG_OUT', 'LOG_OUT'),
			 ('AUDIO_MESSAGE', 'AUDIO_MESSAGE'),			 ('REGISTRATION_FAILED', 'REGISTRATION_FAILED'),
			 ('OTP', 'OTP'),					 ('REGISTRATION_SUCCESS', 'REGISTRATION_SUCCESS'),
			 ('HRMS_ACCESS', 'HRMS_ACCESS'),			 ('EDIT_TEAM_NAME', 'EDIT_TEAM_NAME'),
			 ('MAILERS', 'MAILERS'),				 ('ADD_TEAM_MEMBER', 'ADD_TEAM_MEMBER'),
			 ('GROUPS', 'GROUPS'),					 ('DELETE_TEAM_MEMBER', 'DELETE_TEAM_MEMBER'),
			 ('GROUP_MEMBERS', 'GROUP_MEMBERS'),			 ('SEND_PN_TO_ALL', 'SEND_PN_TO_ALL'),
			 ('FRIENDS', 'FRIENDS'),				 ('SEND_PN_TO_TEAMS', 'SEND_PN_TO_TEAMS'),
			 ('SENT_NOTIFICATION', 'SENT_NOTIFICATION'),
			 ('SENT_MESSAGE', 'SENT_MESSAGE'),
			 ('ACK_NOTIFICATION', 'ACK_NOTIFICATION'),
			 ('ACK_MESSAGE', 'ACK_MESSAGE'),
			 ('PN_STATUS_CHANGE', 'PN_STATUS_CHANGE'),
		       )

    def now():
        return datetime.datetime.now()

    #Session details
    session_key = models.CharField('session key', max_length=40, blank = True, null=True)
    url_visited  = models.CharField("Last URL Visited", blank = True, null=True, max_length=300)
    visit_time = models.DateTimeField('Time of Action', default=datetime.datetime.now)
    visitor_ip = models.CharField("IP Address", blank = True, null=True, max_length=30)

    email = models.CharField(('e-mail address of logged in user'),blank = True, null=True, max_length=75)
    referral  = models.CharField("Referred By", blank = True, null=True, max_length=300)
    source  = models.CharField("Source ", blank = True, null=True, max_length=50)
    ## Action to be used while sending out communication from our side
    action = models.CharField('Action Performed', choices = POSSIBLE_ACTIONS,
         max_length = 30, blank=True, null=True)


def log_visit(request=None, action = 'NotProvided', email = None, source = 'iot'):
    visitor_log = Visitors()
    try:
        if request != None:
            visitor_log.url_visited = request.META['PATH_INFO'][:299]
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                try:
                    visitor_log.visitor_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
                except Exception,e:
                    print "Error while fetching the IP", str(e)
                    pass
            else:
                visitor_log.visitor_ip = request.META['REMOTE_ADDR']

            if action in ['NotProvided',]:
                action = 'Surfing'

            try:
                visitor_log.email = request.user.email
            except:
                pass
            try:
                visitor_log.referral = request.META['HTTP_REFERER'][:299]
            except:
                visitor_log.referral = 'direct'

        visitor_log.action = action

        if email:
            visitor_log.email = email
        if source:
            visitor_log.source = source


        visitor_log.save()

    except Exception, e:
        print "In Models", str(e)
        pass


