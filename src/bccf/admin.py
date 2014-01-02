from copy import deepcopy

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import NoReverseMatch

from mezzanine.core.admin import DisplayableAdmin, DisplayableAdminForm
from mezzanine.utils.urls import admin_url
from mezzanine.conf import settings
from mezzanine.pages.admin import PageAdmin

from bccf.models import (BCCFTopic, Settings, EventForProfessionals,
    EventForParents, HomeMarquee, FooterMarquee, HomeMarqueeSlide, FooterMarqueeSlide,
    PageMarquee, PageMarqueeSlide, BCCFPage, BCCFChildPage, BCCFBabyPage, 
    Blog, Program, Article, Magazine, Video, TipSheet, DownloadableForm, Campaign)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    list_editable = ['value']

class ParentsEventAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(ParentsEventAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'provider',
                                    'date_start',
                                    'date_end',
                                    'location_city',
                                    'location_street',
                                    'location_street2',
                                    'location_postal_code',
                                    'price',
                                    'bccf_topic',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['provider', 'date_start', 'date_end', 'price']:
                self.list_display.insert(-1, fieldname)
                
class ProfessionalsEventAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(ProfessionalsEventAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'provider',
                                    'date_start',
                                    'date_end',
                                    'location_city',
                                    'location_street',
                                    'location_street2',
                                    'location_postal_code',
                                    'price',
                                    'image',
                                    'survey_before',
                                    'bccf_topic',
                                    'survey_after']):
                self.fieldsets[0][1]['fields'].insert(3, field)
        if self.list_display == DisplayableAdmin.list_display:
            self.list_display = list(deepcopy(self.list_display))
            for fieldname in ['provider', 'date_start', 'date_end', 'price']:
                self.list_display.insert(-1, fieldname)

admin.site.register(Settings, SettingsAdmin)
admin.site.register(EventForParents, ParentsEventAdmin)
admin.site.register(EventForProfessionals, ProfessionalsEventAdmin)

#Pages
page_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
page_fieldsets[0][1]["fields"] += ("gparent", "page_for", "bccf_topic", "featured", "content",)

class BCCFPageAdminForm(DisplayableAdminForm):

    def clean_slug(self):
        """
        Save the old slug to be used later in PageAdmin.model_save()
        to make the slug change propagate down the page tree.
        """
        self.instance._old_slug = self.instance.slug
        return self.cleaned_data['slug']

class BCCFPageAdmin(DisplayableAdmin):
    """
    Admin class for the ``Page`` model and all subclasses of
    ``Page``. Handles redirections between admin interfaces for the
    ``Page`` model and its subclasses.
    """

    form = BCCFPageAdminForm
    fieldsets = page_fieldsets
    change_list_template = "admin/page/bccf_page_list.html"

    def __init__(self, *args, **kwargs):
        """
        For ``Page`` subclasses that are registered with an Admin class
        that doesn't implement fieldsets, add any extra model fields
        to this instance's fieldsets. This mimics Django's behaviour of
        adding all model fields when no fieldsets are defined on the
        Admin class.
        """
        super(BCCFPageAdmin, self).__init__(*args, **kwargs)
        # Test that the fieldsets don't differ from BCCFPageAdmin's.
        if self.model is not BCCFPage and self.fieldsets == BCCFPageAdmin.fieldsets:
            # Make a copy so that we aren't modifying other Admin
            # classes' fieldsets.
            self.fieldsets = deepcopy(self.fieldsets)
            # Insert each field between the publishing fields and nav
            # fields. Do so in reverse order to retain the order of
            # the model's fields.
            exclude_fields = BCCFChildPage._meta.get_all_field_names() + ['bccfchildpage_ptr']
            try:
                exclude_fields.extend(self.exclude)
            except (AttributeError, TypeError):
                pass
            try:
                exclude_fields.extend(self.form.Meta.exclude)
            except (AttributeError, TypeError):
                pass
            fields = self.model._meta.fields + self.model._meta.many_to_many
            for field in reversed(fields):
                if field.name not in exclude_fields and field.editable:
                    self.fieldsets[0][1]["fields"].insert(3, field.name)

    def in_menu(self):
        """
        Hide subclasses from the admin menu.
        """
        return self.model is BCCFChildPage

    def _check_permission(self, request, page, permission):
        """
        Runs the custom permission check and raises an
        exception if False.
        """
        if not getattr(page, "can_" + permission)(request):
            raise PermissionDenied

    def add_view(self, request, **kwargs):
        """
        For the ``Page`` model, redirect to the add view for the
        first page model, based on the ``ADD_PAGE_ORDER`` setting.
        """
        if self.model is BCCFChildPage:
            return HttpResponseRedirect(self.get_content_models()[0].add_url)
        return super(BCCFPageAdmin, self).add_view(request, **kwargs)

    def change_view(self, request, object_id, **kwargs):
        """
        For the ``Page`` model, check ``page.get_content_model()``
        for a subclass and redirect to its admin change view.
        Also enforce custom change permissions for the page instance.
        """
        page = get_object_or_404(BCCFChildPage, pk=object_id)
        content_model = page.get_content_model()
        self._check_permission(request, content_model, "change")
        if self.model is BCCFChildPage:
            if content_model is not None:
                change_url = admin_url(content_model.__class__, "change",
                                       content_model.id)
                return HttpResponseRedirect(change_url)
        kwargs.setdefault("extra_context", {})
        kwargs["extra_context"].update({
            "hide_delete_link": not content_model.can_delete(request),
            "hide_slug_field": content_model.overridden(),
        })
        return super(BCCFPageAdmin, self).change_view(request, object_id, **kwargs)

    def delete_view(self, request, object_id, **kwargs):
        """
        Enforce custom delete permissions for the page instance.
        """
        page = get_object_or_404(BCCFPage, pk=object_id)
        content_model = BCCFPage.get_content_model()
        self._check_permission(request, content_model, "delete")
        return super(BCCFPageAdmin, self).delete_view(request, object_id, **kwargs)

    def changelist_view(self, request, extra_context=None):
        """
        Redirect to the ``Page`` changelist view for ``Page``
        subclasses.
        """
        if self.model is not BCCFChildPage:
            return HttpResponseRedirect(admin_url(BCCFChildPage, "changelist"))
        if not extra_context:
            extra_context = {}
        extra_context["page_models"] = self.get_content_models()
        return super(BCCFPageAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        """
        Set the ID of the parent page if passed in via querystring, and
        make sure the new slug propagates to all descendant pages.
        """
        if change and obj._old_slug != obj.slug:
            # _old_slug was set in BCCFPageAdminForm.clean_slug().
            new_slug = obj.slug or obj.generate_unique_slug()
            obj.slug = obj._old_slug
            obj.set_slug(new_slug)

        # Force parent to be saved to trigger handling of ordering and slugs.
        parent = request.GET.get("parent")
        if parent is not None and not change:
            obj.parent_id = parent
            obj.save()
        super(BCCFPageAdmin, self).save_model(request, obj, form, change)

    def _maintain_parent(self, request, response):
        """
        Maintain the parent ID in the querystring for response_add and
        response_change.
        """
        location = response._headers.get("location")
        parent = request.GET.get("parent")
        if parent and location and "?" not in location[1]:
            url = "%s?parent=%s" % (location[1], parent)
            return HttpResponseRedirect(url)
        return response

    def response_add(self, request, obj):
        """
        Enforce page permissions and maintain the parent ID in the
        querystring.
        """
        response = super(BCCFPageAdmin, self).response_add(request, obj)
        return self._maintain_parent(request, response)

    def response_change(self, request, obj):
        """
        Enforce page permissions and maintain the parent ID in the
        querystring.
        """
        response = super(BCCFPageAdmin, self).response_change(request, obj)
        return self._maintain_parent(request, response)

    @classmethod
    def get_content_models(cls):
        """
        Return all Page subclasses that are admin registered, ordered
        based on the ``ADD_PAGE_ORDER`` setting.
        """
        models = []
        for model in BCCFChildPage.get_content_models():
            try:
                admin_url(model, "add")
            except NoReverseMatch:
                continue
            else:
                setattr(model, "meta_verbose_name", model._meta.verbose_name)
                setattr(model, "add_url", admin_url(model, "add"))
                models.append(model)
        order = [name.lower() for name in settings.ADD_PAGE_ORDER]

        def sort_key(page):
            name = "%s.%s" % (page._meta.app_label, page._meta.object_name)
            unordered = len(order)
            try:
                return (order.index(name.lower()), "")
            except ValueError:
                return (unordered, page.meta_verbose_name)
        return sorted(models, key=sort_key)

class BCCFChildAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(BCCFChildAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'bccf_topic',
                                    'featured',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)
                
class BCCFResourceAdmin(DisplayableAdmin):
    def __init__(self, *args, **kwargs):
        super(BCCFResourceAdmin, self).__init__(*args, **kwargs)
        if self.fieldsets == DisplayableAdmin.fieldsets:
            self.fieldsets = deepcopy(self.fieldsets)
            for field in reversed(['content',
                                    'bccf_topic',
                                    'featured',
                                    'page_for',
                                    'image']):
                self.fieldsets[0][1]['fields'].insert(3, field)

admin.site.register(BCCFPage, PageAdmin)
admin.site.register(BCCFTopic)
admin.site.register(BCCFChildPage, BCCFPageAdmin)
admin.site.register(BCCFBabyPage, BCCFPageAdmin)
admin.site.register(Blog, BCCFChildAdmin)
admin.site.register(Program, BCCFChildAdmin)
admin.site.register(Campaign, BCCFChildAdmin)
admin.site.register(Article, BCCFResourceAdmin)
admin.site.register(DownloadableForm, BCCFResourceAdmin)
admin.site.register(Magazine, BCCFResourceAdmin)
admin.site.register(TipSheet, BCCFResourceAdmin)
admin.site.register(Video, BCCFResourceAdmin)

#Inline
class HomeMarqueeSlideInline(admin.TabularInline):
    model = HomeMarqueeSlide.marquee.through

class FooterMarqueeSlideInline(admin.TabularInline):
    model = FooterMarqueeSlide.marquee.through
    
class PageMarqueeSlideInline(admin.TabularInline):
    model = PageMarqueeSlide.marquee.through

#Marquees
class HomeMarqueeAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    inlines = [HomeMarqueeSlideInline]
    
class FooterMarqueeAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    inlines = [FooterMarqueeSlideInline]
    
class PageMarqueeAdmin(admin.ModelAdmin):
    inlines = [PageMarqueeSlideInline]

admin.site.register(HomeMarqueeSlide)
admin.site.register(FooterMarqueeSlide)
admin.site.register(PageMarqueeSlide)
admin.site.register(HomeMarquee, HomeMarqueeAdmin)
admin.site.register(FooterMarquee, FooterMarqueeAdmin)
admin.site.register(PageMarquee, PageMarqueeAdmin)
