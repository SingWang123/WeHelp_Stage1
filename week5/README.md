# Week 5 Assignment

## Task 2: Create database and table in MySQL server
### Create a new database named website
*SQL Statement*  

```MySql
create data base website;
```

![statement 2-1](images/statement_2-1.png)

### Create a new table named member, in the website database, designed as below:
*SQL Statement*  

```MySql
create table member(id bigint, name varchar(255), username varchar(255), password varchar(255),follower_count int unsigned, time datetime);
```

![statement 2-1_1](images/statement_2-2_1.png)  

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

![statement 2-1_1](images/statement_2-2_2.png)  

*SQL Statement*  

```MySql
alter table member
    -> modify follower_count int unsigned not null default 0;
```  
```MySql
alter table member
    -> modify time datetime not null default current_timestamp;
```  

![statement 2-1_1](images/statement_2-2_3.png)  

## Task 3: SQL CRUD
### INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.

