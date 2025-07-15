import openai
from core.config import settings
from domain.hashtags.schemas import HashtagRecommendRequest, HashtagRecommendResponse
from domain.hashtags.models import HashtagSearch
from sqlalchemy.orm import Session
from infrastructure.security import get_current_user

def recommend_hashtags(req: HashtagRecommendRequest, db: Session, user_id: str) -> HashtagRecommendResponse:
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"키워드: {', '.join(req.keywords)}\n관련 해시태그 10개와 점수(0~1)를 반환해줘. 예시: #해시태그1:0.9, #해시태그2:0.8 ..."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message["content"]
    # 예시 파싱 (실제 파싱 로직 필요)
    hashtags = []
    scores = []
    for item in content.split(','):
        if ':' in item:
            tag, score = item.strip().split(':')
            hashtags.append(tag.strip())
            try:
                scores.append(float(score.strip()))
            except:
                scores.append(0.5)
    # 로그 저장
    db.add(HashtagSearch(user_id=user_id, keywords=','.join(req.keywords), result=content))
    db.commit()
    return HashtagRecommendResponse(
        hashtags=hashtags,
        relevance_scores=scores,
        platform=req.platform or "youtube"
    )
