# 커넥쇼

![image-20201022000019442](readme.assets/image-20201022000019442.png)

![image-20201021235843858](readme.assets/image-20201021235843858.png)

![image-20201021235853730](readme.assets/image-20201021235853730.png)

![image-20201021235904912](readme.assets/image-20201021235904912.png)

![image-20201021235914307](readme.assets/image-20201021235914307.png)

![image-20201021235926931](readme.assets/image-20201021235926931.png)

![image-20201022000036476](readme.assets/image-20201022000036476.png)

![image-20201022000049146](readme.assets/image-20201022000049146.png)

![image-20201022000106690](readme.assets/image-20201022000106690.png)

![image-20201022000116530](readme.assets/image-20201022000116530.png)






# Start

```bash
pip install -r requirements.txt
python manage.py runserver
```





# API

| 기능          | HTTP Methods | Url                  | Input Parameter                                              | Response           |
| ------------- | ------------ | -------------------- | ------------------------------------------------------------ | ------------------ |
| 회원가입      | post         | /rest-auth/signup/   | username, passward1, passward2 ,email, like_category, profile_image(default) | status, data(user) |
| 로그인        | post         | /rest-auth/login/    | username, passward                                           | token              |
| 로그아웃      | post         | /rest-auth/logout/   | token(header)                                                | status             |
| 회원정보 수정 | put          | /accounts/<user_id>/ | email, like_category, profile_image(default)                 | status, data(user) |
| 회원 탈퇴     | delete       | /accounts/<user_id>/ | token(header)                                                | status             |

...

# ERD

![image-20201022001339743](readme.assets/image-20201022001339743.png)