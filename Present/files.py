import glob
import logging
import os
import shutil

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Files(object):

    def __init__(self):
        super(Files, self).__init__()

    @staticmethod
    def touch(target):
        if os.path.exists(target):
            return os.utime(target, None)
        else:
            return open(target, 'a').close()

    @staticmethod
    def rm(target):
        if os.path.isdir(target):
            return shutil.rmtree(target)
        if os.path.isfile(target):
            return os.remove(target)
        if os.path.islink(target):
            return os.unlink(target)

    @staticmethod
    def pwd():
        return os.getcwd()

    def mkdir(self, path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self.mkdir(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)

    def ln(self, source, target):
        if self.exists(target):
            return False
        return os.symlink(source, target)

    def chmod(self, target, mode, recursive=False):

        if recursive:
            for (path, dirs, files) in os.walk(target):
                for dirname in dirs:
                    os.chmod(os.path.join(path, dirname), mode)
                    self.chmod(os.path.join(path, dirname), mode, recursive=True)
                for filename in files:
                    os.chmod(os.path.join(path, filename), mode)
        else:
            os.chmod(target, mode)

    @staticmethod
    def cp(source, target):
        if os.path.isdir(source):
            return shutil.copytree(source, target)
        return shutil.copy(source, target)

    @staticmethod
    def mv(source, target):
        return shutil.move(source, target)

    @staticmethod
    def ls(target):
        return glob.glob(target)

    @staticmethod
    def dirname(target):
        return os.path.dirname(target)

    @staticmethod
    def getparam(target):
        return os.environ.get(target)

    @staticmethod
    def size(target):
        return os.path.getsize(target)

    @staticmethod
    def exists(target):
        return os.path.exists(target)

    @staticmethod
    def get_wavdir_size(root_path):
        """ byte 단위 파일 크기 계산 """
        wav_dir_size = 0.0
        for root, dirs, files in os.walk(root_path):
            if root.split('/')[-1] == 'wav':
                wav_dir_size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return wav_dir_size

    @staticmethod
    def merge(info):
        """ 텍스트 파일 merge """
        with open(info.get('src1'), 'r', encoding='utf-8') as f:
            data1 = f.read().splitlines()
        with open(info.get('src2'), 'r', encoding='utf-8') as f:
            data2 = f.read().splitlines()
        return data1 + data2

    @staticmethod
    def get_chunk(info):
        """ list 타입 chunk 단위로 split 후 리턴 """
        orig_list = info.get('list')
        chunk_size = info.get('chunk-size')
        chunks = [orig_list[i:i + chunk_size] for i in range(0, len(orig_list), chunk_size)]
        return chunks

    @staticmethod
    def isdir(target):
        return os.path.isdir(target)

    @staticmethod
    def match(root_path, target_file):
        """ root_path 기준 target_file 서치 후 경로 리턴 """
        matched_file = list()

        for (path, dirname, files) in os.walk(root_path):
            for f in files:
                if f == target_file:  # for README, PROMPTS, DURINFO etc ..
                    matched_file.append(path + '/' + f)
        return matched_file

    @staticmethod
    def search_dir(root_path):
        """ root_path 하위 디렉토리 검색 """
        searched_list = list()
        for (path, dir, files) in os.walk(root_path):
            searched_list.append('%s/%s' % (path, dir))
        if searched_list:
            return searched_list
        else:
            return False

    @staticmethod
    def search_extension(root_path, extension):
        """ 확장자 기준 파일 검색 """
        searched_list = list()
        for (path, dir, files) in os.walk(root_path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == extension:
                    searched_list.append('%s/%s' % (path, filename))
        if searched_list:
            return searched_list
        else:
            return False
