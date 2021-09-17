-- migrate:up

alter table reviews add column word_count integer default 0;


-- migrate:down

alter table reviews drop column word_count;
