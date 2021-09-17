-- migrate:up
create table organizations
(
    id               bigint not null constraint organizations_pkey primary key,
    date_created     timestamp not null,
    date_updated     timestamp,
    name             varchar(255)
);

create table hotels
(
    id               bigint    not null constraint hotels_pkey primary key,
    date_created     timestamp not null,
    date_updated     timestamp,
    hotel_name       varchar(255) unique,
    address          varchar(255),
    organization_id  bigint references organizations
);

create table reviewers
(
    id              bigint    not null constraint reviewers_pkey primary key,
    date_created    timestamp not null,
    date_updated    timestamp,
    name            varchar(255),
    address         varchar(255)
);

create table reviews
(
    id              bigint    not null constraint reviews_pkey primary key,
    date_created    timestamp not null,
    date_updated    timestamp,
    title           varchar(255),
    full_review     text,
    review_date     varchar(10),
    rating          integer,
    hotel_id        bigint references hotels,
    reviewer_id     bigint references reviewers
);

create sequence organizations_seq;
create sequence hotels_seq;
create sequence reviewers_seq;
create sequence reviews_seq;

-- migrate:down
drop table organizations cascade ;
drop table hotels cascade ;
drop table reviews cascade ;
drop table reviewers cascade ;
drop sequence reviewers_seq;
drop sequence reviews_seq;
drop sequence hotels_seq;
drop sequence organizations_seq;
