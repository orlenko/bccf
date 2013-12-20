# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TopicLink'
        db.delete_table(u'bccf_topiclink')

        # Deleting model 'Video'
        db.delete_table(u'bccf_video')

        # Deleting model 'TipSheet'
        db.delete_table(u'bccf_tipsheet')

        # Deleting model 'DownloadableForm'
        db.delete_table(u'bccf_downloadableform')

        # Deleting model 'Article'
        db.delete_table(u'bccf_article')

        # Deleting model 'FeaturableResource'
        db.delete_table(u'bccf_featurableresource')

        # Deleting model 'Program'
        db.delete_table(u'bccf_program')

        # Deleting model 'Topic'
        db.delete_table(u'bccf_topic')

        # Deleting model 'ProgramChild'
        db.delete_table(u'bccf_programchild')

        # Deleting model 'Magazine'
        db.delete_table(u'bccf_magazine')

        # Adding model 'BCCFChildPage'
        db.create_table(u'bccf_bccfchildpage', (
            (u'bccfpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFPage'], unique=True, primary_key=True)),
            ('rating_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_sum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating_average', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('page_for', self.gf('django.db.models.fields.CharField')(default='Parents', max_length=13, null=True, blank=True)),
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('rating', self.gf('mezzanine.generic.fields.RatingField')(object_id_field='object_pk', to=orm['generic.Rating'], frozen_by_south=True)),
        ))
        db.send_create_signal(u'bccf', ['BCCFChildPage'])

        # Adding M2M table for field topic on 'BCCFChildPage'
        m2m_table_name = db.shorten_name(u'bccf_bccfchildpage_topic')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bccfchildpage', models.ForeignKey(orm[u'bccf.bccfchildpage'], null=False)),
            ('topics', models.ForeignKey(orm[u'bccf.topics'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bccfchildpage_id', 'topics_id'])

        # Adding model 'DocumentResource'
        db.create_table(u'bccf_documentresource', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('resource_type', self.gf('django.db.models.fields.CharField')(default='article', max_length=11)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['DocumentResource'])

        # Adding model 'BCCFParentPage'
        db.create_table(u'bccf_bccfparentpage', (
            (u'bccfpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFPage'], unique=True, primary_key=True)),
            ('marquee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.PageMarquee'], null=True, blank=True)),
            ('carousel_color', self.gf('django.db.models.fields.CharField')(default='dgreen-list', max_length=11)),
        ))
        db.send_create_signal(u'bccf', ['BCCFParentPage'])

        # Adding model 'Blog'
        db.create_table(u'bccf_blog', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Blog'])

        # Adding model 'Programs'
        db.create_table(u'bccf_programs', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Programs'])

        # Adding model 'VideoResource'
        db.create_table(u'bccf_videoresource', (
            (u'bccfchildpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFChildPage'], unique=True, primary_key=True)),
            ('video_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024, null=True, blank=True)),
            ('link_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024, null=True, blank=True)),
            ('video_file', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['VideoResource'])

        # Adding model 'Topics'
        db.create_table(u'bccf_topics', (
            (u'bccfparentpage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bccf.BCCFParentPage'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Topics'])

        # Deleting field 'BCCFPage.carouselColor'
        db.delete_column(u'bccf_bccfpage', 'carouselColor')

        # Deleting field 'BCCFPage.page_ptr'
        db.delete_column(u'bccf_bccfpage', u'page_ptr_id')

        # Deleting field 'BCCFPage.marquee'
        db.delete_column(u'bccf_bccfpage', 'marquee_id')

        # Adding field 'BCCFPage.id'
        db.add_column(u'bccf_bccfpage', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Adding field 'BCCFPage.keywords_string'
        db.add_column(u'bccf_bccfpage', 'keywords_string',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.site'
        db.add_column(u'bccf_bccfpage', 'site',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site']),
                      keep_default=False)

        # Adding field 'BCCFPage.title'
        db.add_column(u'bccf_bccfpage', 'title',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=500),
                      keep_default=False)

        # Adding field 'BCCFPage.slug'
        db.add_column(u'bccf_bccfpage', 'slug',
                      self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage._meta_title'
        db.add_column(u'bccf_bccfpage', '_meta_title',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.description'
        db.add_column(u'bccf_bccfpage', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.gen_description'
        db.add_column(u'bccf_bccfpage', 'gen_description',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'BCCFPage.created'
        db.add_column(u'bccf_bccfpage', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'BCCFPage.updated'
        db.add_column(u'bccf_bccfpage', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'BCCFPage.status'
        db.add_column(u'bccf_bccfpage', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'BCCFPage.publish_date'
        db.add_column(u'bccf_bccfpage', 'publish_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.expiry_date'
        db.add_column(u'bccf_bccfpage', 'expiry_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.short_url'
        db.add_column(u'bccf_bccfpage', 'short_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.in_sitemap'
        db.add_column(u'bccf_bccfpage', 'in_sitemap',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'BCCFPage._order'
        db.add_column(u'bccf_bccfpage', '_order',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'BCCFPage.parent'
        db.add_column(u'bccf_bccfpage', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['bccf.BCCFPage']),
                      keep_default=False)

        # Adding field 'BCCFPage.in_menus'
        db.add_column(u'bccf_bccfpage', 'in_menus',
                      self.gf('mezzanine.pages.fields.MenusField')(default=(1, 2, 3), max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'BCCFPage.titles'
        db.add_column(u'bccf_bccfpage', 'titles',
                      self.gf('django.db.models.fields.CharField')(max_length=1000, null=True),
                      keep_default=False)

        # Adding field 'BCCFPage.content_model'
        db.add_column(u'bccf_bccfpage', 'content_model',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'BCCFPage.login_required'
        db.add_column(u'bccf_bccfpage', 'login_required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'TopicLink'
        db.create_table(u'bccf_topiclink', (
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.Topic'])),
            ('entity_id', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'bccf', ['TopicLink'])

        # Adding model 'Video'
        db.create_table(u'bccf_video', (
            ('video_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024, null=True, blank=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', frozen_by_south=True, to=orm['generic.AssignedKeyword'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='videos', to=orm['auth.User'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('link_url', self.gf('django.db.models.fields.URLField')(default='', max_length=1024, null=True, blank=True)),
            ('video_file', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bccf', ['Video'])

        # Adding model 'TipSheet'
        db.create_table(u'bccf_tipsheet', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', frozen_by_south=True, to=orm['generic.AssignedKeyword'])),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tipsheets', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'bccf', ['TipSheet'])

        # Adding model 'DownloadableForm'
        db.create_table(u'bccf_downloadableform', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', frozen_by_south=True, to=orm['generic.AssignedKeyword'])),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downloadableforms', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'bccf', ['DownloadableForm'])

        # Adding model 'Article'
        db.create_table(u'bccf_article', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', frozen_by_south=True, to=orm['generic.AssignedKeyword'])),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'bccf', ['Article'])

        # Adding model 'FeaturableResource'
        db.create_table(u'bccf_featurableresource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['FeaturableResource'])

        # Adding model 'Program'
        db.create_table(u'bccf_program', (
            ('image', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Parents', max_length=13, null=True, blank=True)),
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Program'])

        # Adding model 'Topic'
        db.create_table(u'bccf_topic', (
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            ('star_survey_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('carouselColor', self.gf('django.db.models.fields.CharField')(default='dgreen-list', max_length=11)),
            ('featured_image', self.gf('bccf.fields.MyImageField')(max_length=255, null=True, blank=True)),
            ('marquee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.PageMarquee'], null=True, blank=True)),
            ('star_forum_post_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('star_blog_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['Topic'])

        # Adding model 'ProgramChild'
        db.create_table(u'bccf_programchild', (
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['pages.Page'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'bccf', ['ProgramChild'])

        # Adding model 'Magazine'
        db.create_table(u'bccf_magazine', (
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('attached_document', self.gf('mezzanine.core.fields.FileField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('short_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('in_sitemap', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords_string', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('_meta_title', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('publish_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('gen_description', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('keywords', self.gf('mezzanine.generic.fields.KeywordsField')(object_id_field='object_pk', frozen_by_south=True, to=orm['generic.AssignedKeyword'])),
            ('content', self.gf('mezzanine.core.fields.RichTextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='magazines', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'bccf', ['Magazine'])

        # Deleting model 'BCCFChildPage'
        db.delete_table(u'bccf_bccfchildpage')

        # Removing M2M table for field topic on 'BCCFChildPage'
        db.delete_table(db.shorten_name(u'bccf_bccfchildpage_topic'))

        # Deleting model 'DocumentResource'
        db.delete_table(u'bccf_documentresource')

        # Deleting model 'BCCFParentPage'
        db.delete_table(u'bccf_bccfparentpage')

        # Deleting model 'Blog'
        db.delete_table(u'bccf_blog')

        # Deleting model 'Programs'
        db.delete_table(u'bccf_programs')

        # Deleting model 'VideoResource'
        db.delete_table(u'bccf_videoresource')

        # Deleting model 'Topics'
        db.delete_table(u'bccf_topics')

        # Adding field 'BCCFPage.carouselColor'
        db.add_column(u'bccf_bccfpage', 'carouselColor',
                      self.gf('django.db.models.fields.CharField')(default='dgreen-list', max_length=11),
                      keep_default=False)

        # Adding field 'BCCFPage.page_ptr'
        db.add_column(u'bccf_bccfpage', u'page_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['pages.Page'], unique=True, primary_key=True),
                      keep_default=False)

        # Adding field 'BCCFPage.marquee'
        db.add_column(u'bccf_bccfpage', 'marquee',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bccf.PageMarquee'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'BCCFPage.id'
        db.delete_column(u'bccf_bccfpage', u'id')

        # Deleting field 'BCCFPage.keywords_string'
        db.delete_column(u'bccf_bccfpage', 'keywords_string')

        # Deleting field 'BCCFPage.site'
        db.delete_column(u'bccf_bccfpage', 'site_id')

        # Deleting field 'BCCFPage.title'
        db.delete_column(u'bccf_bccfpage', 'title')

        # Deleting field 'BCCFPage.slug'
        db.delete_column(u'bccf_bccfpage', 'slug')

        # Deleting field 'BCCFPage._meta_title'
        db.delete_column(u'bccf_bccfpage', '_meta_title')

        # Deleting field 'BCCFPage.description'
        db.delete_column(u'bccf_bccfpage', 'description')

        # Deleting field 'BCCFPage.gen_description'
        db.delete_column(u'bccf_bccfpage', 'gen_description')

        # Deleting field 'BCCFPage.created'
        db.delete_column(u'bccf_bccfpage', 'created')

        # Deleting field 'BCCFPage.updated'
        db.delete_column(u'bccf_bccfpage', 'updated')

        # Deleting field 'BCCFPage.status'
        db.delete_column(u'bccf_bccfpage', 'status')

        # Deleting field 'BCCFPage.publish_date'
        db.delete_column(u'bccf_bccfpage', 'publish_date')

        # Deleting field 'BCCFPage.expiry_date'
        db.delete_column(u'bccf_bccfpage', 'expiry_date')

        # Deleting field 'BCCFPage.short_url'
        db.delete_column(u'bccf_bccfpage', 'short_url')

        # Deleting field 'BCCFPage.in_sitemap'
        db.delete_column(u'bccf_bccfpage', 'in_sitemap')

        # Deleting field 'BCCFPage._order'
        db.delete_column(u'bccf_bccfpage', '_order')

        # Deleting field 'BCCFPage.parent'
        db.delete_column(u'bccf_bccfpage', 'parent_id')

        # Deleting field 'BCCFPage.in_menus'
        db.delete_column(u'bccf_bccfpage', 'in_menus')

        # Deleting field 'BCCFPage.titles'
        db.delete_column(u'bccf_bccfpage', 'titles')

        # Deleting field 'BCCFPage.content_model'
        db.delete_column(u'bccf_bccfpage', 'content_model')

        # Deleting field 'BCCFPage.login_required'
        db.delete_column(u'bccf_bccfpage', 'login_required')


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
        u'bccf.bccfchildpage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'BCCFChildPage', '_ormbases': [u'bccf.BCCFPage']},
            u'bccfpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFPage']", 'unique': 'True', 'primary_key': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'image': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'page_for': ('django.db.models.fields.CharField', [], {'default': "'Parents'", 'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'rating': ('mezzanine.generic.fields.RatingField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.Rating']", 'frozen_by_south': 'True'}),
            'rating_average': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'rating_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating_sum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'topic': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['bccf.Topics']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.bccfpage': {
            'Meta': {'ordering': "('titles',)", 'object_name': 'BCCFPage'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            '_order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['bccf.BCCFPage']"}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'titles': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bccf.bccfparentpage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'BCCFParentPage', '_ormbases': [u'bccf.BCCFPage']},
            u'bccfpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFPage']", 'unique': 'True', 'primary_key': 'True'}),
            'carousel_color': ('django.db.models.fields.CharField', [], {'default': "'dgreen-list'", 'max_length': '11'}),
            'marquee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bccf.PageMarquee']", 'null': 'True', 'blank': 'True'})
        },
        u'bccf.blog': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Blog', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.documentresource': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'DocumentResource', '_ormbases': [u'bccf.BCCFChildPage']},
            'attached_document': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'resource_type': ('django.db.models.fields.CharField', [], {'default': "'article'", 'max_length': '11'})
        },
        u'bccf.eventforparents': {
            'Meta': {'object_name': 'EventForParents'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'location_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'bccf.eventforprofessionals': {
            'Meta': {'object_name': 'EventForProfessionals'},
            '_meta_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'content': ('mezzanine.core.fields.RichTextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gen_description': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'keywords': ('mezzanine.generic.fields.KeywordsField', [], {'object_id_field': "'object_pk'", 'to': u"orm['generic.AssignedKeyword']", 'frozen_by_south': 'True'}),
            'keywords_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'location_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location_street2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('cartridge.shop.fields.MoneyField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'short_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'survey_after': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_after'", 'null': 'True', 'to': u"orm['builder.FormPublished']"}),
            'survey_before': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'survey_before'", 'null': 'True', 'to': u"orm['builder.FormPublished']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
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
        u'bccf.programs': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Programs', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'bccf.topics': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Topics', '_ormbases': [u'bccf.BCCFParentPage']},
            u'bccfparentpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFParentPage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'bccf.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_forum_moderator': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'membership_order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Order']", 'null': 'True', 'blank': 'True'}),
            'photo': ('bccf.fields.MyImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'bccf.videoresource': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'VideoResource', '_ormbases': [u'bccf.BCCFChildPage']},
            u'bccfchildpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bccf.BCCFChildPage']", 'unique': 'True', 'primary_key': 'True'}),
            'link_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'video_file': ('mezzanine.core.fields.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'builder.formpublished': {
            'Meta': {'object_name': 'FormPublished'},
            'form_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['builder.FormStructure']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'builder.formstructure': {
            'Meta': {'object_name': 'FormStructure'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
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