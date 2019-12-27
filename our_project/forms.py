# from django import forms
# from django.db import models

# from django.contrib.contenttypes.models import ContentType
# from our_project.models import MyGalleryImage

# from django.apps import apps
# from itertools import chain
# from django.utils.safestring import mark_safe
# from django.contrib import admin


# from django.contrib.admin.widgets import ForeignKeyRawIdWidget
# from django.db.models.fields.related import ManyToOneRel

# from our_project.models import Products


# class ImageTypeForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ImageTypeForm, self).__init__(*args, **kwargs)
#         try:
#             model = self.instance.content_type.model_class()
#             model_key = model._meta.pk.name
#         except:
#             model = Products
#             model_key = 'id'
#         self.fields['object_id'].widget = ForeignKeyRawIdWidget(
#             rel=ManyToOneRel(model, model_key, 'id'), admin_site=admin.site)

#         self.fields['content_type'].widget.widget = ContentTypeSelect('lookup_id_object_id',
#                                                                       self.fields['content_type'].widget.widget.attrs,
#                                                                       self.fields['content_type'].widget.widget.choices)


# class ContentTypeSelect(forms.Select):
#     def __init__(self, lookup_id,  attrs=None, choices=()):
#         self.lookup_id = lookup_id
#         super(ContentTypeSelect, self).__init__(attrs, choices)

#     def render(self, name, value, attrs=None, choices=()):
#         output = forms.Select().render(name, value, attrs, choices)

        

#         choices = chain(self.choices, choices)
#         choiceoutput = ' var %s_choice_urls = {' % (attrs['id'],)
#         for choice in choices:
#             try:
#                 ctype = ContentType.objects.get(pk=int(choice[0]))
#                 choiceoutput += '    \'%s\' : \'../../../%s/%s?t=%s\',' % (str(choice[0]),
#                                                                            ctype.app_label, ctype.model, ctype.model_class()._meta.pk.name)
#             except:
#                 pass
#         choiceoutput += '};'

#         output += ('<script type="text/javascript">'
#                    '(function($) {'
#                    '  $(document).ready( function() {'
#                    '%(choiceoutput)s'
#                    '    $(\'#%(id)s\').change(function (){'
#                    '        $(\'#%(fk_id)s\').attr(\'href\',%(id)s_choice_urls[$(this).val()]);'
#                    '    });'
#                    '  });'
#                    '})(django.jQuery);'
#                    '</script>' % {'choiceoutput': choiceoutput,
#                                   'id': attrs['id'],
#                                   'fk_id': self.lookup_id
#                                   })
#         return mark_safe(u''.join(output))
