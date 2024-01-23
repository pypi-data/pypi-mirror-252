# %%
import pyvisa

import labbench as lb

rm = pyvisa.ResourceManager('sim.yml@sim')
lb.visa_default_resource_manager('sim.yml@sim')

# %%
with rm.open_resource('USB::0x1111::0x2222::0x1234::INSTR', write_termination='\r\n', read_termination='\n') as device1:
    print('device1 IDN?: ', device1.query('?IDN'))

with lb.VISADevice('USB::0x1111::0x2222::0x1234::INSTR', write_termination='\r\n', read_termination='\n') as device1:
    print('device1 IDN?: ', device1.query('?IDN'))

# %%
with rm.open_resource('USB::0x1111::0x2222::0x3692::INSTR', write_termination='\n', read_termination='\n') as device3:
    ret = device3.query('*IDN?')
    print('device3 *IDN?: ', repr(ret))

with lb.VISADevice('USB::0x1111::0x2222::0x3692::INSTR', write_termination='\n', read_termination='\n') as device3:
    ret = device3.query('*IDN?')
    print('device3 *IDN?: ', repr(ret))

# %% both
with rm.open_resource(
    'USB::0x1111::0x2222::0x1234::INSTR', write_termination='\r\n', read_termination='\n'
) as device1, rm.open_resource(
    'USB::0x1111::0x2222::0x3692::INSTR', write_termination='\n', read_termination='\n'
) as device3:
    print('device1 IDN?: ', repr(device1.query('?IDN')))
    print('device3 *IDN?: ', repr(device3.query('*IDN?')))

with lb.VISADevice(
    'USB::0x1111::0x2222::0x1234::INSTR', write_termination='\r\n', read_termination='\n'
) as device1, lb.VISADevice(
    'USB::0x1111::0x2222::0x3692::INSTR', write_termination='\n', read_termination='\n'
) as device3:
    print('device1 IDN?: ', repr(device1.query('?IDN')))
    print('device3 *IDN?: ', repr(device3.query('*IDN?')))
