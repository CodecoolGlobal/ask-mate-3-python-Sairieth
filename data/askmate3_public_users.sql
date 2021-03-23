create table users
(
    id                       serial not null
        constraint users_pkey
            primary key,
    username                 text
        constraint users_username_key
            unique,
    password                 bytea,
    registration_date        timestamp,
    count_of_asked_questions integer,
    count_of_answers         integer,
    count_of_comments        integer,
    reputation               integer
);

alter table users
    owner to kprohaszka;

INSERT INTO public.users (id, username, password, registration_date, count_of_asked_questions, count_of_answers, count_of_comments, reputation) VALUES (1, 'rusty@venture.com', '$2b$12$t9rmAiR.sYPJersBhDRByu9vyTWLtQLM4OvQCuc2S2kivWHEgTwyS', '1600-01-01 00:00:00.000000', 1, 1, 1, 1);