
create table "user" (
    "id" serial primary key,
    "email" varchar(300),
    "nick" varchar(100),
    "password" varchar(100),
    "salt" varchar(32),
    "login_time" timestamp,
    "status" int,
    "create_date" timestamp default current_timestamp
);

create table "template" (
    "id" serial primary key,
    "title" varchar(300),
    "user_id" int default 0,
    "content" text,
    "status" int,
    "popular" int,
    "rank" int,
    "type" int,
    "create_date" timestamp default current_timestamp
);

create table "project"(
    "id" serial primary key,
    "title" varchar(300),
    "user_id" int default 0,
    "content" text,
    "status" int,
    "create_date" timestamp default current_timestamp
);





/*  --we drop all tables
drop table "user";
drop table "template";
drop table "project";


*/