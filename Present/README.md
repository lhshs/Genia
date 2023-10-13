# files.py / audio.py 🎁
나만의 유틸리티 보따리 만들기

{내프로젝트}/utils/file.py      (파일 관련 유틸리티)
{내프로젝트}/utils/audio.py (음성 관련 유틸리티)

파일 복사할때마다
import os
import glob
import shutil
import scipyimport numpy

파일 복사
if os.path.isdir(src):
    shutil.copytree(src, dst)
else:
    shutil.copy(src, dst)

.. 어유 지저분해 py 파일마다 import 하고 써야해

내가 자주 쓰는 유틸 기능들을 클래스로 묶어서 만들어두어요. 
여기에만 저런 모듈들 import 많이 해두고
필요한 곳에서는 내 보따리 파일만 import 해서

from utils.file import Files

utils = Files()

utils.cp(src, dst)
utils.mv(src, dst)
utils.rm(src)

이렇게 내가 정의한 함수로
깔끔하게 쓸 수 있어요 (class 의 기능을 사용한다기 보단 같은 기능의 유틸을 묶는 보따리로 사용)

여러가지 보따리가 있는데
어디든 유용하게 사용할 수 있는 보따리 선물 🎁

