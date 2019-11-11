# xda-feed
A simple Python script to generate a [JSON Feed](https://github.com/brentsimmons/JSONFeed) for threads on [XDA Developers](https://www.xda-developers.com).

Uses the [official API](https://api.xda-developers.com/explorer/) and served over [Flask!](https://github.com/pallets/flask/)

Use the [Docker build](https://hub.docker.com/r/leonghui/xda-feed) to host your own instance.

1. Set your timezone as an environment variable (see [docker docs]): `TZ=America/Los_Angeles` 

2. Access the feed using the URL: `http://<host>/?thread_id={id}`

3. Optionally, filter by user names: `http://<host>/?thread_id={id}&usernames={user1,user2}`

E.g.
```
Forum thread:
https://forum.xda-developers.com/android/development/wireguard-rom-integration-t3711635

Feed link:
http://<host>/?thread_id=3711635

Filtered feed link:
http://<host>/?thread_id=3711635&usernames=zx2c4
```

Tested with:
- [Nextcloud News App](https://github.com/nextcloud/news)

[docker docs]:(https://docs.docker.com/compose/environment-variables/#set-environment-variables-in-containers)