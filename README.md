# Dota-Replay-Archiver
A set of lambda functions written in Python to periodically download and save the replay .dem files of new professional DOTA 2 matches into AWS S3 buckets. 

### Why?
Replay files are only hosted for about 14 days (varies based on game volume) on Valve's CDN servers. After that, they're gone for good unless they're saved somewhere else.

### How it works:
`matchid-finder` is called hourly (or however often you'd like) by a CloudWatch event. When called, it scrapes DOTA 2 match IDs from [this tracker](http://www.dota2protracker.com/), and sends the IDs of matches that do not already exist in the target S3 bucket to an SNS stream.

`replay-downloader` is called by the SNS stream with a match ID included as a parameter in each function call. The function queries [OpenDota's API](https://docs.opendota.com/) to retrieve the datacenter cluster ID and replay salt that correspond to the match ID. These two pieces of information are required to locate the replay on Valve's CDN. It then downloads the replay file from Valve's servers, and saves it to a designated S3 bucket.
