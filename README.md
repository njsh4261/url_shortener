# URL Shortener
URL을 입력하면 단축된 URL을 제공, 단축된 URL을 웹 브라우저의 주소창에 입력하면 원래의 URL 주소로 redirect 해주는 서비스

# 기술 스택
- backend: Python3.6, Django
- frontend: HTML, Javascript, CSS, JQuery
    - 별도의 서버 구현 없이 Django 서버에서 static page로 제공

# 실행 환경 준비
* Linux 또는 Windows 10의 WSL 사용 기준
```
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# 실행 방법
* Django에서 static file 제공을 위해 --insecure 옵션이 필요함
```
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8088 --insecure
```

# 실행 예시


# APIs
- 명시되지 않은 method로 접근 시 (e.g. GET /url-enc) 403 Forbidden 혹은 404 not found 에러가 발생

|API|설명|
|:---|:----|
| `GET /`|단축하고자 하는 URL을 입력 및 단축된 URL을 확인하는 page 제공|
| `POST /url-enc` | URL 단축을 요청하는 API |
| `GET /[shorten_url]` | `[shorten_url]`에 해당하는 원본 URL을 DB에서 검색하여 제공|

- `POST /url-enc`의 경우 Request body에 필수로 포함해야 할 attribute / Response body에 포함된 attribute 존재
    - Request body 예시
        ```
        {
            "url": "https://www.github.com/"
        }
        ```
    - Response body 예시
        ```
        {
            "shorten_url": "http://localhost:8088/EMJD"
            "message": "Success! You may copy the shorten URL above."
        }
        ```
