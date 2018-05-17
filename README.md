# Goal: push 알림을 비동기로 처리
## celery 기본 사용법

1. celery install
```bash
pip install celery
```

2. celery에 필요한 broker(message transporter,), backend(return value storage) 셋팅
- broker/ backend: redis 사용
```python
config = { 'CELERY_BROKER_URL': 'redis://localhost:6379/0',
            'CELERY_RESULT_BACKEND': 'redis://localhost:6379/0'}
```

3. celery instance 생성
```python
celery = Celery('task_test', broker=config['CELERY_BROKER_URL'])
# storage 붙일 경우, backend 같이 설정
```

4. celery 작업 내용 구현
```python
@celery.task
def multiple(a, b):
	return a * b
```

5. celery 프로세스 실행
```python
celery -A tasks.task_test worker --loglevel=info
```

## flask handler에서 celery 사용:
1. 분리된 task module import
2. task 등록
```python
@app.route('/multiple/<a>/<b>')
def apply_multiple(a, b):
	multiple_task_id = task_test.multiple.delay(3, 4)
	if multiple_task_id:
		return str(multiple_task_id)
# delay() 활용시 celery task의 id 발급
```

3. task return value 받기  
- task state에 따라 결과 확인
```python
@app.route('/<multiple_task_id>')
	def show_multiple_result(multiple_task_id):
	multiple_task_id = task_test.multiple.AsyncResult(multiple_task_id)
	
	if multiple_task_id.state == 'PENDING':
		response = {
			'state': multiple_task_id.state,
			'current': 0,
			'total': 1,
			'status': 'Pending...'
			}
	elif multiple_task_id.state != 'FAILURE':
		response = {
			'state': multiple_task_id.state,
			'current': multiple_task_id.info
			}
	else:
		response = {
			'state': multiple_task_id.state,
			'current': 1,
			'total': 1,
			'status': str(multiple_task_id.info)
		}
	return jsonify(response)
```

## docker/ docker-compose 활용
- redis, celery를 docker 이미지로 생성함 -> 관리 용이
- docker-compose로 flask, redis, celery를 각각 연결하여 함께 띄움
```dockerfile
[docker-compose.yml 생성하여 필요한 요소들을 각각 컨테이너에 담아 연결함]

version: '3'

# 사용할 service 내용 각각 기술
services:
	flask-celery: # 해당 service의 callable name
		build: .
		ports:
			- "5000:5000"
	redis:
		image: "redis"
	celery:
		build: .
		command: celery -A tasks/task_test worker --loglevel=info
```

```dockerfile
[dockerfile로 원하는 컨테이너의 이미지 생성]
FROM python 

RUN mkdir app

ADD tasks app/tasks
ADD app.py app
ADD requirements.txt app

WORKDIR app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### 참고. requirements.txt에 필요한 라이브러리 기술하여 set up 간편하게 하기
- python requirements generetor를 활용하여 생성 가능
```python
amqp==2.2.2
billiard==3.5.0.3
celery==4.1.0
click==6.7
Flask==1.0.2
itsdangerous==0.24
Jinja2==2.10
kombu==4.1.0
MarkupSafe==1.0
pytz==2018.4
redis==2.10.6
vine==1.1.4
Werkzeug==0.14.1
```
 
