from django import template

register = template.Library()

@register.filter
def mazerango_class(field, css_class):
    attr = field.field.widget.attrs
    is_required = field.field.required
    widget = field.field.widget
    if hasattr(widget, 'input_type') and widget.input_type == 'select':
        field.field.widget.template_name = 'mazerango/widgets/select.html'
        return field
    if 'class' in attr:
        attr_dict = {"class": f"{css_class} {attr['class']}"}
        attr_dict.update({
            "data-parsley-required": "true" if is_required else "false"
        })
        return field.as_widget(attrs=attr_dict)
    return field.as_widget(attrs={"class": f"{css_class}"})


@register.filter
def mazerango_checkbox(field):
    return field.as_widget(attrs={"class": "form-check-input"})

@register.filter
def mazerango_label(field):
    return field.field.label_tag(attrs={"class": "form-label"})

@register.filter
def mazerango_field_label(field):
    return field.label_tag(attrs={"class": "form-label"})

@register.filter
def login_password(value):
    value.field.widget.attrs.update({
        'class': 'form-control form-control-xl',
        'placeholder': 'Password'
    })
    return value

@register.filter
def login_username(value):
    value.field.widget.attrs.update({
        'class': 'form-control form-control-xl',
        'placeholder': 'Username'
    })
    return value
