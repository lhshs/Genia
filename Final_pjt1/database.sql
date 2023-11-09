-- Table: public.FirstLine

DROP TABLE IF EXISTS public."FirstLine";

CREATE TABLE IF NOT EXISTS public."FirstLine"
(
	"Date" Time,
    image bytea
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."FirstLine"
    OWNER to postgres;