# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormEntry'
        db.create_table(u'bccf_form_builder_formentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['bccf_form_builder.Form'])),
        ))
        db.send_create_signal(u'bccf_form_builder', ['FormEntry'])

        # Adding model 'FieldEntry'
        db.create_table(u'bccf_form_builder_fieldentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_id', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['bccf_form_builder.FormEntry'])),
        ))
        db.send_create_signal(u'bccf_form_builder', ['FieldEntry'])

        # Adding model 'Form'
        db.create_table(u'bccf_form_builder_form', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('intro', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('button_text', self.gf('django.db.models.fields.CharField')(default=u'Submit', max_length=50)),
            ('response', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('login_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('send_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_from', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('email_copies', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email_subject', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email_message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'bccf_form_builder', ['Form'])

        # Adding M2M table for field sites on 'Form'
        m2m_table_name = db.shorten_name(u'bccf_form_builder_form_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('form', models.ForeignKey(orm[u'bccf_form_builder.form'], null=False)),
            ('site', models.ForeignKey(orm[u'sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['form_id', 'site_id'])

        # Adding model 'Field'
        db.create_table(u'bccf_form_builder_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=100, blank=True)),
            ('field_type', self.gf('django.db.models.fields.IntegerField')()),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('choices', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('placeholder_text', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('group_id', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fields', to=orm['bccf_form_builder.Form'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf_form_builder', ['Field'])


    def backwards(self, orm):
        # Deleting model 'FormEntry'
        db.delete_table(u'bccf_form_builder_formentry')

        # Deleting model 'FieldEntry'
        db.delete_table(u'bccf_form_builder_fieldentry')

        # Deleting model 'Form'
        db.delete_table(u'bccf_form_builder_form')

        # Removing M2M table for field sites on 'Form'
        db.delete_table(db.shorten_name(u'bccf_form_builder_form_sites'))

        # Deleting model 'Field'
        db.delete_table(u'bccf_form_builder_field')


    models = {
        u'bccf_form_builder.field': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Field'},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['bccf_form_builder.Form']"}),
            'group_id': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'placeholder_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'bccf_form_builder.fieldentry': {
            'Meta': {'object_name': 'FieldEntry'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['bccf_form_builder.FormEntry']"}),
            'field_id': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True'})
        },
        u'bccf_form_builder.form': {
            'Meta': {'object_name': 'Form'},
            'button_text': ('django.db.models.fields.CharField', [], {'default': "u'Submit'", 'max_length': '50'}),
            'email_copies': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email_from': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'default': '[1]', 'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bccf_form_builder.formentry': {
            'Meta': {'object_name': 'FormEntry'},
            'entry_time': ('django.db.models.fields.DateTimeField', [], {}),
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['bccf_form_builder.Form']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bccf_form_builder']