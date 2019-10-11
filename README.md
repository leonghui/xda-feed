# xda-feed
A simple Python script to generate a [JSON Feed](https://github.com/brentsimmons/JSONFeed) for threads on [XDA Developers](https://www.xda-developers.com).

Uses the [official API](https://api.xda-developers.com/explorer/) and served over [Flask!](https://github.com/pallets/flask/)

Use the [Docker build](https://hub.docker.com/r/leonghui/xda-feed) to host your own instance.

Access the feed using the URL: `http://<host>/xda-feed/{threadid}/`

E.g.
```
Forum thread:
https://forum.xda-developers.com/android/development/wireguard-rom-integration-t3711635

Feed link:
http://<host>/xda-feed/3711635/
```

Tested with:
- [Nextcloud News App](https://github.com/nextcloud/news)
