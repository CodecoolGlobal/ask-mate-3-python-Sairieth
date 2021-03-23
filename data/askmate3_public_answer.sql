create table answer
(
    id              serial not null
        constraint pk_answer_id
            primary key,
    submission_time timestamp,
    vote_number     integer,
    question_id     integer
        constraint fk_question_id
            references question,
    message         text,
    image           text
);

alter table answer
    owner to kprohaszka;

INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image) VALUES (1, '2017-04-28 16:49:00.000000', 4, 1, 'You need to use brackets: my_list = []', null);
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image) VALUES (2, '2017-04-25 14:42:00.000000', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg');
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image) VALUES (47, '2021-03-11 11:41:00.000000', 0, 2, 'gyuuyhuh', 'None');
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image) VALUES (48, '2021-03-11 13:28:00.000000', 0, 39, 'rqegqergqreg', 'static/uploads/955649');
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image) VALUES (49, '2021-03-11 13:28:00.000000', 0, 39, 'rqgqregreqg', 'static/uploads/381302');
INSERT INTO public.answer (id, submission_time, vote_number, question_id, message, image) VALUES (50, '2021-03-11 13:29:00.000000', 0, 39, 'gregreg', 'static/uploads/431115');