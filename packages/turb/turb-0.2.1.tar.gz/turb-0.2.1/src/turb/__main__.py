import sys
import os

from turb.f import fuzzy_list_find
from turb.f import fuzzy_dict_key



sample_dict1 = { "foo": "bar", "oo": "Hoi" }
sample_list1 = [ "foo", "oo", "Hoi" ]


print("name test")

x = fuzzy_dict_key(sample_dict1, 'oo')
print(x)
print("-"*80)

x = fuzzy_list_find(sample_list1, 'h')
print(x)
print("-"*80)
