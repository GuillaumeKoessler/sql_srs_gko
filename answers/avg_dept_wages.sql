SELECT
    name,
    wage,
    department,
    AVG(wage)
        OVER(
            PARTITION BY department
        ) as mean_dpt_wage
FROM
    wages
ORDER BY
    mean_dpt_wage