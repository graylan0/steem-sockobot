# steem-sockobot
A steem bot for discord servers. Handles basic functionality and allows for easy addition of commands.

### MIND THAT THE BOT IS CURRENTLY WRITTEN IN POLISH AND WILL BE TRANSLATED BEFORE LAUNCH.

## Commands:

* **$price <SBD/STE/BTC>** - shows the current price of one of these coins (via coinmarketcap).
![price.png](https://i.imgur.com/zVYJJlN.png)
* **$payout <NICKNAME>** - shows the potential payout of given user's posts that have yet to pay out (7 days old or younger).
![payout.png](https://i.imgur.com/nl0RQZm.png)
* **$ping** - checks if the bot is responsive.
![ping.png](https://i.imgur.com/zSHbGgk.png)

## Other functionality:

* Upvote steem posts using provided **private active key** when a moderator uses a ☑ (default) on a steem post link.
![upvoter.png](https://i.imgur.com/dIrxW8w.png)

## Known bugs:
* The bot will crash if $payout is used on a user with really high reputation, like the top3 witnesses. This is easy to reproduce but I have yet to find a fix to it. Contributions are welcome.
