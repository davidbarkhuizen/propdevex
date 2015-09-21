SELECT conname, pg_catalog.pg_get_constraintdef(r.oid, true) as condef
FROM pg_catalog.pg_constraint r
WHERE r.conrelid = 'frp_property'::regclass AND r.contype = 'u' ORDER BY 1;

ALTER TABLE "frp_property" DROP CONSTRAINT "frp_property_name_key";