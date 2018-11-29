from pathlib       import Path
from power_deembed import read_s21
from rohdeschwarz.instruments.vna import Vna

# patch rohdeschwarz vna
import power_deembed.patch.vna.channel.power_cal

root_path = Path(__file__).parent
filename  = str(root_path / 'test' / 'fixtures' / '3 dB attenuator.s2p')

channel = 1
wave    = 'b1'
vna = Vna()
vna.open_tcp()

# offsets
ch = vna.channel(channel)
freq_Hz, offsets_dB      = read_s21(filename)
assert not False in freq_Hz == ch.cal_freq_Hz

# interpolate
# offsets_dB = np.interp(ch.cal_freq_Hz, freq_Hz, offsets_dB)

# deembed, apply
power_cal_dB = ch.get_power_cal(wave) - offsets_dB
ch.set_power_cal(power_cal_dB)
