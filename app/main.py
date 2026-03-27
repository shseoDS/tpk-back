from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import database
from app.api import auth, exam, practice, history, code

app = FastAPI(
    title="TOPIK Practice API",
    description="한국어능력시험(TOPIK) 연습 문제 풀이 서비스 API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(exam.router, prefix="/exams", tags=["Exam"])
app.include_router(practice.router, prefix="/practice", tags=["Practice"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(code.router, prefix="/codes", tags=["Code"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
