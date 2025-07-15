import openai
from core.config import settings
from domain.title.schemas import TitleAnalyzeRequest, TitleAnalyzeResponse
from domain.title.models import TitleAnalysis
from sqlalchemy.orm import Session

def analyze_title(req: TitleAnalyzeRequest, db: Session, user_id: str) -> TitleAnalyzeResponse:
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"제목: {req.title}\n분석 및 피드백을 한국어로 요약해줘. CTR, 참여점수(0~1), 개선 제안, 피드백, 플랫폼 최적화 여부도 포함해서."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message["content"]
    # 예시 파싱 (실제 파싱 로직 필요)
    ctr = 0.8
    engagement = 0.7
    suggestions = ["더 짧게", "키워드 추가"]
    feedback = content
    platform_optimized = True
    # 로그 저장
    db.add(TitleAnalysis(user_id=user_id, title=req.title, result=content))
    db.commit()
    return TitleAnalyzeResponse(
        title=req.title,
        click_through_rate_score=ctr,
        engagement_score=engagement,
        suggestions=suggestions,
        feedback=feedback,
        platform_optimized=platform_optimized
    )
