# tokenizer.py

from kiwipiepy import Kiwi

class KiwiTokenizer:
    def __init__(self, model_type: str = 'sbg', typos: str = None):
        """
        Kiwi 토크나이저 초기화 함수.

        매개변수:
        model_type: Kiwi 모델 타입 ('sbg' 또는 'knlm').
        typos: 오타 수정 옵션 ('basic', 'continual', 'basic_with_continual', None).
        """
        self.kiwi = Kiwi(model_type=model_type, typos=typos)

    def tokenize(self, text: str):
        """
        텍스트를 토큰화하는 함수.

        매개변수:
        text: 토큰화할 텍스트 문자열.

        반환:
        List[KiwiToken]: 토큰화된 결과 리스트.
        """
        return self.kiwi.tokenize(text)
