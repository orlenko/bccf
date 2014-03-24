# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.event_product'
        db.add_column(u'bccf_event', 'event_product',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='event-product', null=True, to=orm['shop.Product']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.event_product'
        db.delete_column(u'bccf_event', 'event_product_id')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bccf.article': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Article'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.bccfbabypage': {
            'Meta': {'ordering': "('order',)", 'object_name': 'BCCFBabyPage', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bccf.bccfchildpage': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'BCCFChildPage'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'bccf_topic': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['bccf.BCCFTopic']", 'null': 'True', 'blank': 'True'}),
            u'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'page_for': ('django.db.models.fields.CharField', [], {'default': "'parent'", 'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.BCCFChildPage']", 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bccf.bccfgenericpage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'BCCFGenericPage', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'show_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_rating': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_resources': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'bccf.bccfpage': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'BCCFPage', '_ormbases': [u'pages.Page']},
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
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
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
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Blog', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.campaign': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Campaign'},
            'approve': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'approved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'by_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'campaigns'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'bccf.downloadableform': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'DownloadableForm'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.event': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Event', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_product': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'event-product'", 'null': 'True', 'to': u"orm['shop.Product']"}),
            'full': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'max_seats': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'program'", 'null': 'True', 'to': u"orm['bccf.Program']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'survey_after': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_after'", 'null': 'True', 'to': u"orm['builder.FormPublished']"}),
            'survey_before': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_before'", 'null': 'True', 'to': u"orm['builder.FormPublished']"})
        },
        u'bccf.eventregistration': {
            'Meta': {'object_name': 'EventRegistration'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_registration'", 'to': u"orm['bccf.Event']"}),
            'event_order': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'event-order'", 'blank': 'True', 'to': u"orm['shop.Order']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Magazine'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'})
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
        u'bccf.podcast': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Podcast', '_ormbases': [u'bccf.BCCFChildPage']},
            'attached_audio': ('mezzanine.core.fields.FileField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.program': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Program', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'user_added': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.programrequest': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'ProgramRequest'},
            'accept': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'accepted_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('mezzanine.core.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'program_requests'", 'to': u"orm['auth.User']"})
        },
        u'bccf.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bccf.tipsheet': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'TipSheet'},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'accreditation': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['bccf.Program']", 'null': 'True', 'blank': 'True'}),
            'autosubscribe': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'avatar': ('bccf.fields.MyImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'male'", 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_mailing_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_forum_moderator': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '10', 'blank': 'True'}),
            'linkedin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'membership_level': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'membership_order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'order'", 'null': 'True', 'to': u"orm['shop.Order']"}),
            'membership_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'members'", 'null': 'True', 'to': u"orm['bccf.UserProfile']"}),
            'phone_mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone_primary': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone_work': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'photo': ('bccf.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pinterest': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'requested_cancellation': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'show_in_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_signatures': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'max_length': '1024', 'blank': 'True'}),
            'signature_html': ('django.db.models.fields.TextField', [], {'max_length': '1054', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'street_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time_zone': ('django.db.models.fields.FloatField', [], {'default': '3.0'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'voting_order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'voting'", 'null': 'True', 'to': u"orm['shop.Order']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'youtube': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'bccf.video': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Video', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Product']", 'null': 'True', 'blank': 'True'}),
            'video_url': ('embed_video.fields.EmbedVideoField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'builder.formpublished': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'FormPublished'},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'form_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['builder.FormStructure']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'builder.formstructure': {
            'Meta': {'object_name': 'FormStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Form Structure'", 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'JSON'", 'max_length': '4'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pages.page': {
            'Meta': {'ordering': "(u'titles',)", 'object_name': 'Page'},
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
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'shop.category': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'Category', '_ormbases': [u'pages.Page']},
            'carousel_color': ('django.db.models.fields.CharField', [], {'default': "'dgreen-list'", 'max_length': '11'}),
            'combined': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'featured_image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'marquee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.PageMarquee']", 'null': 'True', 'blank': 'True'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'product_options'", 'blank': 'True', 'to': u"orm['shop.ProductOption']"}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['pages.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'price_max': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'price_min': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shop.Product']", 'symmetrical': 'False', 'blank': 'True'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Sale']", 'null': 'True', 'blank': 'True'})
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
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'paypal'", 'max_length': '6'}),
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
        u'shop.product': {
            'Meta': {'object_name': 'Product'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shop.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            u'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'num_in_stock': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'related_products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_products_rel_+'", 'blank': 'True', 'to': u"orm['shop.Product']"}),
            'sale_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sale_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'sale_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'sku': ('cartridge.shop.fields.SKUField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'unit_price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'upsell_products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'upsell_products_rel_+'", 'blank': 'True', 'to': u"orm['shop.Product']"})
        },
        u'shop.productoption': {
            'Meta': {'object_name': 'ProductOption'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('cartridge.shop.fields.OptionField', [], {'max_length': '50', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'shop.sale': {
            'Meta': {'object_name': 'Sale'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'sale_related'", 'blank': 'True', 'to': u"orm['shop.Category']"}),
            'discount_deduct': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'discount_exact': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'discount_percent': ('cartridge.shop.fields.PercentageField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['shop.Product']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bccf']