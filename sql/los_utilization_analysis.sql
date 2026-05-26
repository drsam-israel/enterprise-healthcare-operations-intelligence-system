-- LOS & Utilization Analytics

SELECT
    hospital_unit,
    AVG(length_of_stay_days) AS average_los,
    COUNT(*) AS patient_volume
FROM hospital_operations_dataset
GROUP BY hospital_unit
ORDER BY average_los DESC;