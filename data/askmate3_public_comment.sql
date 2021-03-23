create table comment
(
    id              serial not null
        constraint pk_comment_id
            primary key,
    question_id     integer
        constraint fk_question_id
            references question,
    answer_id       integer
        constraint fk_answer_id
            references answer,
    message         text,
    submission_time timestamp,
    edited_count    integer
);

alter table comment
    owner to kprohaszka;

INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count) VALUES (1, 0, null, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00.000000', null);
INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count) VALUES (2, null, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00.000000', null);
INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count) VALUES (7, null, 47, 'nijbnhin', '2021-03-11 11:46:07.648801', 0);
INSERT INTO public.comment (id, question_id, answer_id, message, submission_time, edited_count) VALUES (8, 2, null, 'ergerg', '2021-03-11 11:52:17.447974', 0);