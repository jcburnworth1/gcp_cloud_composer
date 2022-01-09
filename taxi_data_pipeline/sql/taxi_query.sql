SELECT
*
FROM
`{{ params.project_id }}.{{ params.dataset }}.all_taxi_trips`
WHERE
id IN ('e4424ddc-cc53-446d-bed3-ccae930d4998','a2478b16-9c42-4ba1-bff6-ad0a10ea70ab',
       'ac87056b-0266-422f-81d2-1a6b592bbfdb','6c09c0e4-ce4e-47a5-b5fe-9ce947c2c507',
       '0338ede9-494f-4caa-88dc-91eff3648a3e','e20a954e-baf9-40a2-af84-006c8fe26e0d',
       '7db6a04b-e394-4c0b-9439-efe94ae5ecb9','922e90bf-deca-4ec1-9453-9edc73efc8af',
       '03fd0b86-d3a2-417e-9275-884a0bcaf03c','97499029-8eed-4610-b79b-1c674a20504b')
