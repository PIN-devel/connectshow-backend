# Solgik Sever Url

| 기능                     | HTTP Methods | Url                                       | Input Parameter                                              | Response                                                     |
| ------------------------ | ------------ | ----------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 회원가입                 | post         | /rest-auth/signup/                        | username, passward1, passward2 ,email, like_category, profile_image(default) | status, data(user_id ...)                                    |
| 로그인                   | post         | /rest-auth/login/                         | username, passward                                           | token                                                        |
| 로그아웃                 | post         | /rest-auth/logout/                        | token(header)                                                | status                                                       |
| 비밀번호 변경            | post         | /rest-auth/password/change/               | token(header),new_password1, new_password2, old_password     | detail                                                       |
| 유저 조회                | get          | /accounts/                                | token(header)                                                | data(user_id,username)                                       |
| 유저 상세 조회           | get          | /accounts/detail/                         | token(header)                                                | data(user_id,username,email,profile image, like_category, follow_club, club) |
| 회원정보 수정            | put          | /accounts/<user_id>/                      | email, like_category, profile_image(default)                 | status, data(user)                                           |
| 회원 탈퇴                | delete       | /accounts/<user_id>/                      | token(header)                                                | status                                                       |
|                          |              |                                           |                                                              |                                                              |
| 클럽 리스트 조회         | get          | /accounts/clubs/                          |                                                              |                                                              |
| 클럽 생성                | post         | /accounts/clubs/                          |                                                              |                                                              |
| 클럽 상세 조회           | get          | /accounts/clubs/<club_id>/                |                                                              |                                                              |
| 클럽 수정                | put          | /accounts/clubs/<club_id>/                |                                                              |                                                              |
| 클럽 삭제                | delete       | /accounts/clubs/<club_id>/                |                                                              |                                                              |
| 클럽 가입 신청/취소      | post         | /accounts/clubs/<club_id>/apply/          | token(header)                                                |                                                              |
| 클럽 탈퇴                | delete       | /accounts/clubs/<club_id>/apply/          | token(header)                                                |                                                              |
| 클럽가입 수락            | post         | /accounts/clubs/<club_id>/user/<user_id>/ |                                                              |                                                              |
| 클럽 거절/ 추방          | delete       | /accounts/clubs/<club_id>/user/<user_id>/ |                                                              |                                                              |
| 클럽 팔로우              | post         | /accounts/clubs/<club_id>/follow/         | token(header)                                                |                                                              |
|                          |              |                                           |                                                              |                                                              |
| 퍼포먼스 리스트          | get          | /performance/?category=<category_name>    |                                                              |                                                              |
| 퍼포먼스 생성            | post         | /performances/                            | user_id, club_id,,,,                                         |                                                              |
| 퍼포먼스 조회            | get          | /performances/<performance_id>/           |                                                              |                                                              |
| 퍼포먼스 수정            | put          | /performances/<performance_id>/           |                                                              |                                                              |
| 퍼포먼스 삭제            | delete       | /performances/<performance_id>/           |                                                              |                                                              |
| 퍼포먼스 추천            | get          | /performances/recommandations/            |                                                              |                                                              |
| 리뷰 리스트              | get          | /performances/<performance_id>/reviews/   |                                                              |                                                              |
| 리뷰 생성                | post         | /performances/<performance_id>/reviews/   |                                                              |                                                              |
| 리뷰 수정                | put          | /performances/reviews/<review_id>/        |                                                              |                                                              |
| 리뷰 삭제                | delete       | /performances/reviews/<review_id>/        |                                                              |                                                              |
| 퍼포먼스 좋아요          | post         | /performances/<performance_id>/like/      |                                                              |                                                              |
| 클럽에 해당하는 퍼포먼스 | get          | /performances/club/<club_id>/             |                                                              |                                                              |
|                          |              |                                           |                                                              |                                                              |
| 아티클 리스트 조회       | get          | /community/                               |                                                              |                                                              |
| 아티클 생성              | post         | /community/                               | club_id                                                      |                                                              |
| 아티클 상세 조회         | get          | /community/<article_id>/                  |                                                              |                                                              |
| 아티클 수정              | put          | /community/<article_id>/                  |                                                              |                                                              |
| 아티클 삭제              | delete       | /community/<article_id>/                  |                                                              |                                                              |
| 댓글 리스트 조회         | get          | /community/<article_id>/comments/         |                                                              |                                                              |
| 댓글 생성                | post         | /community/<article_id>/comments/         |                                                              |                                                              |
| 댓글 수정                | put          | /community/comments/<comments_id>         |                                                              |                                                              |
| 댓글 삭제                | delete       | /community/comments/<comments_id>         |                                                              |                                                              |

