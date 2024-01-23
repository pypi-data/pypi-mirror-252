import labbench as lb
from labbench import paramattr as attr


# @attr.kwarg.int('channel', min=1, max=4)
class Device(lb.Device):
    # channel_enable = attr.method.bool(key='channel{channel}:enabled')
    # trigger = attr.method.bool(key='trig:enabled')

    # channel_enable = attr.method.bool()
    # trigger = attr.method.bool()

    @attr.method.bool()
    @attr.method_kwarg.int('channel', min=1, max=4)
    def channel_enable(self, *, channel):
        """get"""
        return (channel==1)

    @channel_enable.setter
    def _(self, new_value, *, channel):
        print('got new value: ', new_value, channel)

    @attr.property.str()
    def single_enable(self):
        """get"""
        return getattr(self, '_single_enable', False)

    @single_enable.setter
    def _(self, new_value):
        self._single_enable = new_value

    # @attr.property.bool()
    # def continuous_triggering(self, new_value=lb.Undefined):
    #     if new_value is lb.Undefined:
    #         return self.query('trig:enabled?')
    #     else:
    #         self.write(f'trig:enabled {new_value}')

if __name__ == '__main__':
    d = Device()
    print(d.channel_enable(channel=1))
    d.channel_enable(False, channel=1)

    print(d.single_enable)
    d.single_enable = True
    print(d.single_enable)
