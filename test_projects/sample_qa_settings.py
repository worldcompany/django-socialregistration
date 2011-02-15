# create a copy of this file named qa_settings.py on the root of your PYTHONPATH then fill in the necessary API keys (which need to be different for each app)
# it will be imported by each projects' settings.py and will set the project-specific stuff to keep the settings.py in each project pristine.

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

if TEST_ROLE == 'objectconnect':
    DATABASES['default']['NAME'] = 'socialregtests_objectconnect'
    FACEBOOK_API_KEY = ''
    FACEBOOK_SECRET_KEY = ''
    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET_KEY = ''

elif TEST_ROLE == 'userconnect_generate':
    DATABASES['default']['NAME'] = 'socialregtests_generateusername'
    FACEBOOK_API_KEY = ''
    FACEBOOK_SECRET_KEY = ''
    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET_KEY = ''

elif TEST_ROLE == 'userconnect_manual':
    DATABASES['default']['NAME'] = 'socialregtests_manualusername'
    FACEBOOK_API_KEY = ''
    FACEBOOK_SECRET_KEY = ''
    TWITTER_CONSUMER_KEY = ''
    TWITTER_CONSUMER_SECRET_KEY = ''

else:
    print("No configuration exists for this testing role.")
