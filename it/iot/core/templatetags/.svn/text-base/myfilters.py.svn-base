from django.template import Library

register = Library()

@register.filter(name='genchecked')
def gen_checked(value, arg):
    "Returns checked when value matches the argument"
    if (value == arg):
        return '\" checked = \"checked'
    else:
        return""

@register.filter(name='genselected')
def gen_selected(value, arg):
    "Returns checked when value matches the argument"
    if (value == arg):
        return '\" selected = \"selected'
    else:
        return""

@register.filter(name='displayfloatwithcomma')
def display_float_with_comma(value):
    """
    Converts the input string into a floating point number with commas.
    For example 12 -> 12, 12.1 -> 12.10, 121212.12 ->1,21,212.12
    """
    # incase the input type is not a string, convert into one
    if not isinstance (value, str):
        value = str(value)
        
    if "-" in value:
        newval = value.split("-")[1]
        prefix="-"
    else:
        newval = value
        prefix=''
        
    num_list = newval.split(".")
    num_list_len = len (num_list)
    if num_list_len > 2 or num_list_len == 0:
        raise NotImplementedError

    if num_list_len == 2:
        #Process the decimal digits
        decimal_len = len(num_list[1])
        if  decimal_len > 2:
            raise RuntimeError, "don't support decimal len %s for number %s" % (decimal_len, value,)
        elif decimal_len == 1:
            num_list[1] += '0'
    elif num_list_len == 1:
        #Add the decimal digits
        num_list.append('00')

    #now add the commas
    digit_list = list(num_list[0])
    digit_list_len = len(digit_list)
    num_commas = (digit_list_len/2) - 1
    for i in range(num_commas):
        place = ((2*i)+1+digit_list_len%2)+i
        digit_list.insert (place, ',')
    import string
    num_list[0] = ''.join(digit_list)
    return (prefix + num_list[0] + '.' + num_list[1])

@register.filter(name='displayintwithcomma')
def display_int_with_comma(value):
    """
    Converts the input string into a floating point number with commas.
    For example 12 -> 12, 12.1 -> NotImplementedError, 121212 ->1,21,212
    """
    num_list = value.split(".")
    num_list_len = len (num_list)
    if num_list_len != 1:
        raise NotImplementedError, "input number is %s" % value

    #now add the commas
    digit_list = list(num_list[0])
    digit_list_len = len(digit_list)
 
    num_commas = (digit_list_len/2) - 1
    for i in range(num_commas):
        place = ((2*i)+1+digit_list_len%2)+i
        digit_list.insert (place, ',')
    import string
    num_list[0] = ''.join(digit_list)
    return (num_list[0])

@register.filter(name='signdata')
def sign_data(value):
    "Returns checked when value matches the argument"
    import it.core.view_utils as view_utils
    if value is None:
        raise RunTimeError, "There is no data to be signed"
    else:
        return view_utils.sign_data(str(value))

@register.filter(name='encryptitem')
def encrypt_item(item):
    "Returns encrypted item"
    import it.core.view_utils as view_utils
    if item is None:
        raise RunTimeError, "There is no data to be signed"
    else:
        return view_utils.encrypt_item(item)
    

@register.filter(name='postsuffixprocess')
def postsuffixprocess (value, arg):
    "This is a dirty method. Should be removed a more elegant way to integrate post suffix into data aggregate Edit Delete buttons shouldbe discovered"
    if value is None  or value=='': ##ma added value=='' and returning '' in this case
        return '' #None:
    else:
        return (value.split("/")[0] + arg)


@register.filter(name='truncate')
def truncate (value, arg):
    "Truncate a string to specified length. To make it user friendly a string will be apppended with ... so that the user know thatit has been truncated. For example 'this is a test' could be truncated to 'this is a...' or 'this is a t..' "
    intarg = int(arg)
    if value is None:
        return None
    if (len (value) <= intarg):
        return value 
    else:
        return (value[0:intarg] + "...")

@register.filter(name='nonesubstitute')
def nonesubstitute (value, arg):
    "If value is none than substitute by arg"
    if value is None or value == '':
        return arg
    else:
        return value
    

@register.filter(name='roundoff')
def roundoff (value, arg):
    return value.split(".")[0]

@register.filter(name='moonescape')
def moonescape(value):
    " django escape returns None string if the value is None. It should instead return and empty string"
    from django.utils.html import escape    
    if value == None:
        return ""
    else:
        return (escape (value))

@register.filter(name='rightalign')
def rightalign(value):
    "Right align a string"
    total_space = 15
    value_len = len(value)
    new_value = []
    
    if value_len < total_space:
        for i in range (total_space-value_len):
            new_value.append(' ')
        return (''.join(new_value) + value)
    else:
        return value

@register.filter(name='keyvalue')
def keyvalue(dict, key):    
    return dict[key]
