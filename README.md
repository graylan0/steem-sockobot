# steem-sockobot
A steem bot for discord servers. Handles basic functionality and allows for easy addition of commands.

```TOKEN=<BOT TOKEN> KEY=<PRIVATE POSTING KEY> NAME=<STEEM USERNAME> python3 bot.py``` to run SockoBot

The monitor.sh file is currently used to safely deploy the bot to a cloud server without keeping private tokens and keys in the code. It will most likely be removed upon launch, as every developer has his way of handling this.

## Commands:

* **$price <SBD/STE/BTC>** - shows the current price of one of these coins (via coinmarketcap).
![price.png](https://i.imgur.com/zVYJJlN.png)
* **$payout \<NICKNAME>** - shows the potential payout of given user's posts that have yet to pay out.
![payout.png](https://i.imgur.com/nl0RQZm.png)
* **$ping** - checks if the bot is responsive.
![ping.png](https://i.imgur.com/zSHbGgk.png)

## Other functionality:

* Upvote steem posts using a provided **private active key** when a moderator uses a ☑ (default) on a steem post link.
![stats.png](https://steemitimages.com/0x0/https://res.cloudinary.com/hpiynhbhq/image/upload/v1514307010/gq6pewla6ild673qpddn.png)
![upvoter.png](https://i.imgur.com/dIrxW8w.png)

## Known bugs:
* The bot will crash if $payout is used on a user with really high reputation, like the top3 witnesses. This is easy to reproduce but I have yet to find a fix to it. Contributions are welcome.
