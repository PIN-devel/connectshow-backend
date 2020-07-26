# Solgik Sever Url

| 기능                 | HTTP Methods | Url                                                  | Input Parameter | Response |
| -------------------- | ------------ | ---------------------------------------------------- | --------------- | -------- |
| 회원가입             | post         | /rest-auth/signup/                                   |                 |          |
| 로그인               | post         | /rest-auth/login/                                    |                 |          |
| 로그아웃             | post         | /rest-auth/logout/                                   |                 |          |
| 비밀번호 변경        | post         | /rest-auth/password/change/                          |                 |          |
| 유저 조회            | get          | /accounts/?kw='수미'&order_by='point'&period="month" |                 |          |
| 유저 상세 조회       | get          | /accounts/<user_id>/                                 |                 |          |
| 회원정보 수정        | put          | /accounts/<user_id>/                                 |                 |          |
| 회원 탈퇴            | delete       | /accounts/<user_id>/                                 |                 |          |
| 비밀번호 찾기        | -            | -                                                    |                 |          |
|                      |              |                                                      |                 |          |
| 스트레칭 리스트 조회 | get          | /streching/?category=""                              |                 |          |
| 스트레칭 생성        | post         | /streching/                                          |                 |          |
| 스트레칭 상세 조회   | get          | /streching/<streching_id>/                           |                 |          |
| 스트레칭 수정        | put          | /streching/<streching_id>/                           |                 |          |
| 스트레칭 삭제        | delete       | /streching/<streching_id>/                           |                 |          |
|                      |              |                                                      |                 |          |
| 짝꿍 리스트 조회     | get          | /accounts/friend/                                    |                 |          |
| 짝꿍 추가/삭제       | post         | /accounts/friend/<user_id>/                          |                 |          |


