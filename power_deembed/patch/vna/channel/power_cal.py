import numpy as np
from   rohdeschwarz.instruments.vna import Channel

# patch in query_64_bit
import power_deembed.patch.vna.query_64_bit

def get_power_cal(self, wave):
    scpi = "SENS{ch}:CORR:POW:DATA? '{wave}'"
    scpi = scpi.format(ch=self.index, wave=wave)
    return self._vna.query_64_bit(scpi)
Channel.get_power_cal = get_power_cal

def set_power_cal(self, wave, corrections):
    corrections = np.array(corrections, 'float64')
    scpi = "SENS{ch}:CORR:POW:DATA '{wave}',"
    scpi = scpi.format(ch=self.index, wave=wave)

    self._vna.settings.binary_64_bit_data_format = True
    self._vna.write_raw_no_end(bytes(scpi, 'ascii'))
    self._vna.write_64_bit_vector_block_data(corrections)
    self._vna.settings.ascii_data_format = True
Channel.set_power_cal = set_power_cal

def get_cal_freq(self):
    scpi = "SENS{ch}:CORR:STIM?".format(ch=self.index)
    return self._vna.query_64_bit(scpi)
Channel.get_cal_freq = get_cal_freq
Channel.cal_freq_Hz  = property(get_cal_freq)
