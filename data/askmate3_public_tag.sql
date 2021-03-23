create table tag
(
    id   serial not null
        constraint pk_tag_id
            primary key,
    name text
);

alter table tag
    owner to kprohaszka;

INSERT INTO public.tag (id, name) VALUES (1, 'python');
INSERT INTO public.tag (id, name) VALUES (2, 'sql');
INSERT INTO public.tag (id, name) VALUES (3, 'css');