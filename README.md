# steem-sockobot
A steem bot for discord servers. Handles basic functionality and allows for easy addition of commands.

SockoBot aims to be the most open-source friendly steem related Discord bot out there. By introducing a wide variety of commands and letting the owner easily remove them and/or add new functionality, the bot can easily be adapted to work in any Steem Community discord server. The bot is written in a beginner friendly way - the commands are all stored under a single function and so is most of the funcionality, for simplicity's sake, not even classes are present so **anyone** with basic python knowledge can easily add extra functionality with the help of [steem-python's](http://steem.readthedocs.io/en/latest/index.html) and [discord.py's](https://discordpy.readthedocs.io/en/latest/) documentations.

## Usage:

```TOKEN=<BOT TOKEN> KEY=<PRIVATE POSTING KEY> NAME=<STEEM USERNAME> python3 bot.py``` to run SockoBot

The monitor.sh file is currently used to safely deploy the bot to a cloud server without keeping private tokens and keys in the code. It will most likely be removed upon launch, as every developer has his way of handling this. This file is also present for crash-control. If the bot crashes, for any reason, it will reboot immediately. To use that, you need to run monitor.sh with the TOKEN, KEY and NAME values as arguments in that order.

## Commands:

### **$price <SBD/STE/BTC>**
Shows the current price of one of these coins (via coinmarketcap). This can easily be expanded to any coin supported by coinmarketcap.
![price.png](https://i.imgur.com/IVmgejL.png)

### **$payout \<NICKNAME> <DAYS>** 
Shows the potential payout of given user's posts that have yet to pay out. The days argument is used to define a time period (up to 7 days) in which the payouts should be counted. The payout's value is counted based on coinmarketcap's prices.
![payout.png](https://i.imgur.com/ILoilD8.png)

### **$register \<NICKNAME>**
Gives user a memo with which, by sending a set ammount of STEEM/SBD, the user will be able to gain a role on the discord server. 
![register.png](https://i.imgur.com/PiHwYBp.png)

### **$ping** 
Checks if the bot is responsive.
![ping.png](https://i.imgur.com/6kWkzjO.png)


## Other functionality:

* Upvote steem posts using a provided **private active key** when a moderator uses a ☑ (default) on a steem post link.
![stats.png](https://steemitimages.com/0x0/https://res.cloudinary.com/hpiynhbhq/image/upload/v1514307010/gq6pewla6ild673qpddn.png)

* Remove old posts from allowed channels.

* Check if the author of a message/reaction has moderating privilages.

## Known bugs:
* 
