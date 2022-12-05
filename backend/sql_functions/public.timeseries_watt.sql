/*
SQL function to generate aggregated watt data for a given time range by a given gap in minutes, and return the result as a jsonb object.
The function is used to generate the watt data for the timeseries chart in the frontend.
The function is called by the following API:
GET /api/v1/timeseries/watt?start_time=2022-12-05T03:26:06.909086Z&end_time=2022-12-05T05:42:06.102965Z&gap=5&timezone=Australia/Perth
The function returns a jsonb object with the following structure:
{
    "timeslot": "2022-12-05T03:30:00+08:00",
    "avg_watt": 0.0,
    "percentile_01th": 0.0,
    "percentile_50th": 0.0,
    "percentile_99th": 0.0
}
*/

DROP FUNCTION IF EXISTS public.timeseries_watt;

CREATE OR REPLACE FUNCTION public.timeseries_watt(
    query_start_time timestamptz, -- start time of query
    query_end_time timestamptz, -- end time of query
    gap integer, -- aggregated gap in minutes
    intz text -- timezone
)
    RETURNS TABLE
            (
                result jsonb
            )
    LANGUAGE plpgsql
    STABLE
AS
$function$
DECLARE
    start_time timestamptz;
    end_time   timestamptz;
BEGIN
    SELECT DATE_TRUNC('hour' :: TEXT, query_start_time) into start_time;
    SELECT DATE_TRUNC('hour' :: TEXT, query_end_time + INTERVAL '30 minute') into end_time;

    RETURN QUERY
        WITH watt_data AS (SELECT ts, watt
                           FROM realtime_watt
                           WHERE ts >= start_time
                             AND ts <= end_time ORDER BY ts),
             agg_watt AS (SELECT get_date_trunc(ts, gap)      AS timeslot,
                                 round(avg(watt)::numeric, 2) AS avg_watt,
                                 round(percentile_cont(0.99) WITHIN GROUP (ORDER BY watt ASC)::numeric,
                                       2)                     AS percentile_99th,
                                 round(percentile_cont(0.50) WITHIN GROUP (ORDER BY watt ASC)::numeric,
                                       2)                     AS percentile_50th,
                                 round(percentile_cont(0.01) WITHIN GROUP (ORDER BY watt ASC)::numeric,
                                       2)                     AS percentile_01th
                          FROM watt_data
                          GROUP BY get_date_trunc(ts, gap))

        SELECT json_agg(final_result)::jsonb
        FROM (SELECT timeslot AT TIME ZONE intz, avg_watt, percentile_01th, percentile_50th, percentile_99th
              FROM agg_watt) AS final_result;
END
$function$;

-- SELECT * FROM timeseries_watt('2022-12-05 03:26:06.909086 +00:00', '2022-12-05 05:42:06.102965 +00:00', 5, 'Australia/Perth');