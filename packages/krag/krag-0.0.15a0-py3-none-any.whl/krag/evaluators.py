# krag/evaluators.py

from krag.document import KragDocument as Document
from korouge_score import rouge_scorer
from typing import Union, List
import math

class OfflineRetrievalEvaluators:
    def __init__(self, actual_docs: List[List[Document]], predicted_docs: List[List[Document]], match_method="text"):
        self.actual_docs = actual_docs 
        self.predicted_docs = predicted_docs  
        self.match_method = match_method  

    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        if isinstance(predicted_text, list):
            return any(actual_text in text for text in predicted_text)
        return actual_text in predicted_text

    def calculate_hit_rate(self, k: int = None) -> float:
        total_queries = len(self.actual_docs)
        full_matches = 0
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
            predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs]
            if all(self.text_match(actual_doc.page_content, predicted_texts) for actual_doc in actual_docs):
                full_matches += 1
        return full_matches / total_queries if total_queries > 0 else 0.0

    def calculate_mrr(self, k: int = None) -> float:
        cumulative_reciprocal = 0
        Q = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
            for rank, predicted_doc in enumerate(predicted_docs, start=1):
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs):
                    cumulative_reciprocal += 1 / rank
                    break
        return cumulative_reciprocal / Q if Q > 0 else 0.0

    def calculate_recall(self, k: int = None) -> float:
        total_recall = 0
        total_docs = 0
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
            match_count = 0
            top_k_predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs]
            for actual_doc in actual_docs:
                actual_text = actual_doc.page_content
                if self.text_match(actual_text, top_k_predicted_texts):
                    match_count += 1
            total_recall += match_count
            total_docs += len(actual_docs)
        return total_recall / total_docs if total_docs > 0 else 0.0
    
    def calculate_precision(self, k: int = None) -> float:
        total_precision = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
            match_count = 0
            top_k_predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs]
            for predicted_text in top_k_predicted_texts:
                if any(self.text_match(actual_doc.page_content, predicted_text) for actual_doc in actual_docs):
                    match_count += 1
            total_precision += match_count / len(top_k_predicted_texts)
        return total_precision / total_queries if total_queries > 0 else 0.0

    def calculate_map(self, k: int = None) -> float:
        total_map = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
            num_relevant = 0
            precision_at_i = 0
            for i, predicted_doc in enumerate(predicted_docs, start=1):
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs):
                    num_relevant += 1
                    precision_at_i += num_relevant / i
            total_map += precision_at_i / num_relevant if num_relevant > 0 else 0
        return total_map / total_queries if total_queries > 0 else 0.0
    
    def calculate_dcg(self, relevance_scores: List[float], k: int) -> float:
        dcg = 0.0
        for i in range(min(len(relevance_scores), k)):
            dcg += relevance_scores[i] / math.log2(i + 2)
        return dcg

    def calculate_ndcg(self, k: int = None) -> float:
        total_ndcg = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
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

class RougeOfflineRetrievalEvaluators(OfflineRetrievalEvaluators):
    def __init__(self, actual_docs: List[List["Document"]], predicted_docs: List[List["Document"]], match_method="rouge1", threshold=0.8):
        super().__init__(actual_docs, predicted_docs, match_method)
        self.threshold = threshold
        self.scorer = rouge_scorer.RougeScorer([match_method], use_stemmer=True)
    
    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        if self.match_method in ["rouge1", "rouge2", "rougeL"]:
            if isinstance(predicted_text, list):
                return any(self.scorer.score(actual_text, text)[self.match_method].fmeasure >= self.threshold for text in predicted_text)
            else:
                score = self.scorer.score(actual_text, predicted_text)[self.match_method].fmeasure
                return score >= self.threshold
        else:
            return super().text_match(actual_text, predicted_text)

    def calculate_ndcg(self, k: int = None) -> float:
        total_ndcg = 0
        total_queries = len(self.actual_docs)
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            if k is not None:
                predicted_docs = predicted_docs[:k]
            relevance_scores = []
            for pred_doc in predicted_docs:
                max_score = max(
                    self.scorer.score(actual_doc.page_content, pred_doc.page_content)[self.match_method].fmeasure
                    for actual_doc in actual_docs
                )
                relevance_scores.append(max_score)
            ideal_relevance_scores = sorted(relevance_scores, reverse=True)
            dcg = self.calculate_dcg(relevance_scores, k if k is not None else len(relevance_scores))
            idcg = self.calculate_dcg(ideal_relevance_scores, k if k is not None else len(ideal_relevance_scores))
            total_ndcg += dcg / idcg if idcg > 0 else 0.0
        return total_ndcg / total_queries if total_queries > 0 else 0.0
