## 🛠 Project Overview
- **Framework:** FastAPI
- **Database Access:** Raw SQL (using `databases`)
- **No ORM:** Do not use SQLAlchemy or Tortoise. Use raw SQL queries.

## 📁 Directory Structure Rules
- `app/db/`: DB 커넥션 풀 설정 및 연결/해제 로직.
- `app/api/`: SQL 쿼리를 직접 실행하거나, 전용 CRUD 함수 호출.
- `app/schemas/`: DB 결과를 객체로 변환하기 위한 Pydantic 모델 정의.

## 📝 Coding Standards
- **Raw SQL:** 모든 쿼리는 f-string이 아닌 **기본 바인딩(Parameter Binding)** 방식을 사용하여 SQL Injection을 방지할 것.
  - 예: `query = "SELECT * FROM users WHERE id = :id"`
- **Type Casting:** SQL 실행 결과(Row)를 반환할 때 반드시 `schemas`에 정의된 Pydantic 모델로 변환하여 반환할 것.
- **Async DB:** 데이터베이스 작업은 반드시 `await`를 사용하는 비동기 드라이버를 사용할 것.