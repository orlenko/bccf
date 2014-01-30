from mezzanine.pages.page_processors import processor_for

from bccf.models import BCCFPage

@processor_for(BCCFPage)
def bccfpage(request, page):
    return {'child':None, 'baby':None}