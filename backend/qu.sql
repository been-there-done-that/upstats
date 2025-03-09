SELECT
    table_name,
    pg_size_pretty( pg_total_relation_size(quote_ident(table_name))),
    pg_total_relation_size(quote_ident(table_name))
FROM
    information_schema.tables
WHERE
    table_schema = 'public'
ORDER BY
    pg_total_relation_size(quote_ident(table_name)) DESC;


SELECT *, pg_size_pretty(total_bytes) AS total
     , pg_size_pretty(index_bytes) AS INDEX
     , pg_size_pretty(toast_bytes) AS toast
     , pg_size_pretty(table_bytes) AS table_size
FROM (
         SELECT *, total_bytes-index_bytes-COALESCE(toast_bytes,0) AS table_bytes
         FROM (
                  SELECT c.oid,nspname AS table_schema, relname AS TABLE_NAME
                       , c.reltuples AS row_estimate
                       , pg_total_relation_size(c.oid) AS total_bytes
                       , pg_indexes_size(c.oid) AS index_bytes
                       , pg_total_relation_size(reltoastrelid) AS toast_bytes
                  FROM pg_class c
                           LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
                  WHERE relkind = 'r'
              ) a
     ) a
where a.table_schema='public' ORDER BY total_bytes DESC;
