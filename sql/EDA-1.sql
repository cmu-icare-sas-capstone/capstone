use capstone;
-- select m.ccs_procedure_code, m.apr_drg_code, c.apr_drg_code, c.ccs_diagnosis_code from 
-- CMS_Medicare_Cancer_Alley_DATA1_4_ m
-- join Comorbidities_for_COVID_Synthetic_data c on m.apr_drg_code = c.apr_drg_code
-- where m.apr_drg_code = 465;

-- select m.index, m.apr_drg_code, c.covid_hosp from 
-- CMS_Medicare_Cancer_Alley_DATA1_4_ m
-- join Comorbidities_for_COVID_Synthetic_data c on m.apr_drg_code = c.apr_drg_code
-- where covid_hosp = true;


-- SELECT distinct t1.apr_drg_code as apr_drg, t1.ccs_diagnosis_code as ccs_diagnosis, t1.covid_hosp, t2.covid_hosp
-- FROM capstone.Diagnosis_Review t1
-- join 
-- (SELECT distinct apr_drg_code, covid_hosp, ccs_diagnosis_code FROM capstone.Diagnosis_Review) t2
-- on t1.apr_drg_code = t2.apr_drg_code
-- and t1.ccs_diagnosis_code = t2.ccs_diagnosis_code
-- where t1.covid_hosp != t2.covid_hosp;

SELECT distinct t1.apr_drg_code as apr_drg, t1.covid_hosp, t2.covid_hosp
FROM capstone.Diagnosis_Review t1
join
(SELECT distinct apr_drg_code, covid_hosp, ccs_diagnosis_code FROM capstone.Diagnosis_Review) t2
on t1.apr_drg_code = t2.apr_drg_code
where t1.covid_hosp > t2.covid_hosp;

-- SELECT distinct apr_drg_code, covid_hosp, ccs_diagnosis_code FROM capstone.Diagnosis_Review
-- WHERE apr_drg_code = 45

-- select count(*) from
-- (select distinct apr_drg_code, ccs_diagnosis_code from capstone.Diagnosis_Review) as t;
