from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet

class GenericPage(Page):
    banner_title = models.CharField(max_length=100,
     default='Welcome to Wagtail')

    introduction = models.TextField(blank=True)

    banner_image = models.ForeignKey('wagtailimages.Image', null=True,blank=False,
    on_delete=models.SET_NULL,related_name='+',)

    content_panels = Page.content_panels + [
        FieldPanel('banner_title'),
        FieldPanel('introduction'),
        ImageChooserPanel("banner_image"),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100,blank=True)
    company_url=models.URLField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+',)

    
