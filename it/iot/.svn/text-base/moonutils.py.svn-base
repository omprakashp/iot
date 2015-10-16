def it_set_val(object, dict):
    """ This function assigns values to the elements of object, using the
    values as received in the dictionary
    """

    print dict
    for fields in dict:
        if hasattr(object, fields):
            if isinstance(dict[fields], unicode):
                new_txt = ''
                old_txt = dict[fields]
                for i in range(len(old_txt)):
                    if ord(old_txt[i]) < 128:
                        new_txt += old_txt[i]
                dict[fields] = new_txt

            setattr(object, fields, dict[fields])
        else:
            raise NotImplementedError

    ## Do Not Save here....
    return

