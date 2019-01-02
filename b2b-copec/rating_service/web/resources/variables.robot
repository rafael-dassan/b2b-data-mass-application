*** Variables ***
#==============================GENERAL=====================
${BROWSER}                      chrome
${MS_RATING_URL}                https://b2b-services-qa.westeurope.cloudapp.azure.com/v1/ratings
${JWT_ADMIN}                    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNjE2MjM5MDIyLCJpYXQiOjE1MTYyMzkwMjIsInVwZGF0ZWRfYXQiOjExMTExMTEsIm5hbWUiOiJ1c2VyQGFiLWluYmV2LmNvbSIsImFjY291bnRJRCI6IjAwMTAwMDEwMDEiLCJ1c2VySUQiOiIyMTE4Iiwicm9sZXMiOlsiUk9MRV9BRE1JTiJdfQ.BR_K5exHOoaqOXNfVZgVCwNAczJ0vKCYVInL15c_wZY

#==============================BAVARIA=====================
${URL_BAVARIA}                  https://qa-conv-bavaria.abi-sandbox.net/customer/account/login/
${EMAIL_BAVARIA}                0010560934@mailinator.com
${PASSWORD_BAVARIA}             Bienvenido1
${JWT_BAVARIA}                  Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTUzOTkwNDAwLCJpYXQiOjE1NDUwNjg5ODUsInVwZGF0ZWRfYXQiOjE1NDUwNjg5ODUsIm5hbWUiOiIwMDEwNTYwOTM0QG1haWxpbmF0b3IuY29tIiwiYWNjb3VudElEIjoiMDAxMDU2MDkzNCIsInVzZXJJRCI6IjIxMjUiLCJyb2xlcyI6WyJST0xFX0NVU1RPTUVSIl19.ZT3m07KLk-B-r0LY6Ky8Kt08gAPtjkfGRv7N4I06Hvc
${CUSTID_BAVARIA}               0010560934
${USE_CASE_ID_BAVARIA}          CO000001161

${EMAIL_BAVARIA_SINGLE}         10391513@mailinator.com
${PASSWORD_BAVARIA_SINGLE}      Bienvenido1
${JWT_BAVARIA_SINGLE}           Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTUzOTkwNDAwLCJpYXQiOjE1NDUwNjg5ODUsInVwZGF0ZWRfYXQiOjE1NDUwNjg5ODUsIm5hbWUiOiIxMDM5MTUxM0BtYWlsaW5hdG9yLmNvbSIsImFjY291bnRJRCI6IjAwMTAzOTE1MTMiLCJ1c2VySUQiOiIyMTI1Iiwicm9sZXMiOlsiUk9MRV9DVVNUT01FUiJdfQ.7wX3_QaBzOhqmZyEazMK2khxPvSrhVKKJR-7Sj3AkCk
${CUSTID_BAVARIA_SINGLE}        0010391513
${USE_CASE_ID_BAVARIA_SINGLE}   CO000001157

${COUNTRY_BAVARIA}              CO

#==============================BACKUS=====================
${URL_BACKUS}                   https://qa-conv-backus.abi-sandbox.net/customer/account/login/
${EMAIL_BACKUS}                 0010001001@mailinator.com
${PASSWORD_BACKUS}              Bienvenido1
${JWT_BACKUS}                   Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTUzOTkwNDAwLCJpYXQiOjE1NDUwNjg5ODUsInVwZGF0ZWRfYXQiOjE1NDUwNjg5ODUsIm5hbWUiOiIwMDEwMDAxMDAxQG1haWxpbmF0b3IuY29tIiwiYWNjb3VudElEIjoiMDAxMDAwMTAwMSIsInVzZXJJRCI6IjIxMjUiLCJyb2xlcyI6WyJST0xFX0NVU1RPTUVSIl19.I9AkGL9Dx4EP9GU_IKO-OjTQEr8Hukl_hAPt0bwhggo
${CUSTID_BACKUS}                0010001001
${USE_CASE_ID_BACKUS}           PE000002799

${EMAIL_BACKUS_SINGLE}          10185302@mailinator.com
${PASSWORD_BACKUS_SINGLE}       Bienvenido1
${JWT_BACKUS_SINGLE}            Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTUzOTkwNDAwLCJpYXQiOjE1NDUwNjg5ODUsInVwZGF0ZWRfYXQiOjE1NDUwNjg5ODUsIm5hbWUiOiIxMDE4NTMwMkBtYWlsaW5hdG9yLmNvbSIsImFjY291bnRJRCI6IjAwMTAxODUzMDIiLCJ1c2VySUQiOiIyMTI1Iiwicm9sZXMiOlsiUk9MRV9DVVNUT01FUiJdfQ.8hNNIL5Ymi52iBhUJtgMJn8lMe1lzmS_ISUu0bg3u2Y
${CUSTID_BACKUS_SINGLE}         0010185302
${USE_CASE_ID_BACKUS_SINGLE}    PE000002783

${COUNTRY_BACKUS}               PE

#==============================MITIENDA=====================
${URL_MITIENDA}                 https://qa-conv-nacional.abi-sandbox.net/customer/account/login/
${EMAIL_MITIENDA}               11817172@mailinator.com
${PASSWORD_MITIENDA}            Bienvenido1
${JWT_MITIENDA}                 Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTUzOTkwNDAwLCJpYXQiOjE1NDUwNjg5ODUsInVwZGF0ZWRfYXQiOjE1NDUwNjg5ODUsIm5hbWUiOiIxMTgxNzE3MkBtYWlsaW5hdG9yLmNvbSIsImFjY291bnRJRCI6IjAwMTE4MTcxNzIiLCJ1c2VySUQiOiIyMTI1Iiwicm9sZXMiOlsiUk9MRV9DVVNUT01FUiJdfQ.5L77aVvHJuLT6p-5rAhR5VXSOwoF7rRKvju7qatjOX0
${CUSTID_MITIENDA}              0011817172
${USE_CASE_ID_MITIENDA}         EQ000000525

${EMAIL_MITIENDA_SINGLE}        11804523@mailinator.com
${PASSWORD_MITIENDA_SINGLE}     Bienvenido1
${JWT_MITIENDA_SINGLE}          Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhYi1pbmJldiIsImF1ZCI6ImFiaS1taWNyb3NlcnZpY2VzIiwiZXhwIjoxNTUzOTkwNDAwLCJpYXQiOjE1NDUwNjg5ODUsInVwZGF0ZWRfYXQiOjE1NDUwNjg5ODUsIm5hbWUiOiIxMTgwNDUyM0BtYWlsaW5hdG9yLmNvbSIsImFjY291bnRJRCI6IjAwMTE4MDQ1MjMiLCJ1c2VySUQiOiIyMTI1Iiwicm9sZXMiOlsiUk9MRV9DVVNUT01FUiJdfQ.VhnD2HeMf0sFgMO8K50q4Vzz_6TtNsbzHldgy8GcTtY
${CUSTID_MITIENDA_SINGLE}       0011804523
${USE_CASE_ID_MITIENDA_SINGLE}  EQ000000523

${COUNTRY_MITIENDA}             EC