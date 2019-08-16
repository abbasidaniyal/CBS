from django.contrib import admin

from .models import HomePage,AboutUsInfo,Carousel,ContactUs,WhyUsCard
# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
      list_display    = ['name','email','contact_number','query','query_date']

class WhyUsInline(admin.StackedInline):
    '''Stacked Inline View for WhyUs'''

    model = WhyUsCard
    min_num = 2
    max_num = 4
    ordering = ['-id']
    

class AboutUsAdmin(admin.ModelAdmin):
    '''Admin View for AboutUs'''

    # list_display = ('')
    inlines = [
        WhyUsInline,
    ]


admin.site.register(HomePage)
admin.site.register(AboutUsInfo,AboutUsAdmin)
admin.site.register(Carousel)
admin.site.register(ContactUs,ContactUsAdmin)

