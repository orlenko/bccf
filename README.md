BCCF
====

VCN BCCF Project



Dev Setup
------------

 * Create a virtual environment for mezzanine-based bccf project: mkvirtualenv bccf
 * Run `pip install mezzanine south PIP`
 * Create local_settings.py based on local_settings_sample.py
 * Run `./manage.py syncdb`
 * Run `./manage.py migrate`
 * Run `./manage.py runserver`
 * You are running your server!
