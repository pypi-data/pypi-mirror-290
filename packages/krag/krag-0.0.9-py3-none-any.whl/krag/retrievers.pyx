# retrievers.py

from langchain_core.runnables import Runnable
from langchain_community.retrievers import BM25Retriever
from typing import List
from krag.tokenizers import KiwiTokenizer  

class KiWiBM25RetrieverWithScore(Runnable):
    def __init__(self, documents, kiwi_tokenizer: KiwiTokenizer = None, k: int = None, threshold: float = 0.0):
        """
        매개변수:
        documents: 문서 리스트.
        kiwi_tokenizer: Kiwi 토크나이저 모델 객체.
        k: 반환할 최대 문서 수.
        threshold: BM25 점수 임계값.
        """
        self.documents = documents
        self.kiwi_tokenizer = kiwi_tokenizer
        self.k = k if k is not None else 4
        self.threshold = threshold

        # BM25Retriever 초기화
        if self.kiwi_tokenizer is None:
            self.bm25_retriever = BM25Retriever.from_documents(documents=self.documents)
        else:
            self.bm25_retriever = BM25Retriever.from_documents(
                documents=self.documents,
                preprocess_func=self._tokenize
            )

    def _tokenize(self, text: str) -> List[str]:
        """
        한국어 토크나이저를 사용하여 문장을 토큰화하는 함수.
        :param text: 토큰화할 문장.
        :return: 토큰 리스트.
        """
        if self.kiwi_tokenizer is None:
            return text.split()
        else:
            return [t.form for t in self.kiwi_tokenizer.tokenize(text)]

    def _retireve_bm25_with_score(self, query: str) -> List[dict]:
        """
        주어진 쿼리에 대한 문서를 BM25 점수와 함께 검색.

        매개변수:
        query: 검색 쿼리 문자열.

        반환:
        List[dict]: 검색된 문서와 BM25 점수를 포함하는 리스트.
        """
        # 설정된 k 값을 사용하여 문서 검색
        self.bm25_retriever.k = self.k
        retrieved_docs = self.bm25_retriever.invoke(query)

        # 쿼리 토크나이징
        tokenized_query = self._tokenize(query)
        
        # BM25 점수 계산
        doc_scores = self.bm25_retriever.vectorizer.get_scores(tokenized_query)
        doc_scores_sorted = sorted(enumerate(doc_scores), key=lambda x: x[1], reverse=True)

        # 문서에 BM25 점수 추가
        for i, doc in enumerate(retrieved_docs):
            doc.metadata["bm25_score"] = doc_scores_sorted[i][1]
        
        # 스코어가 임계값 이상인 문서만 반환
        return [doc for doc in retrieved_docs if doc.metadata["bm25_score"] > self.threshold]

    def invoke(self, query: str, config=None) -> List[dict]:
        """
        검색 쿼리를 받아 문서를 검색하는 함수.

        매개변수:
        query: 검색 쿼리 문자열.
        config: 추가적인 설정 정보 (옵션).

        반환:
        List[dict]: 검색된 문서와 BM25 점수를 포함하는 리스트.
        """
        return self._retireve_bm25_with_score(query)
    

