# URL Shortener
URL을 입력하면 단축된 URL을 제공, 단축된 URL을 웹 브라우저의 주소창에 입력하면 원래의 URL 주소로 redirect 해주는 서비스

# 기술 스택
- backend: Python3.6, Django
- frontend: HTML, Javascript, CSS, JQuery
    - 별도의 서버 구현 없이 Django 서버에서 static page로 제공
- database: SQLite (Django 기본 내장)

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
![image](https://user-images.githubusercontent.com/54832818/140405733-c6dde13a-d4a4-4035-aa93-8441273f8df4.png)
* main page(local에서 실행 시 `localhost:8088`) 접속화면

![image](https://user-images.githubusercontent.com/54832818/140405954-458f4ead-9543-4a2f-929c-2c365f4a175c.png)
* URL을 입력하고 submit 버튼을 누르면 shorten URL이 반환됨

![image](https://user-images.githubusercontent.com/54832818/140406138-e6500e3a-bb27-4a00-a041-d727d2abd4b1.png)
* 서버에 shorten URL이 존재하는 경우 동일한 shorten URL 반환
* URL에 http/https 프로토콜을 명시하지 않아도 DB에 URL이 존재하는 경우 동일한 결과를 제공
    * DB에 존재하지 않는 경우 http로 간주하고 shorten URL 반환

![image](https://user-images.githubusercontent.com/54832818/140406593-11959d58-22db-4307-911c-cacde3590d50.png)
* URL 형식에 맞지 않는 text 입력 시 error message 반환

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
