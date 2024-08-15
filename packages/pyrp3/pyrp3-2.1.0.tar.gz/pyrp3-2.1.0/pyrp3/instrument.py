from math import ceil, log

import numpy as np

from .enum import Enum
from .memory import MemoryInterface


class UnsignedInteger:
    def __init__(self, size):
        self.size = size

    def to_python(self, val):
        if not 0 <= val < (1 << self.size):
            raise ValueError("Input value %s exceeds %s-bit limit" % (val, self.size))
        return int(val & ((1 << self.size) - 1))

    def to_binary(self, val):
        if not 0 <= val < (1 << self.size):
            raise ValueError("Input value %s exceeds %s-bit limit" % (val, self.size))
        return val & ((1 << self.size) - 1)


class SignedInteger:
    def __init__(self, size):
        self.size = size

    def to_python(self, val):
        val &= (1 << self.size) - 1
        if val >= (1 << (self.size - 1)):
            val -= 1 << self.size
        if not -(1 << (self.size - 1)) <= val < (1 << (self.size - 1)):
            raise ValueError(
                "Input value %s exceeds %s-bit signed limit" % (val, self.size)
            )
        return int(val)

    def to_binary(self, val):
        if not -(1 << (self.size - 1)) <= val < (1 << self.size):
            raise ValueError(
                "Input value %s exceeds %s-bit signed limit" % (val, self.size)
            )
        if val < 0:
            val += 1 << self.size
        return val & ((1 << self.size) - 1)


class EnumTypeWrapper(UnsignedInteger):
    def __init__(self, enum_type):
        self._enum_type = enum_type
        size = int(ceil(log(16, 2)))
        super(EnumTypeWrapper, self).__init__(size=size)

    def to_python(self, val):
        raw = super(EnumTypeWrapper, self).to_python(val)
        return self._enum_type(raw)

    def to_binary(self, val):
        return super(EnumTypeWrapper, self).to_binary(int(val))


class Temperature(UnsignedInteger):
    """Convert the XADC temperature to degrees"""

    def __init__(self):
        super(Temperature, self).__init__(size=12)

    def to_python(self, val):
        raw = super(Temperature, self).to_python(val)
        return raw * 503.975 / float(0xFFF) - 273.15


class XADC(UnsignedInteger):
    """Convert the XADC output 12bits to volts (0-3.5V)"""

    def __init__(self):
        super(XADC, self).__init__(size=12)

    def to_python(self, val):
        return super(XADC, self).to_python(val) / float(2**self.size) * 3.5


class PWMDAC(UnsignedInteger):
    """Convert volts (0-1.8V) to binary for the PWMDAC"""

    def __init__(self):
        super(PWMDAC, self).__init__(size=32)

    def to_binary(self, val):
        #        """
        #        PWM value (100% == 156)
        #        Bit select for PWM repetition which have value PWM+1
        #        """
        val = val / 1.8
        assert val >= 0
        assert val <= 1
        tmp = np.longlong(np.round(val * (17 * 157 - 1)))
        high = tmp // 17
        low = (1 << (tmp % 17)) - 1
        return (high << 16) | low


class RegisterProperty:
    def __init__(self, addr, register_type, size=None):
        if isinstance(register_type, type) and issubclass(register_type, Enum):
            register_type = EnumTypeWrapper(register_type)
        self.register_type = register_type
        self.addr = addr
        self.size = size

    def __get__(self, instance, owner):
        if instance is None:
            return self
        raise "Cannot get property at addr {obj.addr}.".format(obj=self)


class GetRegister(RegisterProperty):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        out = instance.read(self.addr)
        return self.register_type.to_python(out)


class SetRegister(RegisterProperty):
    def __set__(self, instance, value):
        return instance.write(self.addr, self.register_type.to_binary(value))


class GetSetRegister(SetRegister, GetRegister):
    pass


class GetSetBit:
    def __init__(self, addr, pos, bit_type=None):
        self._bit_type = bit_type
        self.addr = addr
        self.pos = pos

    def __get__(self, instance, owner):
        if instance is None:
            return self
        out = instance.read(self.addr)
        val = (out >> self.pos) & 1
        return (
            bool(val) if self._bit_type is None else self._bit_type.to_python(bool(val))
        )

    def __set__(self, instance, value):
        current = instance.read(self.addr)
        new_value = current & ~(1 << self.pos) | ((value & 1) << self.pos)
        return instance.write(self.addr, int(new_value))


class HK(MemoryInterface):
    def __init__(self, addr_base=0x40000000, **kwd):
        kwd["addr_base"] = addr_base
        super(HK, self).__init__(**kwd)

    id = GetRegister(0x0, UnsignedInteger(size=4))
    dna_part1 = GetRegister(0x4, UnsignedInteger(size=32))
    dna_part2 = GetRegister(0x8, UnsignedInteger(size=32))

    expansion_connector_direction_P = GetSetRegister(0x10, UnsignedInteger(size=8))
    expansion_connector_direction_N = GetSetRegister(0x14, UnsignedInteger(size=8))

    expansion_connector_output_P = GetSetRegister(0x18, UnsignedInteger(size=8))
    expansion_connector_output_N = GetSetRegister(0x1C, UnsignedInteger(size=8))

    expansion_connector_input_P = GetSetRegister(0x20, UnsignedInteger(size=8))
    expansion_connector_input_N = GetSetRegister(0x24, UnsignedInteger(size=8))

    led = GetSetRegister(0x30, UnsignedInteger(size=8))


class AMS(MemoryInterface):
    ADC_FULL_RANGE_CNT = 0xFFF

    def __init__(self, addr_base=0x40400000, **kwd):
        kwd["addr_base"] = addr_base
        super(AMS, self).__init__(**kwd)

    temp = GetRegister(addr=0x30, register_type=Temperature())

    aif0 = GetRegister(addr=0x0, register_type=XADC())
    aif1 = GetRegister(addr=0x4, register_type=XADC())
    aif2 = GetRegister(addr=0x8, register_type=XADC())
    aif3 = GetRegister(addr=0xC, register_type=XADC())
    aif4 = GetRegister(addr=0x10, register_type=XADC())

    dac0 = SetRegister(0x20, register_type=PWMDAC())
    dac1 = SetRegister(0x24, register_type=PWMDAC())
    dac2 = SetRegister(0x28, register_type=PWMDAC())
    dac3 = SetRegister(0x2C, register_type=PWMDAC())

    vccpint = GetRegister(addr=0x34, register_type=XADC())
    vccpaux = GetRegister(addr=0x38, register_type=XADC())
    vccbram = GetRegister(addr=0x3C, register_type=XADC())
    vccint = GetRegister(addr=0x40, register_type=XADC())
    vccaux = GetRegister(addr=0x44, register_type=XADC())
    vccddr = GetRegister(addr=0x48, register_type=XADC())


class TriggerSource(Enum):
    none = 0
    immediately = 1
    cha_posedge = 2
    cha_negedge = 3
    chb_posedge = 4
    chb_negedge = 5
    ext_posedge = 6
    ext_negedge = 7
    awg_posedge = 8
    awg_negedge = 9


class Decimation(UnsignedInteger):
    def __init__(self):
        super(Decimation, self).__init__(size=32)

    def to_binary(self, val):
        return super(Decimation, self).to_binary(val)


class Scope(MemoryInterface):
    data_length = 2**14

    def __init__(self, addr_base=0x40100000, channel="A", **kwd):
        kwd["addr_base"] = addr_base
        super(Scope, self).__init__(**kwd)

    writestate_machine_bit = GetSetBit(addr=0x0, pos=1)
    trigger_bit = GetSetBit(addr=0x0, pos=0)

    def reset_writestate_machine(self, v=True):
        self.writestate_machine_bit = v

    def arm_trigger(self, v=True):
        self.trigger_bit = v

    trigger_source = GetSetRegister(0x4, TriggerSource())
    threshold_ch1 = GetSetRegister(0x8, SignedInteger(size=14))
    threshold_ch2 = GetSetRegister(0xC, SignedInteger(size=14))
    trigger_delay = GetSetRegister(0x10, UnsignedInteger(size=32))
    data_decimation = GetSetRegister(0x14, Decimation())
    write_pointer_current = GetRegister(0x18, UnsignedInteger(size=14))
    write_pointer_trigger = GetRegister(0x1C, UnsignedInteger(size=14))
    hysteresis_ch1 = GetSetRegister(0x20, SignedInteger(size=14))
    hysteresis_ch2 = GetSetRegister(0x24, SignedInteger(size=14))
    average = GetSetBit(addr=0x28, pos=0)
    # equalization filter not implemented here
    dac2_on_ch1 = GetSetBit(0x50, pos=0)
    dac1_on_ch2 = GetSetBit(0x50, pos=1)

    # Function specific to read the array of data
    def get_rawdata(self, addr):
        x = self.reads(addr, self.data_length)
        y = x.copy()
        y.dtype = np.int32
        y[y > 2**13] -= 2**14
        return y

    @property
    def rawdata_ch1(self):
        return self.get_rawdata(0x10000)

    @property
    def rawdata_ch2(self):
        return self.get_rawdata(0x20000)

    @property
    def data_ch1(self):
        return np.roll(self.rawdata_ch1, -int(self.write_pointer_trigger))

    @property
    def data_ch2(self):
        return np.roll(self.rawdata_ch2, -int(self.write_pointer_trigger))

    # helpers
    @property
    def times(self):
        return np.linspace(
            0.0,
            8e-9 * self.data_decimation * float(self.data_length),
            self.data_length,
            endpoint=False,
        )

    def setup(self, frequency=1, trigger_source=TriggerSource.immediately):
        self.reset_writestate_machine(v=True)
        self.trigger_delay = self.data_length
        self.dac1_on_ch2 = False
        self.dac2_on_ch1 = False
        self.arm_trigger(v=False)
        self.average = True
        self.frequency = frequency
        self.trigger_source = trigger_source
        self.reset_writestate_machine(v=False)
        self.arm_trigger()

    def rearm(self, frequency=None, trigger_source=8):
        if frequency is not None:
            self.frequency = frequency
        self.trigger_delay = self.data_length
        self.trigger_source = trigger_source
        self.arm_trigger()

    @property
    def frequency(self):
        return 1.0 / float(self.data_decimation) / float(self.data_length) / 8e-9

    @frequency.setter
    def frequency(self, v):
        fbase = 125e6 / float(2**14)
        factors = [1, 8, 64, 1024, 8192, 65536, 65537]
        for f in factors:
            if v > fbase / float(f):
                self.data_decimation = f
                break
            if f == 65537:
                self.data_decimation = 65536
                print("Frequency too low: Impossible to sample the entire waveform")


class ASG(MemoryInterface):
    data_length = 2**14

    def __init__(self, addr_base=0x40200000, channel="A", **kwd):
        kwd["addr_base"] = addr_base
        super(ASG, self).__init__(**kwd)
        if channel == "B":
            self.data_offset = 0x20000
            self.value_offset = 0x20
            self.bit_offset = 16
        else:  # this includes channel A
            self.data_offset = 0x10000
            self.value_offset = 0x00
            self.bit_offset = 0

    @property
    def output_zero(self):
        return self.bitstate(0x0, self.bit_offset + 7)

    @output_zero.setter
    def output_zero(self, v):
        self.changebit(0x0, self.bit_offset + 7, v)

    @property
    def sm_reset(self):
        return self.bitstate(0x0, self.bit_offset + 6)

    @sm_reset.setter
    def sm_reset(self, v):
        self.changebit(0x0, self.bit_offset + 6, v)

    @property
    def sm_onetimetrigger(self):
        return self.bitstate(0x0, self.bit_offset + 5)

    @sm_onetimetrigger.setter
    def sm_onetimetrigger(self, v):
        self.changebit(0x0, self.bit_offset + 5, v)

    @property
    def sm_wrappointer(self):
        return self.bitstate(0x0, self.bit_offset + 4)

    @sm_wrappointer.setter
    def sm_wrappointer(self, v):
        self.changebit(0x0, self.bit_offset + 4, v)

    @property
    def trig_selector(self):
        """
        1-trig immediately
        2-external trigger positive edge - DIO0_P pin
        3-external trigger negative edge
        """
        v = self.read(0x0)
        return (v >> (self.bit_offset)) & 0x0F

    @trig_selector.setter
    def trig_selector(self, v):
        v = v & 0xF
        v = (self.read(0x0) & (~0x0000000F)) | v
        self.write(0x0, v)

    @property
    def offset(self):
        v = self.read(self.value_offset + 0x4)
        v = (v >> 16) & 0x00003FFF
        if v & 2**13:
            v = v - 2**14
        return int(v)

    @offset.setter
    def offset(self, v):
        v = self.from_pyint(v, 14) * 2**16 + self.scale
        self.write(self.value_offset + 0x4, v)

    @property
    def scale(self):
        """
        Amplitude scale. 0x2000 == multiply by 1. Unsigned
        """
        v = self.read(self.value_offset + 0x4)
        v = v & 0x00003FFF
        return int(v)

    @scale.setter
    def scale(self, v):
        if v >= 2**14:
            v = 2**14 - 1
        if v < 0:
            v = 0
        v = int(v) + (self.offset * 2**16)
        self.write(self.value_offset + 0x4, v)

    @property
    def counter_wrap(self):
        """
        typically this value is set to
        2**16*(2**14-1)
        in order to exploit the full data buffer
        """
        v = self.read(self.value_offset + 0x8)
        return v & 0x3FFFFFFF

    @counter_wrap.setter
    def counter_wrap(self, v):
        v = v & 0x3FFFFFFF
        self.write(self.value_offset + 0x8, v)

    @property
    def counter_step(self):
        """
        Each clock cycle the counter_step is increases the internal counter modulo
        counter_wrap. The current counter step rightshifted by 16 bits is the index of
        the value that is chosen from the data table.
        """
        v = self.read(self.value_offset + 0x10)
        return v & 0x3FFFFFFF

    @counter_step.setter
    def counter_step(self, v):
        v = v & 0x3FFFFFFF
        self.write(self.value_offset + 0x10, v)

    @property
    def start_offset(self):
        """counter offset for trigged events = phase offset"""
        v = self.read(self.value_offset + 0x0C)
        return v & 0x3FFFFFFF

    @start_offset.setter
    def start_offset(self, v):
        v = v & 0x3FFFFFFF
        self.write(self.value_offset + 0x0C, v)

    @property
    def full_timescale(self):
        """not sure if there is an offset for counter_wrap, need to check code"""
        return 8e-9 * float(self.counter_wrap + 2**16) / float(self.counter_step)

    @property
    def max_index(self):
        return self.counter_wrap >> 16

    @property
    def data(self):
        return np.array(
            [self.to_pyint(v) for v in self.reads(self.data_offset, self.data_length)]
        )

    @data.setter
    def data(self, data):
        data = [self.from_pyint(v) for v in data]
        self.writes(self.data_offset, data)

    @property
    def lastpoint(self):
        """
        The last point before the output jumps back to the zero/wrapped index value.
        """
        return self.counter_wrap / self.counter_step

    @property
    def frequency(self):
        return float(self.counter_step) / float(self.counter_wrap + 2**16) / 8e-9

    @frequency.setter
    def frequency(self, v):
        self.counter_step = np.long(
            np.round(float(v) * 8e-9 * (float(self.counter_wrap + 2**16)))
        )

    def setup(self, frequency=1):
        # corresponds to 2Vpp sine
        self.output_zero = True
        self.sm_reset = True
        self.trig_selector = 0
        self.scale = 2**13
        self.offset = 0

        self.d = np.zeros(2**14, dtype=np.long)
        for i in range(len(self.d)):
            self.d[i] = np.long(
                np.round(-(2**13 - 1) * np.cos((float(i) / 2**14) * 2 * np.pi))
            )
        self.data = self.d

        self.start_offset = 0
        self.counter_wrap = 2**16 * (2**14 - 1)
        self.frequency = frequency

        self.sm_onetimetrigger = True
        self.sm_wrappointer = False
        self.output_zero = False
        self.sm_reset = False

    def trig(self, frequency=None):
        if frequency is not None:
            self.frequency = frequency
        self.start_offset = 0
        self.trig_selector = 1
        self.trig_selector = 0


class Pid(MemoryInterface):
    def __init__(self, addr_base=0x40300000, number="11", **kwd):
        kwd["addr_base"] = addr_base
        super(Pid, self).__init__(**kwd)
        if number == "11":
            self.pidnumber = 0
        elif number == "12":
            self.pidnumber = 1
        elif number == "21":
            self.pidnumber = 2
        elif number == "22":
            self.pidnumber = 3

    @property
    def reset(self):
        v = self.read(0x0)
        return (v >> self.pidnumber) & 0x1 != 0

    @reset.setter
    def reset(self, val):
        self.changebit(0x0, self.pidnumber, val)

    @property
    def setpoint(self):
        v = self.read(self.pidnumber * 0x10 + 0x10)
        return self.to_pyint(v, bitlength=14)

    @setpoint.setter
    def setpoint(self, val):
        self.write(self.pidnumber * 0x10 + 0x10, self.from_pyint(val, bitlength=14))

    @property
    def proportional(self):
        v = self.read(self.pidnumber * 0x10 + 0x14)
        return self.to_pyint(v, bitlength=14)

    @proportional.setter
    def proportional(self, val):
        self.write(self.pidnumber * 0x10 + 0x14, self.from_pyint(val, bitlength=14))

    @property
    def integral(self):
        v = self.read(self.pidnumber * 0x10 + 0x18)
        return self.to_pyint(v, bitlength=14)

    @integral.setter
    def integral(self, val):
        self.write(self.pidnumber * 0x10 + 0x18, self.from_pyint(val, bitlength=14))

    @property
    def derivative(self):
        v = self.read(self.pidnumber * 0x10 + 0x1C)
        return self.to_pyint(v, bitlength=14)

    @derivative.setter
    def derivative(self, val):
        self.write(self.pidnumber * 0x10 + 0x1C, self.from_pyint(val, bitlength=14))

    def initialize(self, setpoint=None, integral=0, proportional=0, derivative=0):
        self.reset = True
        if setpoint is not None:
            self.setpoint = setpoint
        self.integral = integral
        self.proportional = proportional
        self.derivative = derivative
        self.reset = False


class InterfaceDescriptor:
    def __init__(self, cls, **kwd):
        self._cls = cls
        self.kwd = kwd

    def __get__(self, instance, owner):
        if instance is None:
            return self._cls
        return self._cls(parent_memory=instance, **self.kwd)


class RedPitaya:
    hk = InterfaceDescriptor(HK)
    ams = InterfaceDescriptor(AMS)
    scope = InterfaceDescriptor(Scope)
    pid11 = InterfaceDescriptor(Pid, number="11")
    pid12 = InterfaceDescriptor(Pid, number="12")
    pid21 = InterfaceDescriptor(Pid, number="21")
    pid22 = InterfaceDescriptor(Pid, number="22")
    asga = InterfaceDescriptor(ASG, channel="A")
    asgb = InterfaceDescriptor(ASG, channel="B")


if __name__ == "__main__":
    from time import sleep, time

    red_pitaya = RedPitaya()
    red_pitaya.scope.arm_trigger()
    red_pitaya.scope.trigger_source = 1
    sleep(1)
    t0 = time()
    red_pitaya.scope.data_ch1
    print(time() - t0)
