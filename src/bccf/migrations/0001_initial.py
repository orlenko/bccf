# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HomeMarquee'
        db.create_table(u'bccf_homemarquee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bccf', ['HomeMarquee'])

        # Adding model 'FooterMarquee'
        db.create_table(u'bccf_footermarquee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bccf', ['FooterMarquee'])

        # Adding model 'PageMarquee'
        db.create_table(u'bccf_pagemarquee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['PageMarquee'])

        # Adding model 'HomeMarqueeSlide'
        db.create_table(u'bccf_homemarqueeslide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
            ('linkLabel', self.gf('django.db.models.fields.CharField')(default='', max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['HomeMarqueeSlide'])

        # Adding M2M table for field marquee on 'HomeMarqueeSlide'
        m2m_table_name = db.shorten_name(u'bccf_homemarqueeslide_marquee')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homemarqueeslide', models.ForeignKey(orm[u'bccf.homemarqueeslide'], null=False)),
            ('homemarquee', models.ForeignKey(orm[u'bccf.homemarquee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['homemarqueeslide_id', 'homemarquee_id'])

        # Adding model 'FooterMarqueeSlide'
        db.create_table(u'bccf_footermarqueeslide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['FooterMarqueeSlide'])

        # Adding M2M table for field marquee on 'FooterMarqueeSlide'
        m2m_table_name = db.shorten_name(u'bccf_footermarqueeslide_marquee')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('footermarqueeslide', models.ForeignKey(orm[u'bccf.footermarqueeslide'], null=False)),
            ('footermarquee', models.ForeignKey(orm[u'bccf.footermarquee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['footermarqueeslide_id', 'footermarquee_id'])

        # Adding model 'PageMarqueeSlide'
        db.create_table(u'bccf_pagemarqueeslide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, null=True, blank=True)),
            ('linkLabel', self.gf('django.db.models.fields.CharField')(default='', max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['PageMarqueeSlide'])

        # Adding M2M table for field marquee on 'PageMarqueeSlide'
        m2m_table_name = db.shorten_name(u'bccf_pagemarqueeslide_marquee')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pagemarqueeslide', models.ForeignKey(orm[u'bccf.pagemarqueeslide'], null=False)),
            ('pagemarquee', models.ForeignKey(orm[u'bccf.pagemarquee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pagemarqueeslide_id', 'pagemarquee_id'])

        # Adding model 'BCCFPage'
        db.create_table(u'bccf_bccfpage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('marquee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.PageMarquee'], null=True, blank=True)),
            ('carousel_color', self.gf('django.db.models.fields.CharField')(default='dgreen-list', max_length=11)),
        ))
        db.send_create_signal(u'bccf', ['BCCFPage'])

        # Adding model 'BCCFTopic'
        db.create_table(u'bccf_bccftopic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('marquee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.PageMarquee'], null=True, blank=True)),
            ('carousel_color', self.gf('django.db.models.fields.CharField')(default='dgreen-list', max_length=11)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'bccf', ['BCCFTopic'])

        # Adding model 'BCCFChildPage'
        db.create_table(u'bccf_bccfchildpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comments_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('rating_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_sum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_average', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('_order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.BCCFChildPage'], null=True, blank=True)),
            ('gparent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.BCCFPage'], null=True, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('titles', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
            ('content_model', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('login_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('in_menus', self.gf('mezzanine.pages.fields.MenusField')(default=(1, 2, 3), max_length=100, null=True, blank=True)),
            ('page_for', self.gf('django.db.models.fields.CharField')(default='parent', max_length=13, null=True, blank=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', to=orm['generic.AssignedKeyword'], frozen_by_south=True)),
            ('rating', self.gf('mezzanine.generic.fields.RatingField')(object_id_field='object_pk', to=orm['generic.Rating'], frozen_by_south=True)),
            ('comments', self.gf('mezzanine.generic.fields.CommentsField')(object_id_field='object_pk', to=orm['generic.ThreadedComment'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'bccf', ['BCCFChildPage'])

        # Adding M2M table for field bccf_topic on 'BCCFChildPage'
        m2m_table_name = db.shorten_name(u'bccf_bccfchildpage_bccf_topic')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bccfchildpage', models.ForeignKey(orm[u'bccf.bccfchildpage'], null=False)),
            ('bccftopic', models.ForeignKey(orm[u'bccf.bccftopic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bccfchildpage_id', 'bccftopic_id'])

        # Adding model 'BCCFGenericPage'
        db.create_table(u'bccf_bccfgenericpage', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['BCCFGenericPage'])

        # Adding model 'BCCFBabyPage'
        db.create_table(u'bccf_bccfbabypage', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['BCCFBabyPage'])

        # Adding model 'Article'
        db.create_table(u'bccf_article', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['Article'])

        # Adding model 'DownloadableForm'
        db.create_table(u'bccf_downloadableform', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['DownloadableForm'])

        # Adding model 'Magazine'
        db.create_table(u'bccf_magazine', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['Magazine'])

        # Adding model 'TipSheet'
        db.create_table(u'bccf_tipsheet', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['TipSheet'])

        # Adding model 'Video'
        db.create_table(u'bccf_video', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('video_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024, null=True, blank=True)),
            ('link_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024, null=True, blank=True)),
            ('video_file', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['Video'])

        # Adding model 'Program'
        db.create_table(u'bccf_program', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Program'])

        # Adding model 'Blog'
        db.create_table(u'bccf_blog', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Blog'])

        # Adding model 'Campaign'
        db.create_table(u'bccf_campaign', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Campaign'])

        # Adding model 'UserProfile'
        db.create_table(u'bccf_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('photo', self.gf('bccf.fields.MyImageField')(max_length=255, null=True, blank=True)),
            ('membership_order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Order'], null=True, blank=True)),
            ('requested_cancellation', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('is_forum_moderator', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('membership_type', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('membership_level', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['UserProfile'])

        # Adding model 'EventForParents'
        db.create_table(u'bccf_eventforparents', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('price', self.gf('cartridge.shop.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('location_city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location_street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location_street2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location_postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['EventForParents'])

        # Adding model 'EventForProfessionals'
        db.create_table(u'bccf_eventforprofessionals', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('price', self.gf('cartridge.shop.fields.MoneyField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('location_city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location_street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location_street2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location_postal_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('survey_before', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='survey_before', null=True, to=orm['builder.FormPublished'])),
            ('survey_after', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='survey_after', null=True, to=orm['builder.FormPublished'])),
        ))
        db.send_create_signal(u'bccf', ['EventForProfessionals'])

        # Adding model 'Settings'
        db.create_table(u'bccf_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'bccf', ['Settings'])


    def backwards(self, orm):
        # Deleting model 'HomeMarquee'
        db.delete_table(u'bccf_homemarquee')

        # Deleting model 'FooterMarquee'
        db.delete_table(u'bccf_footermarquee')

        # Deleting model 'PageMarquee'
        db.delete_table(u'bccf_pagemarquee')

        # Deleting model 'HomeMarqueeSlide'
        db.delete_table(u'bccf_homemarqueeslide')

        # Removing M2M table for field marquee on 'HomeMarqueeSlide'
        db.delete_table(db.shorten_name(u'bccf_homemarqueeslide_marquee'))

        # Deleting model 'FooterMarqueeSlide'
        db.delete_table(u'bccf_footermarqueeslide')

        # Removing M2M table for field marquee on 'FooterMarqueeSlide'
        db.delete_table(db.shorten_name(u'bccf_footermarqueeslide_marquee'))

        # Deleting model 'PageMarqueeSlide'
        db.delete_table(u'bccf_pagemarqueeslide')

        # Removing M2M table for field marquee on 'PageMarqueeSlide'
        db.delete_table(db.shorten_name(u'bccf_pagemarqueeslide_marquee'))

        # Deleting model 'BCCFPage'
        db.delete_table(u'bccf_bccfpage')

        # Deleting model 'BCCFTopic'
        db.delete_table(u'bccf_bccftopic')

        # Deleting model 'BCCFChildPage'
        db.delete_table(u'bccf_bccfchildpage')

        # Removing M2M table for field bccf_topic on 'BCCFChildPage'
        db.delete_table(db.shorten_name(u'bccf_bccfchildpage_bccf_topic'))

        # Deleting model 'BCCFGenericPage'
        db.delete_table(u'bccf_bccfgenericpage')

        # Deleting model 'BCCFBabyPage'
        db.delete_table(u'bccf_bccfbabypage')

        # Deleting model 'Article'
        db.delete_table(u'bccf_article')

        # Deleting model 'DownloadableForm'
        db.delete_table(u'bccf_downloadableform')

        # Deleting model 'Magazine'
        db.delete_table(u'bccf_magazine')

        # Deleting model 'TipSheet'
        db.delete_table(u'bccf_tipsheet')

        # Deleting model 'Video'
        db.delete_table(u'bccf_video')

        # Deleting model 'Program'
        db.delete_table(u'bccf_program')

        # Deleting model 'Blog'
        db.delete_table(u'bccf_blog')

        # Deleting model 'Campaign'
        db.delete_table(u'bccf_campaign')

        # Deleting model 'UserProfile'
        db.delete_table(u'bccf_userprofile')

        # Deleting model 'EventForParents'
        db.delete_table(u'bccf_eventforparents')

        # Deleting model 'EventForProfessionals'
        db.delete_table(u'bccf_eventforprofessionals')

        # Deleting model 'Settings'
        db.delete_table(u'bccf_settings')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bccf.article': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Article'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.bccfbabypage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'BCCFBabyPage', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.bccfchildpage': {
            'Meta': {'ordering': "('titles',)", 'object_name': 'BCCFChildPage'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bccf_topic': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['bccf.BCCFTopic']", 'null': 'True', 'blank': 'True'}),
            'comments': ('mezzanine.generic.fields.CommentsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.ThreadedComment']", 'frozen_by_south': 'True'}),
            'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gparent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.BCCFPage']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page_for': ('django.db.models.fields.CharField', [], {'default': "'parent'", 'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.BCCFChildPage']", 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.Rating']", 'frozen_by_south': 'True'}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bccf.bccfgenericpage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'BCCFGenericPage', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.bccfpage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'BCCFPage', '_ormbases': [u'pages.Page']},
            'carousel_color': ('django.db.models.fields.CharField', [], {'default': "'dgreen-list'", 'max_length': '11'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'marquee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.PageMarquee']", 'null': 'True', 'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.bccftopic': {
            'Meta': {'object_name': 'BCCFTopic'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'carousel_color': ('django.db.models.fields.CharField', [], {'default': "'dgreen-list'", 'max_length': '11'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'marquee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.PageMarquee']", 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bccf.blog': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Blog', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.campaign': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Campaign', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.downloadableform': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'DownloadableForm'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.eventforparents': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'EventForParents'},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.eventforprofessionals': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'EventForProfessionals'},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'survey_after': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_after'", 'null': 'True', 'to': u"orm['builder.FormPublished']"}),
            'survey_before': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_before'", 'null': 'True', 'to': u"orm['builder.FormPublished']"})
        },
        u'bccf.footermarquee': {
            'Meta': {'object_name': 'FooterMarquee'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bccf.footermarqueeslide': {
            'Meta': {'object_name': 'FooterMarqueeSlide'},
            'caption': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'marquee': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bccf.FooterMarquee']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'bccf.homemarquee': {
            'Meta': {'object_name': 'HomeMarquee'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bccf.homemarqueeslide': {
            'Meta': {'object_name': 'HomeMarqueeSlide'},
            'caption': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'linkLabel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'marquee': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bccf.HomeMarquee']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'bccf.magazine': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Magazine'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.pagemarquee': {
            'Meta': {'object_name': 'PageMarquee'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bccf.pagemarqueeslide': {
            'Meta': {'object_name': 'PageMarqueeSlide'},
            'caption': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'linkLabel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'marquee': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bccf.PageMarquee']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'bccf.program': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Program', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bccf.tipsheet': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'TipSheet'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_forum_moderator': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'membership_level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'membership_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Order']", 'null': 'True', 'blank': 'True'}),
            'membership_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'photo': ('bccf.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'requested_cancellation': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'bccf.video': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Video', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'video_file': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'builder.formpublished': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'FormPublished', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'form_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['builder.FormStructure']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'builder.formstructure': {
            'Meta': {'object_name': 'FormStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Form Structure'", 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'JSON'", 'max_length': '4'})
        },
        u'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'generic.assignedkeyword': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'AssignedKeyword'},
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['generic.Keyword']"}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {})
        },
        u'generic.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'generic.rating': {
            'Meta': {'object_name': 'Rating'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.IntegerField', [], {}),
            'rating_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratings'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        u'generic.threadedcomment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'ThreadedComment', '_ormbases': [u'comments.Comment']},
            'by_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['comments.Comment']", 'unique': 'True', 'primary_key': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.Rating']", 'frozen_by_south': 'True'}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'replied_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'null': 'True', 'to': u"orm['generic.ThreadedComment']"})
        },
        u'pages.page': {
            'Meta': {'ordering': "('titles',)", 'object_name': 'Page'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content_model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_menus': ('mezzanine.pages.fields.MenusField', [], {'default': '(1, 2, 3)', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'shop.order': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Order'},
            'additional_instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'billing_detail_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_detail_country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_detail_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'billing_detail_first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_detail_last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_detail_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'billing_detail_postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'billing_detail_state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'billing_detail_street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'discount_code': ('cartridge.shop.fields.DiscountCodeField', [], {'max_length': '20', 'blank': 'True'}),
            'discount_total': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_total': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'shipping_detail_city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_detail_country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_detail_first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_detail_last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_detail_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shipping_detail_postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'shipping_detail_state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_detail_street': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipping_total': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'shipping_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tax_total': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'tax_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'total': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bccf']