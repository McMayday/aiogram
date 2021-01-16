create table instagram
  (
    username text,
    created_at date,
    updated_at date,
    in_blacklist boolean,
    user_count integer,
    id serial primary key
  );

alter table instagram
  owner to postgres;


create table usernames
  (
    id serial primary key,
    username text,
    chat_id text,
    users_id integer references instagram(id)
  );

  alter table usernames
    owner to postgres;



create table users
  (
    chat_id bigint not null
      constraint users_pk
          primary key,
    username text,
    in_blacklist boolean,
    full_name text,
    active boolean,
    id serial not null
  );

  alter table users
    owner to postgres;

  create unique index users_id_index
    on users (id);
