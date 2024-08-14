# evaluators.py

from krag.document import KragDocument as Document
from korouge_score import rouge_scorer
from typing import Union, List
import math

# 기본 평가자 클래스 정의
class OfflineRetrievalEvaluators:
    def __init__(self, actual_docs: List[List[Document]], predicted_docs: List[List[Document]], match_method="text"):
        """
        OfflineRetrievalEvaluators 클래스 초기화 메서드

        매개변수:
        - actual_docs: 실제 문서의 리스트. 각 문서는 List[List[Document]] 형태로 전달됩니다.
        - predicted_docs: 예측 문서의 리스트. 각 문서는 List[List[Document]] 형태로 전달됩니다.
        - match_method: 텍스트 매칭 방법 ('text', 'rouge1', 'rouge2', 'rougeL').
        """
        self.actual_docs = actual_docs  # 실제 문서 리스트 저장
        self.predicted_docs = predicted_docs  # 예측 문서 리스트 저장
        self.match_method = match_method  # 매칭 방법 저장

    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        """
        실제 텍스트와 예측 텍스트가 일치하는지 확인하는 메서드.

        매개변수:
        - actual_text: 실제 문서의 텍스트 (str 타입).
        - predicted_text: 예측된 문서의 텍스트 또는 텍스트 리스트 (str 또는 List[str] 타입).

        반환값:
        - 일치 여부를 나타내는 boolean 값.
        """
        # 예측 텍스트가 리스트인 경우, 리스트 내 텍스트 중 하나라도 실제 텍스트와 일치하면 True 반환
        if isinstance(predicted_text, list):
            return any(actual_text in text for text in predicted_text)
        
        # 예측 텍스트가 단일 문자열인 경우, 단순히 텍스트가 일치하는지 확인
        return actual_text in predicted_text

    # Hit Rate 계산
    def calculate_hit_rate(self, k: int = None) -> float:
        """
        Hit Rate를 계산하는 메서드.
        
        실제 문서 리스트와 예측 문서 리스트에서 각 쿼리의 모든 실제 문서가 상위 k개의 예측 문서와 일치하는 경우에만 1로 계산합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - Hit Rate 값 (float).
        """
        total_queries = len(self.actual_docs)  # 전체 쿼리 수를 저장할 변수
        full_matches = 0  # 완전 일치한 쿼리의 수를 저장할 변수
        
        # 실제 문서 리스트와 예측 문서 리스트를 반복
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
            predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs]
            
            # 모든 실제 문서가 예측 문서 리스트에 포함되는지 확인
            if all(self.text_match(actual_doc.page_content, predicted_texts) for actual_doc in actual_docs):
                full_matches += 1  # 모든 문서가 일치하면 완전 일치 수 증가
        
        # 완전 일치한 쿼리 수를 전체 쿼리 수로 나누어 Hit Rate 계산
        return full_matches / total_queries if total_queries > 0 else 0.0

    # MRR 계산
    def calculate_mrr(self, k: int = None) -> float:
        """
        MRR (Mean Reciprocal Rank)를 계산하는 메서드.
        
        첫 번째로 일치한 문서의 순위를 바탕으로 평균 역수를 계산합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - MRR 값 (float).
        """
        cumulative_reciprocal = 0  # 누적 역수 합을 저장할 변수
        Q = len(self.actual_docs)  # 전체 쿼리 수 (실제 문서 리스트의 길이)
        
        # 실제 문서 리스트와 예측 문서 리스트를 반복
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
            
            for rank, predicted_doc in enumerate(predicted_docs, start=1):
                # 예측 문서 중 첫 번째로 실제 문서와 일치하는 경우
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs):
                    cumulative_reciprocal += 1 / rank  # 해당 순위의 역수를 누적
                    break  # 첫 번째 일치 문서를 찾으면 루프 종료
        
        # 누적 역수를 전체 쿼리 수로 나누어 MRR 계산
        return cumulative_reciprocal / Q if Q > 0 else 0.0

    # Recall 계산
    def calculate_recall(self, k: int = None) -> float:
        """
        Recall를 계산하는 메서드.
        
        상위 k개의 예측 문서 중 실제 문서가 포함된 비율을 계산합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - Recall 값 (float).
        """
        total_recall = 0  # 전체 Recall 합을 저장할 변수
        total_docs = 0  # 전체 실제 문서 수를 저장할 변수
        
        # 실제 문서 리스트와 예측 문서 리스트를 반복
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
            match_count = 0  # 현재 문서 쌍에서의 일치 횟수를 저장할 변수
            top_k_predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs]
            
            for actual_doc in actual_docs:
                actual_text = actual_doc.page_content  # 실제 문서의 텍스트 추출
                # 실제 문서가 상위 k개의 예측 문서에 포함된 경우
                if self.text_match(actual_text, top_k_predicted_texts):
                    match_count += 1  # 일치 횟수 증가
            
            total_recall += match_count  # 전체 Recall 합에 현재 일치 횟수 추가
            total_docs += len(actual_docs)  # 전체 실제 문서 수에 현재 문서 수 추가
        
        # 전체 Recall 합을 전체 문서 수로 나누어 Recall 계산
        return total_recall / total_docs if total_docs > 0 else 0.0
    
    # Precision 계산
    def calculate_precision(self, k: int = None) -> float:
        """
        Precision를 계산하는 메서드.
        
        상위 k개의 예측 문서 중 실제 문서가 포함된 비율을 계산합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - Precision 값 (float).
        """
        total_precision = 0  # 전체 Precision 합을 저장할 변수
        total_queries = len(self.actual_docs)  # 전체 쿼리 수를 저장할 변수
        
        # 실제 문서 리스트와 예측 문서 리스트를 반복
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
            match_count = 0  # 현재 문서 쌍에서의 일치 횟수를 저장할 변수
            top_k_predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs]
            
            for predicted_text in top_k_predicted_texts:
                # 예측 문서가 실제 문서 중 하나와 일치하는 경우
                if any(self.text_match(actual_doc.page_content, predicted_text) for actual_doc in actual_docs):
                    match_count += 1  # 일치 횟수 증가
            
            total_precision += match_count / len(top_k_predicted_texts)  # 현재 Precision 값을 전체 Precision 합에 추가
        
        # 전체 Precision 합을 전체 쿼리 수로 나누어 Precision 계산
        return total_precision / total_queries if total_queries > 0 else 0.0

    # MAP 계산
    def calculate_map(self, k: int = None) -> float:
        """
        MAP (Mean Average Precision)를 계산하는 메서드.
        
        상위 k개의 예측 문서에 대해 평균 Precision을 계산합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - MAP 값 (float).
        """
        total_map = 0  # 전체 MAP 합을 저장할 변수
        total_queries = len(self.actual_docs)  # 전체 쿼리 수를 저장할 변수
        
        # 실제 문서 리스트와 예측 문서 리스트를 반복
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
            num_relevant = 0  # 관련 문서 수를 저장할 변수
            precision_at_i = 0  # i번째 문서까지의 Precision 합을 저장할 변수
            
            for i, predicted_doc in enumerate(predicted_docs, start=1):
                # 예측 문서가 실제 문서 중 하나와 일치하는 경우
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs):
                    num_relevant += 1  # 관련 문서 수 증가
                    precision_at_i += num_relevant / i  # Precision 값을 누적
            
            # 관련 문서가 있을 경우 MAP 값을 계산하여 전체 MAP 합에 추가
            total_map += precision_at_i / num_relevant if num_relevant > 0 else 0
        
        # 전체 MAP 합을 전체 쿼리 수로 나누어 MAP 계산
        return total_map / total_queries if total_queries > 0 else 0.0
    
    def calculate_dcg(self, relevance_scores: List[float], k: int) -> float:
        """
        DCG (Discounted Cumulative Gain)를 계산하는 메서드.

        매개변수:
        - relevance_scores: 관련성 점수 리스트 (List[float]).
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int).

        반환값:
        - DCG 값 (float).
        """
        dcg = 0.0
        for i in range(min(len(relevance_scores), k)):
            dcg += relevance_scores[i] / math.log2(i + 2)
        return dcg

    def calculate_ndcg(self, k: int = None) -> float:
        """
        NDCG (Normalized Discounted Cumulative Gain)를 계산하는 메서드.
        
        주어진 순위에서의 관련성을 바탕으로 누적 이득을 계산하여 NDCG 값을 반환합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - NDCG 값 (float).
        """
        total_ndcg = 0  # 전체 NDCG 합을 저장할 변수
        total_queries = len(self.actual_docs)  # 전체 쿼리 수를 저장할 변수
        
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
                
            relevance_scores = []
            for pred_doc in predicted_docs:
                max_score = max(
                    1 if self.text_match(actual_doc.page_content, pred_doc.page_content) else 0
                    for actual_doc in actual_docs
                )
                relevance_scores.append(max_score)

            ideal_relevance_scores = sorted(relevance_scores, reverse=True)
            dcg = self.calculate_dcg(relevance_scores, k if k is not None else len(relevance_scores))
            idcg = self.calculate_dcg(ideal_relevance_scores, k if k is not None else len(ideal_relevance_scores))
            total_ndcg += dcg / idcg if idcg > 0 else 0.0
        
        return total_ndcg / total_queries if total_queries > 0 else 0.0


# ROUGE 점수를 사용하는 자식 클래스 정의
class RougeOfflineRetrievalEvaluators(OfflineRetrievalEvaluators):
    def __init__(self, actual_docs: List[List["Document"]], predicted_docs: List[List["Document"]], match_method="rouge1", threshold=0.8):
        """
        RougeOfflineRetrievalEvaluators 클래스 초기화 메서드

        매개변수:
        - actual_docs: 실제 문서의 리스트. 각 문서는 List[List[Document]] 형태로 전달됩니다.
        - predicted_docs: 예측 문서의 리스트. 각 문서는 List[List[Document]] 형태로 전달됩니다.
        - match_method: 사용할 ROUGE 매칭 방법 ('rouge1', 'rouge2', 'rougeL' 중 하나).
        - threshold: ROUGE 점수를 사용할 경우의 임계값 (float).
        """
        super().__init__(actual_docs, predicted_docs, match_method)  # 부모 클래스 초기화 메서드 호출
        self.threshold = threshold  # ROUGE 점수 임계값 저장
        self.scorer = rouge_scorer.RougeScorer([match_method], use_stemmer=True)  # ROUGE 점수 계산기 초기화
    
    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        """
        ROUGE 점수를 사용하여 실제 텍스트와 예측 텍스트가 일치하는지 확인하는 메서드.

        매개변수:
        - actual_text: 실제 문서의 텍스트 (str 타입).
        - predicted_text: 예측된 문서의 텍스트 또는 텍스트 리스트 (str 또는 List[str] 타입).

        반환값:
        - 일치 여부를 나타내는 boolean 값.
        """
        if self.match_method in ["rouge1", "rouge2", "rougeL"]:
            if isinstance(predicted_text, list):
                # 리스트 내 텍스트 중 하나라도 ROUGE 점수가 임계값 이상이면 True 반환
                return any(self.scorer.score(actual_text, text)[self.match_method].fmeasure >= self.threshold for text in predicted_text)
            else:
                # 단일 텍스트에 대해 ROUGE 점수가 임계값 이상이면 True 반환
                score = self.scorer.score(actual_text, predicted_text)[self.match_method].fmeasure
                return score >= self.threshold
        else:
            # ROUGE 이외의 매칭 방법은 부모 클래스의 메서드를 사용
            return super().text_match(actual_text, predicted_text)

    # NDCG 계산
    def calculate_ndcg(self, k: int = None) -> float:
        """
        NDCG (Normalized Discounted Cumulative Gain)를 계산하는 메서드.
        
        주어진 순위에서의 관련성을 바탕으로 누적 이득을 계산하여 NDCG 값을 반환합니다.
        k=None일 경우, 전체 예측 문서를 대상으로 계산합니다.

        매개변수:
        - k: 상위 k개의 문서를 고려할 때의 k 값 (int). None이면 전체 문서를 대상으로 함.

        반환값:
        - NDCG 값 (float).
        """
        total_ndcg = 0  # 전체 NDCG 합을 저장할 변수
        total_queries = len(self.actual_docs)  # 전체 쿼리 수를 저장할 변수
        
        # 실제 문서 리스트와 예측 문서 리스트를 반복
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]  # 상위 k개의 예측 문서로 제한
                
            relevance_scores = []  # 각 문서 쌍의 관련성 점수를 저장할 리스트
            
            for pred_doc in predicted_docs:
                # 각 예측 문서에 대해 모든 실제 문서와 비교하여 가장 높은 ROUGE 점수를 사용
                max_score = max(
                    self.scorer.score(actual_doc.page_content, pred_doc.page_content)[self.match_method].fmeasure
                    for actual_doc in actual_docs
                )
                relevance_scores.append(max_score)  # 해당 점수를 관련성 점수 리스트에 추가
            
            # 관련성 점수 리스트를 내림차순으로 정렬하여 이상적인 관련성 점수 리스트 생성
            ideal_relevance_scores = sorted(relevance_scores, reverse=True)
            dcg = self.calculate_dcg(relevance_scores, k if k is not None else len(relevance_scores))  # DCG 계산
            idcg = self.calculate_dcg(ideal_relevance_scores, k if k is not None else len(ideal_relevance_scores))  # 이상적인 DCG 계산
            
            # NDCG 값을 계산하여 전체 NDCG 합에 추가
            total_ndcg += dcg / idcg if idcg > 0 else 0.0
        
        # 전체 NDCG 합을 전체 쿼리 수로 나누어 NDCG 계산
        return total_ndcg / total_queries if total_queries > 0 else 0.0
