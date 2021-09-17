-- migrate:up

create table locations
(
    id           bigint    not null
        constraint locations_pkey primary key,
    date_created timestamp not null,
    date_updated timestamp,
    address      varchar(255),
    city         varchar(255),
    state        varchar(255),
    country      varchar(255)
);

create sequence locations_seq;
ALTER TABLE hotels
    add location_id bigint,
    ADD CONSTRAINT fk_hotel_location
        FOREIGN KEY (location_id) REFERENCES locations (id);
ALTER TABLE reviewers
    add location_id bigint,
    ADD CONSTRAINT fk_reviewer_location
        FOREIGN KEY (location_id) REFERENCES locations (id);


-- migrate:down


drop table locations cascade;
drop sequence locations_seq;
alter table hotels drop column location_id;
alter table reviewers drop column location_id;
