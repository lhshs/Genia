# Pokemon Image Similarity
사전학습된 CNN모델을 활용해 Kaggle Pokemon Image Similarity 측정 모델 만들기

## How To
1. repo를 받은 뒤 root 폴더로 경로 설정 후 CLI 환경에서 python main.py를 입력한다.
2. 첫 번째 포켓몬을 입력한다. (enter)
3. 첫 번째 포켓몬과 비교하고 싶은 두 번째 포켓몬을 입력한다. (enter)
4. 유사도를 확인한다.

<br>
최종 실행 후 figure를 끄면 다음 실행이 가능합니다.
<br>최초 실행시 feature_extract에 약 2분정도 소요됩니다.
<br>최초 실행시 생성된 <strong>feature_extraction.pickle</strong> 파일이 root 폴더에 존재한다면, 다음 실행부터 feature extraction 과정 없이 유사도를 볼 수 있습니다.

### Model
- VGG16

### Data
- https://www.kaggle.com/datasets/vishalsubbiah/pokemon-images-and-types
