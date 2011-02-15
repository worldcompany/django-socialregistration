DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

if TEST_ROLE == 'objectconnect':
    DATABASES['default']['NAME'] = 'socialregtests_objectconnect'
elif TEST_ROLE == 'userconnect_generate':
    DATABASES['default']['NAME'] = 'socialregtests_generateusername'
elif TEST_ROLE == 'userconnect_manual':
    DATABASES['default']['NAME'] = 'socialregtests_manualusername'
