from django.conf.urls import patterns, url


urlpatterns = patterns("",
    url(r'^directory/', 'bccf.views.page.user_list', name='member-directory'),
    url(r'^profile/(?P<id>\d+)/$', 'bccf.views.member.profile', name='member-profile'),
    url(r'^upgrade/(?P<variation_id>.*)/$', 'bccf.views.member.membership_upgrade', name='member-membership-upgrade'),
    url(r'^renew/$', 'bccf.views.member.membership_renew', name='member-membership-renew'),
    url(r'^select/$', 'bccf.views.member.membership_select', name='member-membership-select'),
    url(r'^cancel/$', 'bccf.views.member.membership_cancel', name='member-membership-cancel'),
    url('^addmember/$', 'bccf.views.member.addmember', name='member-addmember'),
    url('^addexistingmember/$', 'bccf.views.member.addexistingmember', name='member-addexisting'),
    url('^delmember/$', 'bccf.views.member.delmember', name='member-delete'),
    url('^program/request', 'bccf.views.member.reqprogram', name='member-request-program'),
    url(r'^(?P<slug>.*)/$', 'bccf.views.member.membership', name='member-membership'),
)