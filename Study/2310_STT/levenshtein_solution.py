# import numpy


class Levenshtein(object):

    def __init__(self):
        super(Levenshtein, self).__init__()

    @staticmethod
    def editDistance(r, h):
        """
        Levenshtein Distance 구현

        :param r: reference (비교 기준)
        :param h: STT result (비교할 텍스트)
        :return: Levenshtein Distance Matrix (len(r) * len(h))
        """

        # edited --------------------------------------
        # 기존 방법
        # d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint32).reshape((len(r) + 1, len(h) + 1))

        # numpy 패키지 안쓰고 파이썬으로만 짜는 방법
        d = [[0 for j in range(len(h)+1)] for i in range(len(r)+1)]
        # -------------------------------------------

        for i in range(len(r) + 1):
            for j in range(len(h) + 1):
                if i == 0:
                    d[0][j] = j
                elif j == 0:
                    d[i][0] = i
        for i in range(1, len(r) + 1):
            for j in range(1, len(h) + 1):
                if r[i - 1] == h[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    substitute = d[i - 1][j - 1] + 1
                    insert = d[i][j - 1] + 1
                    delete = d[i - 1][j] + 1
                    d[i][j] = min(substitute, insert, delete)

        return d

    @staticmethod
    def getStepList(r, h, d):
        """
        TOT, MAT, INS, DEL, SUB 리스트 출력 함수

        :param r: Reference
        :param h: STT result
        :param d: Levenshtein Distance Matrix
        :return:  Matched info list
        """

        x = len(r)
        y = len(h)

        list = []

        while True:
            print("===============================")
            print(x, y, "-->", d[x][y])
            if x == 0 and y == 0:
                break
            elif d[x][y] == d[x - 1][y - 1] and r[x - 1] == h[y - 1] and x >= 1 and y >= 1:
                print("m")
                list.append("m")
                x = x - 1
                y = y - 1
            elif d[x][y] == d[x][y - 1] + 1 and y >= 1:
                print(f"d[x][y]: {d[x][y]}")
                print(f"d[x][y-1]+1: {d[x][y-1]+1}")
                print("i")
                list.append("i")
                x = x
                y = y - 1
            elif d[x][y] == d[x - 1][y - 1] + 1 and x >= 1 and y >= 1:
                print("s")
                list.append("s")
                x = x - 1
                y = y - 1
            else:
                print("d")
                list.append("d")
                x = x - 1
                y = y

        return list[::-1]


def cer(info):

    r_sent = info.get('ref')
    h_sent = info.get('hyp')

    r = list(''.join(r_sent.split()))
    h = list(''.join(h_sent.split()))

    levenshtein = Levenshtein()

    d = levenshtein.editDistance(r, h)

    print(d)

    if len(r) != 0:
        cer_rate = float(d[len(r)][len(h)]) / len(r) * 100
    else:
        cer_rate = float('inf')

    match_list = levenshtein.getStepList(r, h, d)

    num_total = len(r)
    num_mat = len([item for item in match_list if item == 'm'])
    num_sub = len([item for item in match_list if item == 's'])
    num_del = len([item for item in match_list if item == 'd'])
    num_ins = len([item for item in match_list if item == 'i'])

    cer_info = {'cer': cer_rate, 'tot': num_total,
                'mat': num_mat, 'sub': num_sub,
                'del': num_del, 'ins': num_ins,
                'list': match_list}

    return cer_info


if __name__ == '__main__':

    refer = '안녕하세요 만나서 반갑습니다'  # 전사 결과
    hyper = '안녕하세요오 만나 반갑습니당'  # STT 결과

    refer = 'delete'  # 전사 결과
    hyper = 'delegate'  # STT 결과

    refer = '서랑함다'
    hyper = '사랑합니다'

    refer = '나는너를좋아해'
    hyper = '너는나좋아하니'

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
