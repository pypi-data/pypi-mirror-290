from langchain_core.documents import Document

class KragDocument(Document):
    def __init__(self, page_content: str, metadata: dict = None):
        """
        KragDocument 클래스는 Document 클래스를 상속하여 추가적인 메타데이터와 제목을 지원합니다.
        
        매개변수:
        page_content (str): 문서의 본문 내용.
        metadata (dict): 문서와 관련된 추가 메타데이터 (기본값: None).
        """
        super().__init__(page_content=page_content, metadata=metadata)
    
    def get_summary(self) -> str:
        """
        문서의 요약을 반환하는 메서드 (여기서는 간단히 첫 100자를 반환).
        
        반환:
        str: 문서 내용의 요약.
        """
        return self.page_content[:100] + "..." if len(self.page_content) > 100 else self.page_content
    
