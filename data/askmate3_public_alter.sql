ALTER TABLE question
ADD user_id integer;

ALTER TABLE answer
ADD user_id integer;

ALTER TABLE comment
ADD user_id integer;