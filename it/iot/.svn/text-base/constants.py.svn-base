from collections import OrderedDict

POSSIBLE_ACTIONS = (
                         ('REGISTRATION', 'REGISTRATION'),
			 ('LOGIN', 'LOGIN'),
			 ('LOGOUT', 'LOGOUT'),
			 ('ON', 'ON'),
			 ('OFF', 'OFF'),
                   )


'''
CATEGORIES = ["automation", "embedded", "ecommerce", "automobile"]#, "mobility"]

#Devicetypes
EMBEDDED = ["light", "switch", "temperature"]
AUTOMATION = ["visor"]
AUTOMOBILE = ["car"]
#MOBILITY = ["ios", "android"]
ECOMMERCE = [""]
'''

CATEGORIES = ["my_home", "my_office", "my_retail", "my_car", "miscellaneous"]#, "mobility"]

my_home = ["light", "switch", "ac"]
my_office = ["light", "switch", "ac"]
my_car = ["engine", "ac", "light"]
my_retail = ["store"]
miscellaneous = ["visor"]

#If device types are having same names follow category_device name and write a wrapper to return category and device name

light = { 
	  "ON / OFF": "current_state",
          "DIM": "dim",
        }

ac = OrderedDict({
	          "ON / OFF": "current_state",
                  "SET TEMPERATURE": "temperature",
                  "READ CURRENT TEMPERATURE": "",
                  "SWING": "swing_state",
              })

switch = {
	      "ON / OFF": "current_state",
    	 }	


engine = {
	      "ON / OFF": "current_state",
	 }


def clean_categories(request=None):
    categories = []
    for cat in CATEGORIES:
        categories.append(cat.replace('_', ' '))
    return categories


def get_categorywise_devices(category=None):
    if category:
        return eval(category.lower().replace(' ', '_'))
    
    categories_dict = {}
    for cat in CATEGORIES:
        categories_dict[cat] = eval(cat)
    print "categories_dict", categories_dict
    return categories_dict

def get_features(device_type=None):
    if device_type:
        return eval(device_type)
    commands_dict = {}
    print "Im here"
    for cat in CATEGORIES:
        try:
            device_types = eval(cat)
            for device_type in device_types:
                print device_type
                try:
                    commands_dict[device_type] = eval(device_type).keys()
                except:
                    pass # features not defined
        except:
            #define features/commands for different device types
            pass
    return commands_dict


