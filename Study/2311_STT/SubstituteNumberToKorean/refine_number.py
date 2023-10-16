import re

# 경로 수정 -------------------------------
from src.lib.tables import GenerateTable
# ---------------------------------------

# 숫자 치환기 짜보기
def refine_num(text):

    table = GenerateTable()  # 숫자 테이블 객체 생성

    if re.findall(r'([0-9]+)(\.?)([0-9]*)', text):  # 숫자 전체 찾는 정규식
        # 찾은 숫자 패턴은 모두 한글로 변환
        for num in re.findall(r'([0-9]+)(\.?)([0-9]*)', text):  # 패턴이 0으로 시작하거나 8자리 이상인경우 --> 다이얼로 읽기
            if int(num[0][0]) == 0 or len(num[0]) >= 8:
                dial_list = list()

                for dial in num[0]:
                    dial_list.append(table.num2kor.get(dial).get('dial-young'))
                text = re.sub(r'([0-9]+)(\.?)([0-9]*)', ''.join(dial_list), text, count=1)

            else:  # 다이얼이 아닌 경우 일반 숫자 혹은 소수
                if table.num2kor.get(num[0]):    # 숫자 부분
                    int_num = table.num2kor.get(num[0]).get('gisu')
                    # print(f"{num[0]} --> {int_num}")

                else:
                    int_num = num[0]

                if num[1]:   # 점이 있으면 소수가 존재한다는 뜻
                    float_num = list()
                    for dial in num[2]:
                        float_num.append(table.num2kor.get(dial).get('dial-young'))
                        # print(f"{dial} --> ")
                        # print(table.num2kor.get(dial).get('dial-young'))
                    float_num = ''.join(float_num)
                    combine_num = int_num + " 점 " + float_num
                else:
                    combine_num = int_num
                text = re.sub(r'([0-9]+)(\.?)([0-9]*)', combine_num, text, count=1)

    return text


if __name__ == '__main__':

    # 숫자 치환기

    text1 = "파이는 3.141592 이고, 마라톤 거리는 42.195 킬로미터 입니다"  # 삼 점 일사일오구이
    text2 = "2023년 3월 7일은 화요일입니다"                              # 이천이십삼년 삼월 칠일
    text3 = "이 제품의 코드 번호는 003948 입니다"   # 영영삼구사팔

    for text in [text1, text2, text3]:
        print("-----------")
        print(f"before : {text}")
        print(f"after : {refine_num(text)}")
