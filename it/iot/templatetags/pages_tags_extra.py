import math
import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
@stringfilter
def contains(value, arg):
    return arg in value

@register.filter
@stringfilter
def endswith(value, arg):
    return value.endswith( arg )

@register.filter
def get_val(item_list, idx):
    if len( item_list ) > idx:
        return item_list[idx]

@register.filter
def add(value, arg):
    return value + arg

@register.filter
def minus(value, arg):
    return value - arg

@register.filter
def first_half(item_list):
    half = len( item_list ) / 2
    return item_list[:half]

@register.filter
def last_half(item_list):
    half = len( item_list ) / 2
    return item_list[half:]

@register.filter
def nhalf(item_list):
    return len( item_list ) / 2

@register.filter
def has_right(item_list):
    return len( item_list ) > 1

def _intcomma(value, first_pass=True):
    """
    Converts an integer to an Indian-style curency string, e.g., 1,23,400
    Borrows from contrib.humanize.templatetags.humanize.intcomma
    """
    orig = force_unicode( value )

    if first_pass:
        new = re.sub( "^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig )
    else:
        new = re.sub( "^(-?\d+)(\d{2})", '\g<1>,\g<2>', orig )

    if orig == new:
        return '<div class="app-value"><img alt="display" src="/it_media/v4/images/inr.png"/>&nbsp;%s</div>' % new
    else:
        return _intcomma( new, False )

@register.filter
def display_api_txt(value):
    """Meant mostly for single-valued entries like user name"""
    txt = ''
    i = 0
    for d in value:
        i += 1
        display_title = d.get( 'display_title', '' )
        # Default display type is assumed to be text
        display_type = d.get( 'display_type', 'text' )
        display_value = d.get( 'display_value' )
        display_url = d.get( 'display_url' )
        display_helptext = d.get( 'display_helptext' )
        display_helpurl = d.get( 'display_helpurl' )
        # FIXME: Here we have nowhere to hook "active" to
        display_active = d.get( 'display_active' )
        display_icon = d.get( 'display_icon' )

        if display_icon:
            # CSS as per shortcuts at top of right panel
            display_title = '<div class="app-right-icon"><img alt="display" src="/it_media/v4/images/%s"/></div>' % display_icon + display_title

        if display_value is not None:
            if display_type == "numeric":
                display_value = str( display_value )
            elif display_type == "currency":
                display_value = _intcomma( display_value )

        if display_url:
            display_target = d.get( 'display_target', 'onpage' )
            if display_target == 'inline':
                # We hook fancybox into a class of this name
                display_title = '<a href="%s" class="fancy-popup">%s</a>' % (display_url, display_title)
            elif display_target == 'newtab':
                display_title = '<a href="%s" target="_blank">%s</a>' % (display_url, display_title)
            else:  # "onpage"
                display_title = '<a href="%s">%s</a>' % (display_url, display_title)

        if display_value is not None:
            # CSS as per summary towards top of right panel
            display_title += '<span class="app-wht-txt2"><img alt="gt" src="/it_media/v4/images/grey-gt.jpg"/></span><span class="app-wht-txt3">%s</span>' % display_value

        if display_helptext:
            if display_helpurl:
                display_helptarget = d.get( 'display_helptarget', 'onpage' )
                if display_helptarget == 'onpage':
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#da-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="da-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                elif display_helptarget == 'newtab':
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#da-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="da-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" target="_blank">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                else:
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#da-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="da-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" class="fancy-popup">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
            else:
                display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#da-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="da-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext)

        txt += display_title + '\n'

    return txt

@register.filter
def display_nav_bar(value, arg=None):
    """For navigation bar at top of page"""
    # Get classes from argument, if it exists. This is for co-branding
    if arg:
        classes = arg.get( 'classes' )
        if classes:
            li_active_class = classes.get( 'li_active_class', 'app-crt' )
            divider_class = classes.get( 'divider_class', 'app-divider' )
    else:
        li_active_class = 'app-crt';
        divider_class = 'app-divider'

    txt = '<ul>'
    i = 0
    for d in value:
        i += 1
        display_title = d.get( 'display_title', '' )
        # We ignore display_type: Convert everything to string for display
        display_type = d.get( 'display_type' )
        display_value = d.get( 'display_value', '' )
        display_url = d.get( 'display_url' )
        display_helptext = d.get( 'display_helptext' )
        display_helpurl = d.get( 'display_helpurl' )
        display_active = d.get( 'display_active' )
        display_icon = d.get( 'display_icon' )

        if display_active:
            li_text = '<li  class="%s" >' % li_active_class
        else:
            li_text = '<li>'

        if display_icon:
            # CSS as per shortcuts at top of right panel
            display_title = '<div class="app-right-icon"><img alt="display" src="/it_media/v4/images/%s"/></div>' % display_icon + display_title
            
        if display_value is not None:
            if display_type == "numeric":
                display_value = str( display_value )
            elif display_type == "currency":
                display_value = _intcomma( display_value )

        if display_url:
            display_target = d.get( 'display_target', 'onpage' )
            if display_target == 'inline':
                # We hook fancybox into a class of this name
                display_title = '<a href="%s" class="fancy-popup">%s</a>' % (display_url, display_title)
            elif display_target == 'newtab':
                display_title = '<a href="%s" target="_blank">%s</a>' % (display_url, display_title)
            else:  # "onpage"
                display_title = '<a href="%s">%s</a>' % (display_url, display_title)

        if display_value is not None:
            # CSS as per summary towards top of right panel
            display_title += '<span class="app-wht-txt2"><img alt="gt" src="/it_media/v4/images/grey-gt.jpg"/></span><span class="app-wht-txt3">%s</span>' % display_value

        if display_helptext:
            if display_helpurl:
                display_helptarget = d.get( 'display_helptarget', 'onpage' )
                if display_helptarget == 'onpage':
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dn-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dn-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                elif display_helptarget == 'newtab':
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dn-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dn-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" target="_blank">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                else:
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dn-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dn-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" class="fancy-popup">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl) 
            else:
                display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dn-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dn-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext)

        display_title += '<div class="%s">&nbsp;</div>' % divider_class
        txt += li_text + display_title + '</li>\n'

    # Make tabs a multiple of 7
    ntabs = len( value )
    nmax = int( math.ceil( float( ntabs ) / 7 ) ) * 7
    for i in range( ntabs, nmax ):
        if i == ntabs:
            txt += '<li class="first-extra">&nbsp;</li>'
        else:
            txt += '<li><div class="%s">&nbsp;</div></li>\n' % divider_class

    txt += '</ul>'
    return txt

@register.filter
def display_shortcuts(value):
    """For shortcuts at top of right panel"""
    """For navigation bar at top of page"""
    txt = ''
    i = 0
    for d in value:
        i += 1
        display_title = d.get( 'display_title', '' )
        # We ignore display_type: Convert everything to string for display
        display_type = d.get( 'display_type' )
        display_value = d.get( 'display_value', '' )
        display_url = d.get( 'display_url' )
        display_helptext = d.get( 'display_helptext' )
        display_helpurl = d.get( 'display_helpurl' )
        # Here we have nowhere to hook "active" to
        display_active = d.get( 'display_active' )
        display_icon = d.get( 'display_icon' )

        if display_icon:
            # CSS as per shortcuts at top of right panel
            display_txt = '<div class="app-right-icon"><img alt="display" src="/it_media/v4/images/%s"/></div>' % display_icon
        else:
            display_txt = ''
            
        if display_value is not None:
            if display_type == "numeric":
                display_value = str( display_value )
            elif display_type == "currency":
                display_value = _intcomma( display_value )

        if display_url:
            display_target = d.get( 'display_target', 'onpage' )
            if display_target == 'inline':
                # We hook fancybox into a class of this name
                display_title = '<a href="%s" class="fancy-popup">%s</a>' % (display_url, display_title)
            elif display_target == 'newtab':
                display_title = '<a href="%s" target="_blank">%s</a>' % (display_url, display_title)
            else: # "onpage"
                display_title = '<a href="%s">%s</a>' % (display_url, display_title)

        display_txt += '<div class="app-right-t1">%s' % display_title

        if display_value is not None:
            # CSS as per summary towards top of right panel
            display_title += '<span class="app-wht-txt2"><img alt="gt" src="/it_media/v4/images/grey-gt.jpg"/></span><span class="app-wht-txt3">%s</span>' % str( display_value )

        if display_helptext:
            if display_helpurl:
                display_helptarget = d.get( 'display_helptarget', 'onpage' )
                if display_helptarget == 'onpage':
                    display_txt += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#ds-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="ds-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                elif display_helptarget == 'newtab':
                    display_txt += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#ds-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="ds-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" target="_blank">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                else:
                    display_txt += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#ds-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="ds-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" class="fancy-popup">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
            else:
                display_txt += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#ds-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="ds-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext)

        txt += display_txt + '</div>\n'

    # FIXME: Divider moved into app.html
    # txt += '<div class="argt-divider"><div class="clear-app"></div></div>'

    return txt

@register.filter
def display_summary(value):
    """For summary towards top of right"""
    txt = '<div class="app-right-txt">'
    i = 0
    save_text = ''
    for d in value:
        i += 1
        display_title = d.get( 'display_title', '' )
        # We ignore display_type: Convert everything to string for display
        display_type = d.get( 'display_type' )
        display_value = d.get( 'display_value', '' )
        display_url = d.get( 'display_url' )
        display_helptext = d.get( 'display_helptext' )
        display_helpurl = d.get( 'display_helpurl' )
        display_active = d.get( 'display_active' )
        display_icon = d.get( 'display_icon' )

        if display_value is not None:
            if display_type == "numeric":
                display_value = str( display_value )
            elif display_type == "currency":
                display_value = _intcomma( display_value )

        help_text = ''
        if display_helptext:
            if display_helpurl:
                display_helptarget = d.get('display_helptarget', 'onpage')
                if display_helptarget == 'onpage':
                    help_text += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dm-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dm-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                elif display_helptarget == 'newtab':
                    help_text += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dm-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dm-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" target="_blank">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                else:
                    help_text += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dm-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dm-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" class="fancy-popup">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
            else:
                help_text += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dm-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dm-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext)

        if display_active:
            # Should be only one such item
            save_text = '<div class="app-txt-summary"><div class="app-wht-txtbox"><p>%s</p><span class="app-wht-txt2"><img alt="gt" src="/it_media/v4/images/grey-gt.jpg"/></span><span class="app-wht-txt4">%s</span>%s</div></div>' % (display_title, display_value, help_text)
        else:
            if display_url:
                display_target = d.get( 'display_target', 'onpage' )
                if display_target == 'inline':
                    # We hook fancybox into a class of this name 
                    display_title = '<a href="%s" class="fancy-popup">%s</a>' % (display_url, display_title)
                elif display_target == 'newtab':
                    display_title = '<a href="%s" target="_blank">%s</a>' % (display_url, display_title)
                else:  # "onpage"
                    display_title = '<a href="%s">%s</a>' % (display_url, display_title)

            if display_icon:
                # CSS as per shortcuts at top of right panel
                display_title = '<div class="app-right-icon"><img alt="display" src="/it_media/v4/images/%s"/></div><div "app-title"><p>%s</p></div>' % (display_icon, display_title)
            else:
                display_title = '<p>%s</p>' % display_title
            
            if display_value is not None:
                # CSS as per summary towards top of right panel
                display_title += '<span class="app-wht-txt2"><img alt="gt" src="/it_media/v4/images/grey-gt.jpg"/></span><span class="app-wht-txt3">%s</span>' % str( display_value )

            txt += '<div class="app-wht-txt1">%s</div>' % (display_title + help_text) + '\n'

    txt += '</div>  <!-- .app-right-txt -->' + save_text

    return txt

@register.filter
def display_return_info(value):
    """For return info at right of header (next to logo image)"""
    # Gora: &nbsp; is to fix IE6 line-indent idiosyncrasies
    txt = '<div class="app-logo-txt"> '
    i = 0
    for d in value:
        i += 1
        display_title = d.get( 'display_title', '' )
        # We ignore display_type: Convert everything to string for display
        display_type = d.get( 'display_type' )
        display_value = d.get( 'display_value', '' )
        display_url = d.get( 'display_url' )
        display_helptext = d.get( 'display_helptext' )
        display_helpurl = d.get( 'display_helpurl' )
        display_active = d.get( 'display_active' )
        display_icon = d.get( 'display_icon' )

        if display_value is not None:
            if display_type == "numeric":
                display_value = str( display_value )
            elif display_type == "currency":
                display_value = _intcomma( display_value )

        if display_active:
            display_title = '<strong>%s</strong>' % display_title

        if display_icon:
            # CSS as per shortcuts at top of right panel
            display_title = '<div class="app-right-icon"><img alt="display" src="/it_media/v4/images/%s"/><p>%s</p></div>' % (display_icon, display_title)
        else:
             display_title = '<p>%s</p>' % display_title
            
        if display_url:
            display_target = d.get( 'display_target', 'onpage' )
            if display_target == 'inline':
                # We hook fancybox into a class of this name
                display_title = '<a href="%s" class="fancy-popup">%s</a>' % (display_url, display_title)
            elif display_target == 'newtab':
                display_title = '<a href="%s" target="_blank">%s</a>' % (display_url, display_title)
            else: # "onpage"
                display_title = '<a href="%s">%s</a>' % (display_url, display_title)

        if display_value is not None:
            # CSS as per summary towards top of right panel
            display_title += '<span class="app-wht-txt2"><img alt="gt" src="/it_media/v4/images/grey-gt.jpg"/></span><span class="app-wht-txt3">%s</span>' % str( display_value )

        if display_helptext:
            if display_helpurl:
                display_helptarget = d.get( 'display_helptarget', 'onpage' )
                if display_helptarget == 'onpage':
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dr-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dr-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                elif display_helptarget == 'newtab':
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dr-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dr-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" target="_blank">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
                else:
                    display_title += '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dr-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dr-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s<br/><a href="%s" class="fancy-popup">Click here</a> for more info.</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext, display_helpurl)
            else:
                display_title +=  '<div class="display-help"><div><div class="app-form-ico"><a id="inline" href="#dr-%d" class="fancy-popup"><img alt="question-mark" src="/it_media/v4/images/form-icon1.jpg"/></a></div></div></div><div class="clear-app"></div><div style="display:none"><div id="dr-%d" class="gloss-data"><div class="pan-top"><div class="pan-head">Taxspanner help</div><div class="pan-txt">%s</div><div class="gloss-divider"></div></div></div></div>' % (i, i, display_helptext)

        txt += display_title + '<div class="clear-app"></div>\n'

    txt += '</div>  <!-- .app-logo-txt -->'

    return txt
