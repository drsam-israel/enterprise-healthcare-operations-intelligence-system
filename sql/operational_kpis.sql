-- Enterprise Healthcare Operations Intelligence System
-- Operational KPI Analytics

SELECT
    COUNT(*) AS total_admissions,
    AVG(length_of_stay_days) AS average_los,
    AVG(ed_wait_time_minutes) AS average_ed_wait_time,
    AVG(capacity_pressure_score) AS average_capacity_pressure,
    SUM(total_cost_usd) AS total_operational_cost
FROM hospital_operations_dataset;