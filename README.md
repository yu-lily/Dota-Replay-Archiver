# Dota-Replay-Archiver
A set of lambda functions written in Python to periodically download and save the replay .dem files of new professional DOTA 2 matches into AWS S3 buckets. 

### Why?
Replay files are only hosted for about 14 days (varies based on game volume) on Valve's CDN servers. After that, they're gone for good unless you save them like this.

### How it works
scrape DOTA 2 match IDs from [this tracker](http://www.dota2protracker.com/)
