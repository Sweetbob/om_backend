from django.test import TestCase

# Create your tests here.
from api.utils.network_util import is_alive

print(is_alive('192.168.163.172'))
print(is_alive('192.168.163.173'))
