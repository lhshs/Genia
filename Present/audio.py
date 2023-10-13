import logging
import numpy
import scipy.io.wavfile as wav
from scipy.interpolate import interp1d

import src.lib.common as common_lib

from src.lib.util.files import Files


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Audio(object):

    def __init__(self):
        super(Audio, self).__init__()

    @staticmethod
    def pcm2wav(pcm_path, wav_path, sampling_rate):
        pcm_data_array = numpy.fromfile(pcm_path, dtype='int16')
        wav.write(wav_path, sampling_rate, pcm_data_array.astype(dtype='int16'))

    @staticmethod
    def data2wav(data_array, wav_path, sampling_rate):
        wav.write(wav_path, sampling_rate, data_array.astype(dtype='int16'))

    @staticmethod
    def read(file_path, option):

        if option == 'wav':
            try:
                return wav.read(file_path)
            except Exception as e:
                logger.warning("Unable to read wav : {file} {error}".
                               format(file=file_path, error=str(e)))
                return False, False
        else:
            return None, numpy.fromfile(file_path, dtype='int16')

    @staticmethod
    def wav2pcm(wav_path, pcm_path):
        wav_data = numpy.fromfile(wav_path, dtype='int16')[22:]
        wav_data.astype('int16').tofile(pcm_path)

    @staticmethod
    def data2pcm(wav_data, pcm_path):
        wav_data.astype('int16').tofile(pcm_path)

    @staticmethod
    def resample(info):
        import math

        data = info.get('data')
        sampling = float(info.get('sample'))
        resampling = float(info.get('resample'))
        index = numpy.linspace(0, len(data) - 1, len(data))
        new_length = math.ceil(len(data) * resampling / sampling)
        resample_index = numpy.linspace(0, len(data) - 1, new_length)
        resample_data = interp1d(index, data, kind='cubic')(resample_index)

        return resample_data.astype(dtype='int16')

    @staticmethod
    def vox2wav(info):
        command = 'sox -t ul {src} -b 16 -t wav -s -'.format(src=info.get('src'))
        raw_data = common_lib.get_command_stdout(command)
        with open(info.get('dst'), 'w') as f:
            f.write(raw_data)

    @staticmethod
    def mp2wav(info):
        command = 'sox {src} -r 16000 -c 1 -b 16 -s -t wav -'.format(src=info.get('src'))
        raw_data = common_lib.get_command_stdout(command)
        with open(info.get('dst'), 'w') as f:
            f.write(raw_data)

    @staticmethod
    def sox_resample(info):
        command = 'sox {src} -r {sampling} -c 1 -b 16 -e signed-integer -t wav {dst}'.format(src=info.get('src'),
                        sampling=info.get('sampling'), dst=info.get('dst'))
        raw_data = common_lib.execute_command(command)

    def al2wav(self, info):
        utils = Files()
        audio_file = info.get('src')
        convert_audio_file = audio_file

        if audio_file.split('.')[-1] != 'al':
            temp_audio_file = audio_file + '.temp.al'
            utils.mv(audio_file, temp_audio_file)
            convert_audio_file = temp_audio_file

        dst_file = info.get('dst')
        rate = info.get('rate')
        channel = info.get('channel')
        command = 'sox -r {rate} -c {channel} {src} -b 16 -t wav -'.format(rate=rate,
                                                                           channel=channel,
                                                                           src=convert_audio_file)
        raw_data = common_lib.get_command_stdout(command)
        with open(dst_file, 'w') as f:
            f.write(raw_data)

        if utils.exists(convert_audio_file):
            utils.rm(convert_audio_file)

        sampling, data_list = self.read(dst_file, 'wav')

        if sampling is False:
            utils.rm(dst_file)

    def ul2wav(self, info):
        utils = Files()
        audio_file = info.get('src')
        convert_audio_file = audio_file

        if audio_file.split('.')[-1] != 'ul':
            temp_audio_file = audio_file + '.temp.ul'
            utils.mv(audio_file, temp_audio_file)
            convert_audio_file = temp_audio_file

        dst_file = info.get('dst')
        rate = info.get('rate')
        channel = info.get('channel')
        command = 'sox -r {rate} -c {channel} {src} -b 16 -t wav -'.format(rate=rate,
                                                                           channel=channel,
                                                                           src=convert_audio_file)
        raw_data = common_lib.get_command_stdout(command)
        with open(dst_file, 'w') as f:
            f.write(raw_data)

        if utils.exists(convert_audio_file):
            utils.rm(convert_audio_file)

        sampling, data_list = self.read(dst_file, 'wav')

        if sampling is False:
            utils.rm(dst_file)

    def append_wav_data(self, wav_item, data_array):
        sampling_rate, audio_data = self.read(wav_item, 'wav')
        data_array = numpy.append(data_array, audio_data)
        return sampling_rate, data_array

    @staticmethod
    def __avg_power(data):
        import math

        value = 0.0

        for item in data:
            value += math.pow(item, 2)
        value = value / len(data)

        return value

    def snr_mix(self, info):

        import math
        import numpy as np

        src_wav = info.get('src')
        noise_wav = info.get('noise')
        dst_wav = info.get('dst')
        snr = info.get('snr')

        param = float(snr) / 10

        s_wav_sampling, s_wav_data = self.read(src_wav, 'wav')
        n_wav_sampling, n_wav_data = self.read(noise_wav, 'wav')

        if s_wav_sampling != n_wav_sampling:
            n_wav_data = self.resample({'data': n_wav_data, 'sample': n_wav_sampling, 'resample': s_wav_sampling})

        avg_o_power = self.__avg_power(s_wav_data)
        avg_n_power = self.__avg_power(n_wav_data)

        factor = avg_n_power / avg_o_power * math.pow(10, param)

        mix_data = list()

        for idx in range(0, len(s_wav_data)):
            mix_data.append(s_wav_data[idx] + n_wav_data[idx % len(n_wav_data)] / factor)

        self.data2wav(np.array(mix_data), dst_wav, s_wav_sampling)

    def snr_data(self, info):
        import math

        base_amp = info.get('base-amp')
        src_wav = info.get('wav')
        snr = info.get('snr')

        if base_amp is None:
            base_amp = 1200

        param = float(snr) / 10

        avg_b_power = math.pow(base_amp, 2)

        n_wav_sampling, n_wav_data = self.read(src_wav, 'wav')

        if len(n_wav_data.shape) == 2:
            logger.warning('channel is not mono ... : {wav}'.format(wav=src_wav))
            return n_wav_sampling, numpy.array([], dtype='int16')

        avg_c_power = self.__avg_power(n_wav_data)
        factor = avg_c_power / avg_b_power * math.pow(10, param)

        return n_wav_sampling, n_wav_data / factor

    @staticmethod
    def get_wav_info(info):
        import re

        wav_id = info.get('wav')
        wav_raw_info = common_lib.get_command_stdout('sox --i {wav}'.format(wav=wav_id))

        file_name_exp = '(Input\s*File\s*:\s*)(.*)'
        channel_exp = '(Channels\s*:\s*)(.*)'
        sampling_exp = '(Sample\s*Rate\s*:\s*)(.*)'
        precision_exp = '(Precision\s*:\s*)(.*)'
        duration_exp = '(Duration\s*:\s*)(.*)'
        encoding_exp = '(Sample\s*Encoding\s*:\s*)(.*)'

        wav_info = {}
        wav_raw_info = ''.join(wav_raw_info.split('\0'))

        for item in wav_raw_info.split('\n'):

            m = re.match(precision_exp, item)
            if m:
                wav_info['bit'] = int(m.group(2).split('-')[0])

            m = re.match(file_name_exp, item)
            if m:
                non_special_name = re.sub('[\'\"]', '', m.group(2))
                wav_info['wav'] = non_special_name.split('/')[-1]

            m = re.match(channel_exp, item)
            if m:
                wav_info['channel'] = int(m.group(2))

            m = re.match(sampling_exp, item)
            if m:
                wav_info['sampling'] = int(m.group(2))

            m = re.match(duration_exp, item)
            if m:
                samples = m.group(2).split()[2]
                wav_info['samples'] = int(samples)

            m = re.match(encoding_exp, item)
            if m:
                wav_info['encoding'] = m.group(2)

        wav_info['sec'] = float(wav_info.get('samples')) / float(wav_info.get('sampling'))
        return wav_info
