import logging
import json
log = logging.getLogger(__name__)

from django.test import TestCase
from django.template.loader import render_to_string

#
# Test Cases for the different models and views used in BCCF
#

####
## Marquees
####
from bccf.models import HomeMarquee, FooterMarquee, PageMarquee

# Home Marquee
class HomeMarqueeTestCase(TestCase):
    def setUp(self):
        "Creates a new Home Marquee Object with a title of `Home Marquee Test 1`"
        self.marquee = HomeMarquee.objects.create(title='Home Marquee Test 1')
    def testProperCreation(self):
        "Tests whether the marquee has been created with the proper title and default values"
        self.assertEqual(self.marquee.title, 'Home Marquee Test 1')
        self.assertEqual(self.marquee.active, False)

# Footer Marquee
class FooterMarqueeTestCase(TestCase):
    def setUp(self):
        "Creates a new Footer Marquee Pbject with a title of `Footer Marquee Test 1`"
        self.marquee = FooterMarquee.objects.create(title='Footer Marquee Test 1')
    def testProperCreation(self):
        self.assertEqual(self.marquee.title, 'Footer Marquee Test 1')
        self.assertEqual(self.marquee.active, False)

# Page Marquee
class PageMarqueeTestCase(TestCase):
    def setUp(self):
        "Creates a new Home Marquee Object with a title of `Home Marquee Test 1`"
        self.marquee = PageMarquee.objects.create(title='Page Marquee Test 1')
    def testProperCreation(self):
        "Tests whether the marquee has been created with the proper title and default values"
        self.assertEqual(self.marquee.title, 'Page Marquee Test 1')
        
####
## Marquee Slides
####
from bccf.models import HomeMarqueeSlide, FooterMarqueeSlide, PageMarqueeSlide

# Home Marquee Slide
class HomeMarqueeSlideTestCase(HomeMarqueeTestCase):
    def setUp(self):
        "Creates a new home marquee and home marquee slide"
        super(HomeMarqueeSlideTestCase, self).setUp()
        self.slide = HomeMarqueeSlide.objects.create(caption='Home Marquee Caption', title='Home Marquee Title')
    def testProperCreation(self):
        "Tests whether the slide was created properly"
        self.assertEqual(self.slide.caption, 'Home Marquee Caption')
        self.assertEqual(self.slide.title, 'Home Marquee Title')

class HomeMarqueeTestCaseAddToMarquee(HomeMarqueeSlideTestCase):
    def testAddingToMarquee(self):
        "Adds the slide to a marquee and test whether it was successful"
        self.slide.marquee.add(self.marquee)
        slides = HomeMarqueeSlide.objects.filter(marquee=self.marquee)
        self.failIf(self.slide not in slides)

# Footer Marquee Slide
class FooterMarqueeSlideTestCase(FooterMarqueeTestCase):
    def setUp(self):
        "Creates a new footer marquee and footer marquee slide"
        super(FooterMarqueeSlideTestCase, self).setUp()
        self.slide = FooterMarqueeSlide.objects.create(caption='Footer Marquee Caption', title='Footer Marquee Title')
    def testProperCreation(self):
        "Tests whether the slide was created properly"
        self.assertEqual(self.slide.caption, 'Footer Marquee Caption')
        self.assertEqual(self.slide.title, 'Footer Marquee Title')

class FooterMarqueeSlideTestCaseAddToMarquee(FooterMarqueeSlideTestCase):
    def testAddingToMarquee(self):
        "Adds the slide to a marquee and test whether it was successful"
        self.slide.marquee.add(self.marquee)
        slides = FooterMarqueeSlide.objects.filter(marquee=self.marquee)
        self.failIf(self.slide not in slides)
        
# Page Marquee Slide
class PageMarqueeSlideTestCase(PageMarqueeTestCase):
    def setUp(self):
        "Creates a new page marquee and page marquee slide"
        super(PageMarqueeSlideTestCase, self).setUp()
        self.slide = PageMarqueeSlide.objects.create(caption='Page Marquee Caption', title='Page Marquee Title')
    def testProperCreation(self):
        "Tests whether the slide was created properly"
        self.assertEqual(self.slide.caption, 'Page Marquee Caption')
        self.assertEqual(self.slide.title, 'Page Marquee Title')

class PageMarqueeSlideTestCaseAddToMarquee(PageMarqueeSlideTestCase):
    def testAddingToMarquee(self):
        "Adds the slide to a marquee and test whether it was successful"
        self.slide.marquee.add(self.marquee)
        slides = PageMarqueeSlide.objects.filter(marquee=self.marquee)
        self.failIf(self.slide not in slides)

####
## Pages
####
from bccf.models import BCCFPage, BCCFTopic, BCCFChildPage, BCCFBabyPage, Article, DownloadableForm, Magazine, TipSheet, Video, Program, Blog, Campaign
from pybb.models import Topic

# BCCF Page
class BCCFPageTestCase(PageMarqueeTestCase):
    def setUp(self):
        "Creates a new Page"
        super(BCCFPageTestCase, self).setUp()
        self.page = BCCFPage.objects.create(title='Test Page', content='Test Content', marquee=self.marquee)
    def testProperCreation(self):
        "Tests whether or not the page was created properly"
        self.assertEqual(self.page.title, 'Test Page')
        self.assertEqual(self.page.content, 'Test Content')
        self.assertEqual(self.page.marquee, self.marquee)
        self.assertEqual(self.page.carousel_color, 'dgreen-list')

# BCCF Topic
class BCCFTopicTestCase(PageMarqueeTestCase):
    def setUp(self):
        "Creates a new Topic Page"
        super(BCCFTopicTestCase, self).setUp()
        self.page = BCCFTopic.objects.create(title='Test Topic', content='Test Content', marquee=self.marquee)
    def testProperCreation(self):
        "Tests whether or not the topic page was created properly"
        self.assertEqual(self.page.title, 'Test Topic')
        self.assertEqual(self.page.content, 'Test Content')
        self.assertEqual(self.page.marquee, self.marquee)
        self.assertEqual(self.page.carousel_color, 'dgreen-list')

class BCCTopicViewTestCase(TestCase):
    def testGetTopicPage(self):
        "Gets the topic page"
        response = self.client.get('/topic/topic-1', follow=True)
        self.assertTemplateUsed(response, 'bccf/topic_page.html')
    def testTopicNext(self):
        "Gets the next set of pages based on topic"
        slides = []
        response = self.client.get('/next/topic/topic-1/parent/12', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        slide = render_to_string('generic/carousel_slide_part.html', {'slides':slides})
        grid = render_to_string('generic/carousel_grid_part.html', {'slides':slides})
        self.assertEqual(data['slide'], slide)
        self.assertEqual(data['grid'], grid)
    def testTopicNextNotAjax(self):
        "Gets the next set of pages based on topic without using ajax"
        response = self.client.get('/next/topic/topic-1/parent/12', follow=True)
        self.assertEqual(response.content, 'No')
    def testTopicErrors(self):
        "Tests errors"
        response = self.client.get('/topic/no-topic', follow=True)
        self.assertEqual(response.status_code, 404)

# BCCF Child Page
class BCCFChildPageTestCase(TestCase):
    def setUp(self):
        "Creates a new Topic Page"
        self.page = BCCFPage.objects.create(title='Test Page', content='Test Content')
        self.child = BCCFChildPage.objects.create(title='Test Child', content='Test Content', gparent=self.page)
    def testProperCreation(self):
        "Tests whether or not the child page was created properly"
        self.assertEqual(self.child.title, 'Test Child')
        self.assertEqual(self.child.content, 'Test Content')
        self.assertEqual(self.child.gparent, self.page)
        
class BCCFChildPageTestCaseFeaturedTrue(BCCFChildPageTestCase):
    def setUp(self):
        "Changes the page to become a featured"
        super(BCCFChildPageTestCaseFeaturedTrue, self).setUp()
        self.child.featured = True
        self.child.save()
        self.assertEqual(self.child.featured, True)
    def testGetChildViaFeatured(self):
        "Test to get the child page via the featured rule"
        children = BCCFChildPage.objects.filter(featured=True)
        self.failIf(self.child not in children)
        
class BCCFChildPageTestCaseFeaturedFalse(BCCFChildPageTestCase):
    def setUp(self):
        "Changes the page to not become a featured"
        super(BCCFChildPageTestCaseFeaturedFalse, self).setUp()
        self.child.featured = False
        self.child.save()
        self.assertEqual(self.child.featured, False)
    def testGetChildViaFeatured(self):
        "Test to get the child page via the featured rule"
        children = BCCFChildPage.objects.filter(featured=False)
        self.failIf(self.child not in children)
        
class BCCFChildPageTestCaseGparent(BCCFChildPageTestCase):
    def testGetChildViaGparent(self):
        "Test to get the child page via the gparent rule"
        children = BCCFChildPage.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
class BCCFChildPageTestCasePageForParent(BCCFChildPageTestCase):
    def setUp(self):
        "Sets page for parent"
        super(BCCFChildPageTestCasePageForParent, self).setUp()
        self.child.page_for = 'parent'
        self.child.save()
        self.assertEqual(self.child.page_for, 'parent')
    def testGetChildViaPageFor(self):
        "Test to get child page via page for rule"
        children = BCCFChildPage.objects.filter(page_for='parent')
        self.failIf(self.child not in children)
        
class BCCFChildPageTestCasePageForProfessional(BCCFChildPageTestCase):
    def setUp(self):
        "Sets page for professional"
        super(BCCFChildPageTestCasePageForProfessional, self).setUp()
        self.child.page_for = 'professional'
        self.child.save()
        self.assertEqual(self.child.page_for, 'professional')
    def testGetChildViaPageFor(self):
        "Test to get child page via page for rule"
        children = BCCFChildPage.objects.filter(page_for='professional')
        self.failIf(self.child not in children)

class BCCFChildPageTestCaseTopic(BCCFChildPageTestCase):
    def setUp(self):
        "Sets page to have topic"
        super(BCCFChildPageTestCaseTopic, self).setUp()
        self.topic1 = BCCFTopic.objects.create(title='Topic 1', content='Test Content')
        self.topic2 = BCCFTopic.objects.create(title='Topic 2', content='Test Content')
        
class BCCFChildPageTestTopicGet1(BCCFChildPageTestCaseTopic):
    def setUp(self):
        "Set Topic to Topic 1"
        super(BCCFChildPageTestTopicGet1, self).setUp();        
        self.child.bccf_topic.add(self.topic1)
        self.child.save()
    def testGetChildViaTopic(self):
        "Get the child page via the topic rule"
        children = BCCFChildPage.objects.filter(bccf_topic=self.topic1)
        self.failIf(self.child not in children)
        
class BCCFChildPageTestTopicGet2(BCCFChildPageTestCaseTopic):
    def setUp(self):
        "Set Topic to Topic 2"
        super(BCCFChildPageTestTopicGet2, self).setUp();        
        self.child.bccf_topic.add(self.topic2)
        self.child.save()
    def testGetChildViaTopic(self):
        "Get the child page via the topic rule"
        children = BCCFChildPage.objects.filter(bccf_topic=self.topic2)
        self.failIf(self.child not in children)

class BCCFChildPageViewsTestCase(TestCase):
    def testGetPage(self):
        "Get the Gparent page"
        response = self.client.get('/resources/', follow=True)
        self.assertTemplateUsed('bccf/resources_page.html')
        response = self.client.get('/blog/', follow=True)
        self.assertTemplateUsed('bccf/blog_page.html')
        response = self.client.get('/news/', follow=True)
        self.assertTemplateUsed('bccf/news_page.html')
        response = self.client.get('/tag/', follow=True)
        self.assertTemplateUsed('bccf/tag_page.html')
        response = self.client.get('/programs/', follow=True)
        self.assertTemplateUsed('bccf/programs_page.html')
        response = self.client.get('/trainings/', follow=True)
        self.assertTemplateUsed('bccf/trainings_page.html')
    def testGetChildPage(self):
        "Get Child Page"
        response = self.client.get('/resources/article/', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTemplateUsed('generic/sub_page.html')
    def testGetNext(self):
        "Get Next set of pages"
        slides = []
        response = self.client.get('/next/resources/article/12', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        slide = render_to_string('generic/carousel_slide_part.html', {'slides':slides})
        grid = render_to_string('generic/carousel_grid_part.html', {'slides':slides})
        self.assertEqual(data['slide'], slide)
        self.assertEqual(data['grid'], grid)
    def testGetNextNotAjax(self):
        "Get Next set of pages without ajax"
        response = self.client.get('/next/resources/article/12', follow=True)
        self.assertEqual(response.content, 'No')
    def testFilter(self):
        "Test Forum Topic Filtering"
        slides = Topic.objects.filter(slug='stuff-3')
        response = self.client.get('/filter/example', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        slide = render_to_string('generic/carousel_slide_part.html', {'slides':slides})
        grid = render_to_string('generic/carousel_grid_part.html', {'slides':slides})
        self.assertEqual(data['slide'], slide)
        self.assertEqual(data['grid'], grid)
    def testFilterEmpty(self):
        "Test Forum Topic Filtering with empty query"
        gparent = BCCFPage.objects.get(slug='tag')
        slides = BCCFChildPage.objects.filter(gparent=gparent.pk, content_model='topic', status=2).order_by('-created')[:12]
        response = self.client.get('/filter//', follow=True, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        slide = render_to_string('generic/carousel_slide_part.html', {'slides':slides})
        grid = render_to_string('generic/carousel_grid_part.html', {'slides':slides})
        self.assertEqual(data['slide'], slide)
        self.assertEqual(data['grid'], grid)
    def testFilterNotAjax(self):
        "Test forum topic filtering without ajax"
        response = self.client.get('/filter//', follow=True)
        self.assertEqual(response.content, 'No')       
        
# Baby Page
class BCCFBabyPageTestCase(TestCase):
    def setUp(self):
        "Creates new BCCF Baby Page"
        self.child = BCCFChildPage.objects.create(title='Test Child', content='Test Content')
        self.baby = BCCFBabyPage.objects.create(title='Test Baby', content='Test Content', parent=self.child)
    def testProperCreation(self):
        "Test if BCCF Baby Page was properly created"
        self.assertEqual(self.baby.title, 'Test Baby')
        self.assertEqual(self.baby.content, 'Test Content')
        self.assertEqual(self.baby.parent, self.child)
        
class BCCFBabyPageTestCaseParent(BCCFBabyPageTestCase):
    def testGetBabyViaParent(self):
        "Get the baby page via the parent rule"
        babies = BCCFBabyPage.objects.filter(parent=self.child)
        self.failIf(self.baby not in babies)
        
# Resource
class ResourcesTestCase(TestCase):
    def setUp(self):
        "Create new Resource Page"
        self.page = BCCFPage.objects.get(slug='resources')

# Article       
class ArticleResourceTestCaseGetViaGparent(ResourcesTestCase):
    def setUp(self):
        "Create new Article"
        super(ArticleResourceTestCaseGetViaGparent, self).setUp()
        self.child = Article.objects.create(title='Test Article', content='Test Content')
    def testGetArticleViaGparent(self):
        "Get the Article via the Gparent rule"
        children = Article.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)

# Downloadable Form     
class DownloadableFormResourceTestCaseGetViaGparent(ResourcesTestCase):
    def setUp(self):
        "Create new Downloadable Form"
        super(DownloadableFormResourceTestCaseGetViaGparent, self).setUp()
        self.child = DownloadableForm.objects.create(title='Test Downloadable Form', content='Test Content')
    def testGetDownloadableFormViaGparent(self):
        "Get the Downloadable Form via the Gparent rule"
        children = DownloadableForm.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)

# Magazine
class MagazineResourceTestCaseGetViaGparent(ResourcesTestCase):
    def setUp(self):
        "Create new Magazine"
        super(MagazineResourceTestCaseGetViaGparent, self).setUp()
        self.child = Magazine.objects.create(title='Test Magazine', content='Test Content')
    def testGetMagazineViaGparent(self):
        "Get the Magazine via the Gparent rule"
        children = Magazine.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
# Tip Sheet
class TipSheetResourceTestCaseGetViaGparent(ResourcesTestCase):
    def setUp(self):
        "Create new Tip Sheet"
        super(TipSheetResourceTestCaseGetViaGparent, self).setUp()
        self.child = TipSheet.objects.create(title='Test Tip Sheet', content='Test Content')
    def testGetTipSheetViaGparent(self):
        "Get the Tip Sheet via the Gparent rule"
        children = TipSheet.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
# Video
class VideoResourceTestCaseGetViaGparent(ResourcesTestCase):
    def setUp(self):
        "Create new Tip Sheet"
        super(VideoResourceTestCaseGetViaGparent, self).setUp()
        self.child = Video.objects.create(title='Test Video', content='Test Content')
    def testGetVideoViaGparent(self):
        "Get the Video via the Gparent rule"
        children = Video.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
# Program
class ProgramTestCaseGetViaGparent(TestCase):
    def setUp(self):
        "Create new Page for Program"
        self.page = BCCFPage.objects.get(slug='programs')
        self.child = Program.objects.create(title='Test Program', content='Test Content')
    def testGetProgramViaGparent(self):
        "Get the Program via the Gparent Rule"
        children = Program.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
# Blog
class BlogTestCaseGetViaGparent(TestCase):
    def setUp(self):
        "Create new Page for Blog"
        self.page = BCCFPage.objects.get(slug='blog')
        self.child = Blog.objects.create(title='Test Blog', content='Test Content')
    def testGetBlogViaGparent(self):
        "Get the Blog via the Gparent Rule"
        children = Blog.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
# Campaign
class CampaignTestCaseGetViaGparent(TestCase):
    def setUp(self):
        "Create new Page for Campaign"
        self.page = BCCFPage.objects.get(slug='tag')
        self.child = Campaign.objects.create(title='Test Blog', content='Test Content')
    def testGetCampaignViaGparent(self):
        "Get the Campaign via the Gparent Rule"
        children = Campaign.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)
        
####
## Events
####
from bccf.models import EventForParents, EventForProfessionals
from django.contrib.auth.models import User

class EventTestCase(TestCase):
    def setUp(self):
        "Create new Page for events"
        self.page = BCCFPage.objects.get(slug='trainings')
        self.user = User.objects.get(username='admin')    
    
# Event for Parents    
class EventForParentsTestCase(EventTestCase):
    def setUp(self):
        "Create new Event for parent"
        super(EventForParentsTestCase, self).setUp()
        self.child = EventForParents.objects.create(title='Test Event for Parent', content='Test Content',
            price=500, provider=self.user)

class EventforParentsTestCaseGetViaGparent(EventForParentsTestCase):
    def testGetEventForParentViaGparent(self):
        "Get Event for Parent via the Gparent Rule"
        children = EventForParents.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)

class EventforParentsTestCaseGetViaUser(EventForParentsTestCase):
    def testGetEventForParentViaUser(self):
        "Get Event for Parent via the User Rule"
        children = EventForParents.objects.filter(provider=self.user)
        self.failIf(self.child not in children)
        
# Event for Professionals
class EventForProfessionalsTestCase(EventTestCase):
    def setUp(self):
        "Create new event for professionals"
        super(EventForProfessionalsTestCase, self).setUp()
        self.child = EventForProfessionals.objects.create(title='Test Event for Professionals', content='Test Content',
            price=500, provider=self.user)

class EventforProfessionalsTestCaseGetViaGparent(EventForProfessionalsTestCase):
    def testGetEventForParentViaGparent(self):
        "Get Event for Parent via the Gparent Rule"
        children = EventForProfessionals.objects.filter(gparent=self.page)
        self.failIf(self.child not in children)

class EventforProfessionalsTestCaseGetViaUser(EventForProfessionalsTestCase):
    def testGetEventForParentViaUser(self):
        "Get Event for Parent via the User Rule"
        children = EventForProfessionals.objects.filter(provider=self.user)
        self.failIf(self.child not in children)
        
####
## User Directory
####        
class UserDirectoryTestCase(TestCase):
    def testUserDirectory(self):
        "Test loading user directory"
        response = self.client.get('/member/directory/', follow=True)
        self.assertTemplateUsed('bccf/user_directory.html')
        
####
## Form builder
####
from formable.builder.models import FormStructure, FormPublished, FormFilled, Question, FieldAnswer

class FormBuilderViewTestCase(TestCase):
    def testOpenBuilderNotLoggedIn(self):
        "Test going to creator while not logged in"
        response = self.client.get('/formable/create/', follow=True)
        self.assertRedirects(response, 'accounts/login/?next=/formable/create/')
    def testOpenBuilderViaPost(self):
        "Test Open builder via post"
        response = self.client.post('/formable/create/', follow=True)
        self.assertEqual(response.status_code, 405)
    def testOpenBuilderLoggedIn(self):
        "Test Open builder when logged in"
        self.client.login(username='admin', password='admin')
        response = self.client.get('/formable/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'builder_page.html')
    def testSaveStructViaGet(self):
        "Test save form structure when via get"
        response = self.client.get('/formable/save/', follow=True)
        self.assertEqual(response.status_code, 405)
    def testSaveStructureNotLoggedIn(self):
        "Test save structure when not logged in"
        topic = BCCFTopic.objects.get(slug='topic-1')
        response = self.client.post('/formable/save/', {'bccf_topic':topic.pk, 'title':'Test Form', 'structure':'{"title":"Test","fieldset":[{"title":"Stuff","fields":[{"class":"text-field","label":"Text","attr":{"type":"text","name":"text-field"}}]}]}', 'content':'Test Content', 'page_for':'professionals'}, follow=True)
        self.assertRedirects(response, 'accounts/login/?next=/formable/save/')
    def testSaveStructureLoggedIn(self):
        "Test save structuere when logged in and via post"
        self.client.login(username='admin', password='admin')
        topic = BCCFTopic.objects.get(slug='topic-1')
        response = self.client.post('/formable/save/', {'bccf_topic':topic.pk, 'title':'Test Form', 'structure':'{"title":"Test","fieldset":[{"title":"Stuff","fields":[{"class":"text-field","label":"Text","attr":{"type":"text","name":"text-field"}}]}]}', 'content':'Test Content', 'page_for':'professionals'}, follow=True)
        self.assertRedirects(response, '/formable/view/test-form/')
    def testViewFormNotLoggedIn(self):
        "Test view form when not logged in"
        response = self.client.get('/formable/view/test-form/', follow=True)
        self.assertRedirects(response, 'accounts/login/?next=/formable/view/test-form/')
    def testViewFormLoggedIn(self):
        "Test view form logged in"
        self.client.login(username='admin', password='admin')
        topic = BCCFTopic.objects.get(slug='topic-1')
        self.client.post('/formable/save/', {'bccf_topic':topic.pk, 'title':'Test Form', 'structure':'{"title":"Test","fieldset":[{"title":"Stuff","fields":[{"class":"text-field","label":"Text","attr":{"type":"text","name":"text-field"}}]}]}', 'content':'Test Content', 'page_for':'professionals'}, follow=True)
        response = self.client.get('/formable/view/test-form/', follow=True)
        self.assertTemplateUsed(response, 'view_form.html')
    def testViewFormViaPost(self):
        "Test view form via post"
        topic = BCCFTopic.objects.get(slug='topic-1')
        self.client.post('/formable/save/', {'bccf_topic':topic.pk, 'title':'Test Form', 'structure':'{"title":"Test","fieldset":[{"title":"Stuff","fields":[{"class":"text-field","label":"Text","attr":{"type":"text","name":"text-field"}}]}]}', 'content':'Test Content', 'page_for':'professionals'}, follow=True)
        response = self.client.post('/formable/view/test-form/', follow=True)
        self.assertEqual(response.status_code, 405)
    def testSubmitFormNotLoggedIn(self):
        response = self.client.post('/formable/submit/', follow=True)
        self.assertRedirects(response, 'accounts/login/?next=/formable/submit/')
    def testSubmitFormViaGet(self):
        response = self.client.get('/formable/submit/', follow=True)
        self.assertEqual(response.status_code, 405)
    def testSubmitFormViaPost(self):
        "Test submit form via post"
        self.client.login(username='admin', password='admin')
        response = self.client.post('/formable/submit/', {'publish_id':21, '1.test_field': 'Help'}, follow=True)
        self.assertRedirects(response, '/formable/success/')

####
## Template Tags
####
class ContentCarouselTestCase(TestCase):
    def testContentCarosuelFor(self):
        "Test Content Carousel Creation"
        