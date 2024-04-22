CREATE SCHEMA video_data; 
drop table if exists video_data.videos, video_data.users, video_data."comments" cascade;
CREATE extension if not exists "uuid-ossp";


create table if not exists video_data."comments" (
	id uuid primary key default uuid_generate_v4(),
	comment_text text,
	date_publication date,
	count_likes int
);

CREATE TABLE if not exists video_data.videos (
	id uuid primary key default uuid_generate_v4(),
	name_video text,
	date_publication date,
	during int,
	comments_id uuid references video_data."comments"
);

create table if not exists video_data.users (
	id uuid primary key default uuid_generate_v4(),
	user_name text,
	date_registrated date
);




create table if not exists video_data.user_video(
	user_id uuid references video_data.users,
	video_id uuid references video_data.videos,
	primary key(user_id, video_id)
);

INSERT INTO video_data.comments (comment_text, date_publication, count_likes)
VALUES
    ('Great video!', '2024-04-17', 10),
    ('Nice content', '2024-04-16', 5),
    ('Interesting video', '2024-04-15', 8);


INSERT INTO video_data.videos (name_video, date_publication, during, comments_id)
VALUES
    ('Video 1', '2024-04-17', 300, (SELECT id FROM video_data.comments ORDER BY RANDOM() LIMIT 1)),
    ('Video 2', '2024-04-16', 240, (SELECT id FROM video_data.comments ORDER BY RANDOM() LIMIT 1)),
    ('Video 3', '2024-04-15', 180, (SELECT id FROM video_data.comments ORDER BY RANDOM() LIMIT 1));

INSERT INTO video_data.users (user_name, date_registrated)
VALUES
    ('user1', '2024-04-17'),
    ('user2', '2024-04-16'),
    ('user3', '2024-04-15');


INSERT INTO video_data.user_video (user_id, video_id)
VALUES
    ((SELECT id FROM video_data.users where user_name = 'user1'), (SELECT id FROM video_data.videos where name_video = 'Video 1')),
    ((SELECT id FROM video_data.users where user_name = 'user2'), (SELECT id FROM video_data.videos where name_video = 'Video 2')),
    ((SELECT id FROM video_data.users where user_name = 'user2'), (SELECT id FROM video_data.videos where name_video = 'Video 3'));