# notify-me

This is a scheduler to run a specific time at a given time or at a specific interval.

Send me a notification via a specific channel (Pushover, email, sms, etc) when a specific condition is met

I sometimes wants to be notified when:
  - a server is down or a port is closed on a specific IP
  - a machine is running low is diskspace
  - a domain is going to expire soon
  - a certain phrase is found on a website
  - send me my bank account balance every morning

Currently, the following scripts exist:
- ping_test.py
- shell_cmd.py
- socket_open.py
- socket_open.pyc
- sparebanken_account_check.py
- webpage_text.py

A new script can easily be added to this project by simple inheriting Script, and implementing your own: `do_test()` method

More later!

