-- Capacity & Bed Intelligence

SELECT
    hospital_unit,
    bed_occupancy_status,
    COUNT(*) AS bed_count
FROM hospital_operations_dataset
GROUP BY hospital_unit, bed_occupancy_status
ORDER BY hospital_unit, bed_count DESC;