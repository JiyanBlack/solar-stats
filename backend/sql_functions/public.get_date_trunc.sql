DROP FUNCTION IF EXISTS public.get_date_trunc;

CREATE OR REPLACE FUNCTION public.get_date_trunc(
    ts timestamptz,
    gap int
)
    RETURNS timestamptz
AS
$$
DECLARE
    trunced_date timestamptz;
BEGIN
    IF gap < 60 THEN
        trunced_date = date_trunc('hour'::text, ts) + date_part('minute', ts)::int / gap * gap * interval '1 minute';
    ELSEIF gap < 1440 THEN
        trunced_date = date_trunc('hour'::text, ts);
    ELSEIF gap < 10080 THEN
        trunced_date = date_trunc('day'::text, ts);
    ELSEIF gap < 282240 THEN
        trunced_date = date_trunc('week'::text, ts);
    ELSE
        trunced_date = date_trunc('month'::text, ts);
    END IF;
    RETURN trunced_date;
END
$$ STABLE LANGUAGE plpgsql;