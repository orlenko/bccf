import unittest

#
# Test Cases for the different models used in BCCF
#

####
## Marquees
####
from bccf.models import HomeMarquee, FooterMarquee, PageMarquee

# Home Marquee
class HomeMarqueeTestCase(unittest.TestCase):
    def setUp(self):
        "Creates a new Home Marquee Object with a title of `Home Marquee Test 1`"
        self.marquee = HomeMarquee.objects.create(title='Home Marquee Test 1')
    def testProperCreation(self):
        "Tests whether the marquee has been created with the proper title and default values"
        self.assertEqual(self.marquee.title, 'Home Marquee Test 1')
        self.assertEqual(self.marquee.active, False)

# Footer Marquee
class FooterMarqueeTestCase(unittest.TestCase):
    def setUp(self):
        "Creates a new Footer Marquee Pbject with a title of `Footer Marquee Test 1`"
        self.marquee = FooterMarquee.objects.create(title='Footer Marquee Test 1')
    def testProperCreation(self):
        self.assertEqual(self.marquee.title, 'Footer Marquee Test 1')
        self.assertEqual(self.marquee.active, False)

# Page Marquee
class PageMarqueeTestCase(unittest.TestCase):
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

# BCCF Child Page
class BCCFChildPageTestCase(unittest.TestCase):
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
        
# Baby Page
class BCCFBabyPageTestCase(unittest.TestCase):
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
        
# Article
class ArticleTestCase(unittest.TestCase):
    def setUp(self):
        pass