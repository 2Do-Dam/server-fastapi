from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.auth import router as auth_router
from api.v1.users import router as users_router
from api.v1.contents import router as contents_router
from api.v1.calendar import router as calendar_router
from api.v1.planner import router as planner_router
from api.v1.hashtags import router as hashtags_router
from api.v1.title import router as title_router
from api.v1.feedback import router as feedback_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "calyx-client-git-main-hxmxxs-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/api/users")
app.include_router(contents_router, prefix="/api/contents")
app.include_router(calendar_router, prefix="/api/calendar")
app.include_router(planner_router, prefix="/api/planner")
app.include_router(hashtags_router, prefix="/api/hashtags")
app.include_router(title_router, prefix="/api/title")
app.include_router(feedback_router, prefix="/api/feedback")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)