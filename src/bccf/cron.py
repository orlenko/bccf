from django_cron import CronJobBase, Schedule

from django.db.models import Q
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

from bccf.models import Event, EventRegistration
from bccf.util import emailutil as email

class EventPaymentReminder(CronJobBase):
    """
    CronJob for sending a payment reminder to users who have not paid their
    registrations. The is reminder will be sent 4 weeks before the event.
    """
    RUN_EVERY_MINS = 0.01
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bccf.event_payment_reminder'

    email_title = 'Event Registration Payment Reminder'    
    
    def do(self):
        events = Event.objects.need_reminder().all()
        for event in events:
            regs = EventRegistration.objects.filter(~Q(reminder=True), ~Q(paid=True), event=event.pk)
            for reg in regs:
                context = {
                    'event': event,
                    'reg': reg                
                }
                email.send_reminder(self.email_title, reg.user, context)
                reg.reminder = True
                reg.save()
        
class EventFreeRemind(CronJobBase):
    """
    Removes registered users from the event because he/she has not paid the
    registration fee. This also sends reminders to registered users about the
    event. The this only looks at events that are happening in 2 weeks
    """
    RUN_EVERY_MINS = 0.01
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bccf.event_free_seat'
    
    def do(self):
        events = Event.objects.need_freeing().all()
        for event in events:
            counter = 0
            regs = EventRegistration.objects.filter(event=event)
            for reg in regs:
                if not reg.paid: # Remove
                    counter += 1
                    email.send_reminder('Event seat reservation released', reg.user, context={'event': event})
                else: # Send Reminder
                    email.send_reminder('Event reminder', reg.user, context={'event': event})
            if counter > 0: # Set event to not full if there are people who has not paid
                event.full = False
                event.save()
                
class EventClose(CronJobBase):
    """
    Closes an event that passed
    """
    RUN_EVERY_MINS = 0.01
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bccf.event_close'
    
    def do(self):
        events = Event.objects.filter(date_start__lte=now(), closed=False)
        for event in events:
            event.status = 1
            event.closed = True
            regs = EventRegistration.objects.filter(event=event)
            if event.provider:
                if event.provider.email:
                    email.send_reminder('Event finished', event.provider, context={'event': event}) # To Provider
            for reg in regs:
                email.send_reminder('Event finished', reg.user, context={'event': event}) # To Attendees
            if event.survey_before:
                event.survey_before.closed = True
                event.survey_before.save()
            event.save()
    
class UserMembershipReminder(CronJobBase):
    """
    Sends reminders to users about their expiring memberships.
    """
    RUN_EVERY_MINS = 0.01
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bccf.user_membership_reminder'
    
    def do(self):
        users = User.objects.filter(~Q(profile__membership_order=None))
        for user in users:
            expiry = user.profile.membership_expiration_datetime
            type = user.profile.membership_payment_type
            if type == 'Annual': # 3 months before
                limit = expiry - relativedelta(months=3)
            elif type == 'Quarterly': # 1 month before
                limit = expiry - relativedelta(months=1)
            elif type == 'Monthly': # 1 week before
                limit = expiry - relativedelta(weeks=1)
            if limit and now() <= limit:
                email.send_reminder('Membership Expiring', user)

class UserMembershipExpire(CronJobBase):
    """
    Sets user's membership to a free version after current
    membership expires
    """
    RUN_EVERY_MINS = 0.01
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bccf.user_membership_expire'
    
    def do(self):
        users = User.objects.filter(~Q(profile__membership_order=None))
        for user in users:
            expiry =user.profile.membership_expiration_datetime
            if now() <= expiry:
                email.send_reminder('Membership Expired', user)
                email.send_moderate('Membership Expired', context={'user': user})
                user.profile.membership_order = None
                user.profile.membership_level = 'A'
                user.profile.save()