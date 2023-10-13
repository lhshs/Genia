import numpy as np

class Levenshtein(object):

    def __init__(self):
        super(Levenshtein, self).__init__()

    @staticmethod
    def editDistance(refer, hyper):
        """
        [step1] Levenshtein Distance 구현

        :param refer: reference (비교 기준)
        :param hyper: STT result (비교할 텍스트)
        :return: Levenshtein Distance Matrix (len(r) * len(hyper))
        """
        # 구현

        # edited --------------------------------------
        # 기존 방법
        # d = numpy.zeros((len(r) + 1) * (len(hyper) + 1), dtype=numpy.uint32).reshape((len(r) + 1, len(hyper) + 1))

        # numpy 패키지 안쓰고 파이썬으로만 짜는 방법
        distance_matrix = [[0 for j in range(len(hyper)+1)] for i in range(len(refer)+1)]
        # -------------------------------------------

        for i in range(len(refer) + 1):
            for j in range(len(hyper) + 1):
                if i == 0:
                    distance_matrix[0][j] = j
                elif j == 0:
                    distance_matrix[i][0] = i
        for i in range(1, len(refer) + 1):
            for j in range(1, len(hyper) + 1):
                if refer[i - 1] == hyper[j - 1]:
                    distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
                else:
                    substitute = distance_matrix[i - 1][j - 1] + 1
                    insert = distance_matrix[i][j - 1] + 1
                    delete = distance_matrix[i - 1][j] + 1
                    distance_matrix[i][j] = min(substitute, insert, delete)

        return distance_matrix

    @staticmethod
    def getStepList(refer, hyper, distance_matrix):
        """
        [step2] TOT, MAT, INS, DEL, SUB 리스트 출력 함수

        :param refer: Reference
        :param hyper: STT result
        :param distance_matrix: Levenshtein Distance Matrix
        :return:  Matched info list
        """

        # 구현
        match_list = list()

        # (x,y) -> (0,0) 될 때까지 while
        x = len(refer)
        y = len(hyper)

        # match, insert, delete, substitution
        while True:
            print("===============================")
            print(x, y, "-->", distance_matrix[x][y])
            if x == 0 and y == 0:
                break
            elif distance_matrix[x][y] == distance_matrix[x - 1][y - 1] and refer[x - 1] == hyper[y - 1] and x >= 1 and y >= 1:
                print("m")
                match_list.append("m")
                x = x - 1
                y = y - 1
            elif distance_matrix[x][y] == distance_matrix[x][y - 1] + 1 and y >= 1:
                print(f"d[x][y]: {distance_matrix[x][y]}")
                print(f"d[x][y-1]+1: {distance_matrix[x][y-1]+1}")
                print("i")
                match_list.append("i")
                x = x
                y = y - 1
            elif distance_matrix[x][y] == distance_matrix[x - 1][y - 1] + 1 and x >= 1 and y >= 1:
                print("s")
                match_list.append("s")
                x = x - 1
                y = y - 1
            else:
                print("d")
                match_list.append("d")
                x = x - 1
                y = y

        return match_list[::-1]


def cer(info):
    """
    [step3] 음절 인식 결과 정보 리턴 함수

    :param r: Reference
    :param hyper: STT result
    :param d: Levenshtein Distance Matrix
    :return:  Matched info list
    """

    r_sent = info.get('ref')
    h_sent = info.get('hyp')

    # 구현
    levenshtein = Levenshtein()

    distance_matrix = levenshtein.editDistance(refer, hyper)
    match_list = levenshtein.getStepList(refer, hyper, distance_matrix)

    if len(refer) != 0:
        cer_rate = float(distance_matrix[len(refer)][len(hyper)]) / len(refer) * 100
    else:
        cer_rate = float('inf')

    num_total = len(match_list)
    num_mat = match_list.count('m')
    num_sub = match_list.count('s')
    num_del = match_list.count('d')
    num_ins = match_list.count('i')

    # 리턴 예시
    cer_info = {'cer': cer_rate, 'tot': num_total,
                'mat': num_mat, 'sub': num_sub,
                'del': num_del, 'ins': num_ins,
                'list': match_list}

    return cer_info


if __name__ == '__main__':

    refer = '안녕하세요 만나서 반갑습니다'  # 발성 내용
    hyper = '안녕하세요오 만나 반갑습니당'  # 인식 결과

    refer = '사랑합니다'     # 발성 내용
    hyper = '서랑함다'      # 인식 결과

    refer = '나는너를좋아해'  # 발성 내용
    hyper = '너는나좋아하니'  # 인식 결과

    sentence_info = {'ref': refer, 'hyp': hyper}
    cer_info = cer(sentence_info)

    print('refer : %s' % refer)
    print('hyper : %s' % hyper)
    print('match list : ', cer_info.get('list'))

    # Edit --------------------------------------
    cer_rate = 100 - cer_info.get('cer')
    print('cer : %f' % cer_rate if cer_rate > 0 else 0.0)  # 인식률 (Character Error Rate)
    # -------------------------------------------

    print('tot : %d' % cer_info.get('tot'))  # 전체 음절 수
    print('mat : %d' % cer_info.get('mat'))  # 매치 음절 수
    print('sub : %d' % cer_info.get('sub'))  # 교체 에러 수
    print('ins : %d' % cer_info.get('ins'))  # 삽입 에러 수
    print('del : %d' % cer_info.get('del'))  # 삭제 에러 수
