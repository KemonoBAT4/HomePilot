# HomePilot
HomePilot is a personal remote control and automation platform for managing your home PC and services. Wake, control, launch applications, switch profiles, access files, and automate your workspace from anywhere — with AI-powered orchestration.




##
Examples:

Mobile[turn on home pc with the gaming profile] -> home server[recieved info and activates wake on lan] -> home pc[wake on lan + login] -> home pc[this app][opens the selected profile's app]

```
        ----------------
    --->| Mobile (VPN) |        # (turn on the home pc w/ wake on lan)
    |   ----------------
    |          |
    |          V
    |   ---------------
    ----| Home Server |<---     # (sends the wake on lan package)
        ---------------   |
               |          |
               V          |
        ---------------   |
        |   Home PC   |----     # (turns on, logs in and send back response)
        ---------------
```