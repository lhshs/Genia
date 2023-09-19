FROM python:3.10

# 작업 위치 지정
WORKDIR /workspace

RUN pip install --upgrade pip

# requirements.txt 
COPY requirements.txt . 

RUN pip install -r requirements.txt

# main.py main.py 
# .(left) -> 현재 경로로 설정해 줌으로써, 폴더 내 경로의 모든 파일을 참조한다 
# .(right) -> WORKING DIR로 파일들을 이동시킨다 
COPY . .


# python만 남겨놓으면 살아있음
# main.py 까지 쓰면 container가 올라갔다가 실행된 후 stop 됨 
ENTRYPOINT ["python"]
# ENTRYPOINT ["python", "main.py"]