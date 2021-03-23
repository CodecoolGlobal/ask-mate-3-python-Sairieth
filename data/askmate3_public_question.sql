create table question
(
    id              serial not null
        constraint pk_question_id
            primary key,
    submission_time timestamp,
    view_number     integer,
    vote_number     integer,
    title           text,
    message         text,
    image           text
);

alter table question
    owner to kprohaszka;

INSERT INTO public.question (id, submission_time, view_number, vote_number, title, message, image) VALUES (0, '2017-04-28 08:29:00.000000', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', null);
INSERT INTO public.question (id, submission_time, view_number, vote_number, title, message, image) VALUES (39, '2021-03-11 13:28:00.000000', 7, 0, 'tgreg', 'regrqegqreg', 'static/uploads/822740');
INSERT INTO public.question (id, submission_time, view_number, vote_number, title, message, image) VALUES (1, '2017-04-29 09:19:00.000000', 17, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png');
INSERT INTO public.question (id, submission_time, view_number, vote_number, title, message, image) VALUES (2, '2017-05-01 10:41:00.000000', 1415, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', null);