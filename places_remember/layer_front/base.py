# coding: utf-8


from django.forms import Form


class BaseForm(Form):

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly', None)
        super().__init__(*args, **kwargs)
        if readonly:
            for field in self:
                field.field.widget.attrs.update({'readonly': True})


def field_factory(obj, input_type_val):
    setattr(obj, 'hi_type', input_type_val)
    return obj
