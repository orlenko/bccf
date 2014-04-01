from django_cron import CronJobBase, Schedule

from django.db.models import Q
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

from bccf.models import Event, EventRegistration

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
            regs = EventRegistration.objects.filter(~Q(reminder=True), event=event.pk, paid=False)
            for reg in regs:
                send_reminder(email_title, reg.user, 'bccf', 'Event', event.pk)
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
            regs = EventRegistration.objects.filter(event=event.pk)
            for reg in regs:
                if not reg.paid: # Remove
                    print reg.user.get_full_name()
                    counter += 1
                    # Send email about revoked seat
                else: # Send Reminder
                    print reg.user.get_full_name()
                    # Send email reminder about event
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
        events = Event.objects.filter(date_start__lte=now())
        for event in events:
            event.status = 1
            if event.provider:
                # Send email to provider
                pass
            if event.survey_before:
                event.survey_before.closed = True
                event.survey_before.save()
            if event.survey_after:
                event.survey_after.closed = True
                event.survey_after.save()
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
                limit = expiry - relativedelta(week=1)
            if limit and now() <= limit:
                # Send email
                pass

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
                # Send email
                user.profile.membership_order = None
                user.profile.membership_level = 'A'
                user.profile.save()