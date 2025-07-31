### 의존성 생성
```pip freeze > requirements.txt```

### 의존성 설치
```pip install -r requirements.txt```

### 서버 실행
```uvicorn main:app --reload --port 8000```

### 8000 포트 내리기
```for /f "tokens=5" %a in ('netstat -ano ^| findstr :8000') do taskkill /PID %a /F```