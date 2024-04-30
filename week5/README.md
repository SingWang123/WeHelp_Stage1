# Week 5 Assignment

## Task 2: Create database and table in MySQL server
### Create a new database named website
*SQL Statement*  

```MySql
create database website;
```

![statement 2-1](images/statement_2-1.png)

### Create a new table named member, in the website database.
*SQL Statement*  

```MySql
create table member(id bigint, name varchar(255), username varchar(255), password varchar(255),follower_count int unsigned, time datetime);
```

![statement 2-2_1](images/statement_2-2_1.png)  

*SQL Statement*  

```MySql
alter table member
    -> modify column name varchar(255) not null,
    -> modify column username varchar(255) not null,
    -> modify column password varchar(255) not null;
```  
```MySql
alter table member
    -> add primary key (id);
alter table member
    -> modify id bigint auto_increment;
```  

![statement 2-2_2](images/statement_2-2_2.png)  

*SQL Statement*  

```MySql
alter table member
    -> modify follower_count int unsigned not null default 0;
```  
```MySql
alter table member
    -> modify time datetime not null default current_timestamp;
```  

![statement 2-2_3](images/statement_2-2_3.png)  

## Task 3: SQL CRUD
### INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
*SQL Statement*  

```MySql
insert into member (name, username, password) values ('test', 'test', 'test');
```

![statement 3-1_1](images/statement_3-1_1.png)  

*SQL Statement*  

```MySql
insert into member (name, username, password) values ('林小美', 'mei052277', 'qaz123');
insert into member (name, username, password) values ('WOOWOOOWOOOWOOOOWOO', 'OOWOOWOOOWOOW', '123456');
insert into member (name, username, password) values ('王大明是我的偶像', 'mingmingNO.1', 'frkofkro');
insert into member (name, username, password) values ('我很想試試看字串長度但還是不要整自己好了', '!@#$%^&*', '*&^%$#@!');
```

![statement 3-1_2](images/statement_3-1_2.png)  

### SELECT all rows from the member table.
*SQL Statement*  

```MySql
select * from member;
```

![statement 3-2](images/statement_3-2.png)  

### SELECT all rows from the member table, in descending order of time.
*SQL Statement*  

```MySql
select * from member order by time desc;
```

![statement 3-3](images/statement_3-3.png)  

### SELECT total 3 rows, second to fourth, from the member table, in descending order of time.
*SQL Statement*  

```MySql
select * from member order by time desc limit 1,3;
```

![statement 3-4](images/statement_3-4.png)  

### SELECT rows where username equals to test.
*SQL Statement*  

```MySql
select * from member where username = 'test';
```

![statement 3-5](images/statement_3-5.png)  

### SELECT rows where name includes the es keyword.
*SQL Statement*  

```MySql
select * from member where username like '%es%';
```

![statement 3-6](images/statement_3-6.png)  

### SELECT rows where both username and password equal to test.
*SQL Statement*  

```MySql
select * from member where username = 'test' and password = 'test';
```

![statement 3-7](images/statement_3-7.png)  

### UPDATE data in name column to test2 where username equals to test.
*SQL Statement*  

```MySql
update member set name = 'test2' where username = 'test';
```

![statement 3-8](images/statement_3-8.png)  

## Task 4: SQL Aggregation Functions
### SELECT how many rows from the member table.
*SQL Statement*  

```MySql
select count(*) from member;
```

![statement 4-1](images/statement_4-1.png)  

### SELECT the sum of follower_count of all the rows from the member table.
*SQL Statement*  

```MySql
update member set follower_count = 5 where id = '2';
update member set follower_count = 45458 where id = '3';
update member set follower_count = 487 where id = '4';
update member set follower_count = 6 where id = '5';
```

```MySql
select sum(follower_count)
    -> from member;
```

![statement 4-2](images/statement_4-2.png)  

### SELECT the average of follower_count of all the rows from the member table.
*SQL Statement*  

```MySql
select avg(follower_count)
    -> from member;
```

![statement 4-3](images/statement_4-3.png)  

###  SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
*SQL Statement*  

```MySql
select avg(follower_count)
    -> from ( select * from member order by follower_count desc limit 0,2) as subquery ;
```

![statement 4-4](images/statement_4-4.png)  

## Task 5:  SQL JOIN
### Create a new table named message, in the website database.
*SQL Statement*  

```MySql
create table message (id bigint primary key, member_id bigint, content varchar(255), like_count int unsigned, time datetime);
```  

```MySql
alter table message
    -> modify id bigint auto_increment;
alter table message
    -> modify member_id bigint not null;
alter table message
    -> modify content varchar(255) not null;
alter table message
    -> modify like_count int unsigned not null default 0;
alter table message
    -> modify time datetime not null default current_timestamp;
```

```MySql
insert into message (member_id, content, like_count) values ('1', 'test message content', '5');
insert into message (member_id, content, like_count) values ('1', '您好嗎？', '1354');
insert into message (member_id, content, like_count) values ('3', '我很好', '54');
insert into message (member_id, content, like_count) values ('4', '他不好', '0');
insert into message (member_id, content, like_count) values ('1', '謝謝', '10000');
```

![statement 5-1](images/statement_5-1.png)  

### SELECT all messages, including sender names. We have to JOIN the member table to get that.
*SQL Statement*  

```MySql
select message.id, member.username, message.content, message.like_count, message.time
    -> from message
    -> inner join member on message.member_id = member.id;
```  

![statement 5-2](images/statement_5-2.png)  

###  SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
*SQL Statement*  

```MySql
select message.id, member.username, message.content, message.like_count, message.time
    -> from message
    -> inner join member on message.member_id = member.id
    -> where username = 'test';
```  

![statement 5-3](images/statement_5-3.png) 

###   Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
*SQL Statement*  

```MySql
select avg (like_count)
    -> from (
        select message.id, member.username, message.like_count 
        from message 
        inner join member on message.member_id = member.id 
        where username = 'test'
        )
    -> as subquery;
```  

![statement 5-4](images/statement_5-4.png) 

###   Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
*SQL Statement*  

```MySql
select username, avg (like_count)
    -> from (select message.id, member.username, message.like_count from message inner join member on message.member_id = member.id) as subquery
    -> group by username;
```  

![statement 5-5](images/statement_5-5.png) 





