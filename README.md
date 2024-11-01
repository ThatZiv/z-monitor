# z-monitor

![logo](static/logo.png)

z-monitor is a standalone, cross-platform monitoring tool used for computers located within the same network. Built with Python, [Flask](https://flask.palletsprojects.com/en/stable/), [HTMX](https://htmx.org/), and more stuff I can't remember atm.
Features include:

- Admin GUI Interface
- Key logger
- Process monitor
- Time tracking
- System resource monitor
- Alerting
- More

![imgpreview](https://i.imgur.com/FeghT9v.png)

## TODO

- [x] Add sqlite for persitent time tracking
- [x] make master password
- [x] **Fix recursive cursor issue**
  - [ ] test if these [locks](https://stackoverflow.com/questions/26629080/python-and-sqlite3-programmingerror-recursive-use-of-cursors-not-allowed) ruin or defer any sort of tracking
  - If it does, should I try a [queue](https://www.geeksforgeeks.org/queue-in-python/) instead?
- [ ] log activity changes (processes list?)
- [x] Continue get_logs custom filter for type w/ htmx frontend (use events?
- [ ] way to do headless initialization (no prompt for password on first run)
  - [ ] make config -> to json file that gets removed **after** first run
  - [ ] or just build out a simple gui?
- [x] implement flask api
- [x] implement web interface
  - [ ] set time
  - [ ] change password
  - [ ] use ssl
  - [x] pass pc specs to (polling route)
- [ ] ~~implement websockets for real-time updates~~
- [ ] only allow once instance to run at a time

## Caveats

- Deleting the db file will reset the timer and password
- Only works on the same local network (intentional caveat)
