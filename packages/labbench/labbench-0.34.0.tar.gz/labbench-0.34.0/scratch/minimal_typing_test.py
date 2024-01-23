from typing import reveal_type

import labbench as lb
from labbench import paramattr as attr


class TestDevice(lb.VISADevice):
    bare_keyed = attr.method.str(key='bare_keyed')
    value: int = attr.value.int()

    @attr.method.str(key=None)
    def bare_decorated(self, new_value=lb.Undefined, *, channel):
        return 'hi'


d = TestDevice()


print(d.bare_decorated(channel=4))
d.bare_keyed()
d.bare_decorated()
reveal_type(d.bare_keyed)
reveal_type(d.bare_decorated)
