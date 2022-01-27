<style>
h2 {
  background: lightblue;
  padding: 10px;
}
</style>

# Assignment 5

<br>

## 要求二:建立資料庫和資料表

* 建立一個新的資料庫,取名字為 website。
```
CREATE DATABASE website;

SHOW DATABASES;
```
![request2_1](https://wc-su.github.io/wehelp-assignments/week-5/images/request2_1.png)

<br>

* 在資料庫中,建立會員資料表,取名字為 member。
```
USE website;

CREATE TABLE member (
  id BIGINT AUTO_INCREMENT, # 獨立編號
  name VARCHAR(255) NOT NULL, # 姓名
  username VARCHAR(255) NOT NULL, # 帳戶名稱
  password VARCHAR(255) NOT NULL, # 帳戶密碼
  follower_count INT NOT NULL DEFAULT 0, # 追蹤者數量
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, # 註冊時間
  PRIMARY KEY (id) # 鍵值
);

SHOW TABLES;

DESC member;
```
![request2_2](https://wc-su.github.io/wehelp-assignments/week-5/images/request2_2.png)

<br><br>

## 要求三:SQL CRUD

* 使用 INSERT 指令新增一筆資料到 member 資料表中,這筆資料的 username 和 password 欄位必須是 test。接著繼續新增至少 4 筆隨意的資料。
```
INSERT INTO member(name, username, password) VALUES("test", "test", "test");
INSERT INTO member(name, username, password, time) VALUES("小明", "king", "king223", "2022-01-27 13:17:25");
INSERT INTO member(name, username, password, follower_count) VALUES("test2", "test2", "test2", 3000);
INSERT INTO member(name, username, password, follower_count) VALUES("網紅", "may6699", "123456", 5000);
INSERT INTO member(name, username, password, follower_count) VALUES("小花", "kiki", "159753", 500);
```
![request3_1](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_1.png)

<br>

* 使用 SELECT 指令取得所有在 member 資料表中的會員資料。
```
SELECT * FROM member;
```
![request3_2](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_2.png)

<br>

* 使用 SELECT 指令取得所有在 member 資料表中的會員資料,並按照 time 欄位,由近到遠排序。
```
SELECT * FROM member ORDER BY time DESC;
```
![request3_3](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_3.png)

<br>

* 使用 SELECT 指令取得 member 資料表中第 2 ~ 4 共三筆資料,並按照 time 欄位,由近到遠排序。( 並非編號 2、3、4 的資料,而是排序後的第 2 ~ 4 筆資料 )
```
SELECT * FROM member ORDER BY time DESC LIMIT 1, 3;
```
![request3_4](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_4.png)

<br>

* 使用 SELECT 指令取得欄位 username 是 test 的會員資料。
```
SELECT * FROM member WHERE username="test";
```
![request3_5](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_5.png)

<br>

* 使用 SELECT 指令取得欄位 username 是 test、且欄位 password 也是 test 的資料。
```
SELECT * FROM member WHERE username="test" and password="test";
```
![request3_6](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_6.png)

<br>

* 使用 UPDATE 指令更新欄位 username 是 test 的會員資料,將資料中的 name 欄位改成 test2
```
UPDATE member SET name="test2" WHERE username="test";

SELECT * FROM member WHERE username="test";
```
![request3_7](https://wc-su.github.io/wehelp-assignments/week-5/images/request3_7.png)

<br><br>

## 要求四:SQL Aggregate Functions

* 取得 member 資料表中,總共有幾筆資料 ( 幾位會員 )。
```
SELECT COUNT(id) AS "會員數量" FROM member;
```
![request4_1](https://wc-su.github.io/wehelp-assignments/week-5/images/request4_1.png)

<br>

* 取得 member 資料表中,所有會員 follower_count 欄位的總和。
```
SELECT SUM(follower_count) AS "總追蹤者數量" FROM member;
```
![request4_2](https://wc-su.github.io/wehelp-assignments/week-5/images/request4_2.png)

<br>

* 取得 member 資料表中,所有會員 follower_count 欄位的平均數。
```
SELECT SUM(follower_count) / COUNT(follower_count) AS "平均追蹤者數量" FROM member;
```
![request4_3](https://wc-su.github.io/wehelp-assignments/week-5/images/request4_3.png)

<br><br>

## 要求五:SQL JOIN (Optional)

* 在資料庫中,建立新資料表,取名字為 message。
```
CREATE TABLE message (
  id BIGINT AUTO_INCREMENT, # 獨立編號
  member_id BIGINT NOT NULL, # 留言者會員編號
  content VARCHAR(255) NOT NULL, # 留言內容
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, # 留言時間
  PRIMARY KEY(id), # 鍵值
  FOREIGN KEY (member_id) REFERENCES member(id)
);

SHOW TABLES;

DESC message;
```
![request5_1_1](https://wc-su.github.io/wehelp-assignments/week-5/images/request5_1_1.png)
```
INSERT INTO message(member_id, content) VALUES(4, "聊聊天");
INSERT INTO message(member_id, content) VALUES(4, "talking");
INSERT INTO message(member_id, content) VALUES(1, "shopping");
INSERT INTO message(member_id, content) VALUES(2, "movie time");
INSERT INTO message(member_id, content) VALUES(3, "sleep");
INSERT INTO message(member_id, content) VALUES(5, "coding");
INSERT INTO message(member_id, content) VALUES(5, "relax");

SELECT * FROM message;
```
![request5_1_2](https://wc-su.github.io/wehelp-assignments/week-5/images/request5_1_2.png)

<br>

* 使用 SELECT 搭配 JOIN 語法,取得所有留言,結果須包含留言者會員的姓名。
```
SELECT member.username AS "會員帳戶", member.name AS "會員姓名", message.content AS "留言"
FROM message
JOIN member ON member.id = message.member_id;
```
![request5_2](https://wc-su.github.io/wehelp-assignments/week-5/images/request5_2.png)

<br>

* 使用 SELECT 搭配 JOIN 語法,取得 member 資料表中欄位 username 是 test 的所有留言,資料中須包含留言者會員的姓名。
```
SELECT member.name AS "會員姓名", message.content AS "留言"
FROM message
JOIN member ON member.id = message.member_id AND member.username = "test";
```
![request5_3](https://wc-su.github.io/wehelp-assignments/week-5/images/request5_3.png)

<br><br>
