
class GenerateTable(object):

    def __init__(self):

        # 경로 수정 ------------------------------------------------------------
        table_path = 'C:\\Users\\user\\PycharmProjects\\asrbuilder\\resource'
        # --------------------------------------------------------------------

        self.eng2kor = dict()
        with open(f'{table_path}\\ALPHA2KOR.table', 'r', encoding='utf-8') as f:
            raw_table = f.read().splitlines()

        for i, line in enumerate(raw_table):
            if i == 0:
                continue
            self.eng2kor[line.split('|')[0]] = line.split('|')[1]

        self.num2kor = dict()
        with open(f'{table_path}\\NUM2KOR.table', 'r', encoding='utf-8') as f:
            raw_table = f.read().splitlines()

        for i, line in enumerate(raw_table):
            if i == 0:
                continue
            self.num2kor[line.split('|')[0]] = {'gisu': line.split('|')[1],         # 일
                                                'seosu': line.split('|')[2],        # 하나
                                                'seosu-danwi': line.split('|')[3],  # 한
                                                'dial-gong': line.split('|')[4],    # 공일
                                                'dial-young': line.split('|')[5]}   # 영일
