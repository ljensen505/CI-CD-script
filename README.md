A simple script to rebuild and redeploy an app using github webhooks and systemd.

Further documentation coming soon. Things to note though:

- update constants in main.py
- this script assumes gunicorn will be used for production server
- it may be necessary to tell your system to not require sudo when running this script. 
- See: `visudo`