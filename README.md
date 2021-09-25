# KOPIS 빅데이터 콘테스트 주제 : 협업 필터링
<p>추천받고 싶은 사람의 성별, 나이대, 날짜, 시간대, 날씨를 선택하면 날짜, 시간 날씨로 필터링 해주고, 성별 나이대 정보로 협업 필터링을 진행해 유사도가 가장 높은 공연을 순위 N개(500)까지 필터링 합니다.

위에서 필터링된 뮤지컬 명으로 검색한 결과를 네이버 블로그 내용, tistory 블로그 내용, youtube 댓글 을 크롤링해서 가져온 내용을 긍부정도 모델로 긍정도를 검사해서 긍부정도가 높은 순으로 추천해줍니다.
</p>

```shell
pip install -r requirements.txt
```


```
cd final
```
```
python main.py
```

## Backend

```bash
pip install -r requirements-server

cd final

uvicorn app:app --reload
```

## Frontend

```bash
cd frontend

npm install
# or
yarn

npm start
# or
yarn start
```
