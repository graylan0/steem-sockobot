# steem-sockobot
A Steem bot for discord servers. Handles basic functionality and allows for easy addition of commands.

SockoBot aims to be the most open-source friendly steem related Discord bot out there. By introducing a wide variety of commands and letting the owner easily remove them and/or add new functionality, the bot can easily be adapted to work in any Steem community Discord server. The bot is written in a beginner friendly way - the commands are all stored under a single function and so is most of the funcionality, for simplicity's sake, not even classes are present so **anyone** with basic Python knowledge can easily add extra functionality with the help of [steem-python's](http://steem.readthedocs.io/en/latest/index.html) and [discord.py's](https://discordpy.readthedocs.io/en/latest/) documentation respectively.

## Usage:

To find out how to add SockoBot to your own Discord server go [here](https://github.com/Jestemkioskiem/steem-sockobot/blob/master/HOW_TO_DEPLOY.md) and follow the tutorial.

## Commands:

#### $convert `<value>` `<coin1>` `<coin2>`
Convert the value of a given coin to its equal value in another coin.

Example usage:
```
$convert 1000 steem-dollars bitcoin

You can receive 0.5727615537891285 **bitcoin** for 1000 **steem-dollars**.
```

---

#### $delegate `<delegator>` `<value>` `<delegatee>`
Delegate SP from delegator to delegatee.

Example usage:

```
$delegate amosbastian 0.1 jestemkioskiem

To delegate using SteemConnect, click the link below: 
https://v2.steemconnect.com/sign/delegateVestingShares?delegator=amosbastian&delegatee=jestemkioskiem&vesting_shares=0.1%20SP
```

---

#### $payout `<username>` `<days>` 
Shows the potential payout of a given user's posts that have yet to pay out. The days argument is used to define a time period (up to 7 days) in which the payouts should be counted. The payout's value is counted based on coinmarketcap's prices.

Example usage:
```
$payout jestemkioskiem 7
``` 

![](https://i.imgur.com/yhshKbe.png)

---

#### $ping 
Pings the bot to see if it is responsive.
![ping.png](https://i.imgur.com/6kWkzjO.png)

---

#### $price `<coin>`
Shows the current price of one of the given coin. The name of the coin must be the same as on https://coinmarketcap.com/.

Example usage:

```
$price steem-dollars
    
The current price of steem-dollars is: 5.35649 USD.
```

---

#### $register `<username>`
Gives user a memo with which, by sending a set amount of STEEM/SBD, the user will be able to gain a role on the discord server. 

Example usage:

```
$register jestemkioskiem
```

![](https://camo.githubusercontent.com/1d2f42f41dc0952608ab30a096ecc9313017fe1f/68747470733a2f2f692e696d6775722e636f6d2f506948775942702e706e67)

---

#### $sp `<username>`
Shows the current STEEM POWER and delegations of the user.

Example usage:

```
$sp jestemkioskiem
```

![](https://i.imgur.com/QnbHjgW.png)

---

#### $vote `<username>`
Shows the user's estimated worth of an upvote at 100% voting power and current voting power.

Example usage:

```
$vote jestemkioskiem
```

![](https://i.imgur.com/VXfD5EE.png)

---

#### $wallet `<username>`
Shows the user's current STEEM, STEEM POWER, STEEM DOLLARS, estimated account value and estimated worth of a 100% VP upvote.

Example usage:

```
$wallet jestemkioskiem
```

![](https://i.imgur.com/ck7gwbS.png)

---

## Other functionality:

#### Upvote steem posts
Upvotes posts using a provided **private active key** when a moderator uses a ☑ (default) on a Steem post link.
![stats.png](https://steemitimages.com/0x0/https://res.cloudinary.com/hpiynhbhq/image/upload/v1514307010/gq6pewla6ild673qpddn.png)

#### Automatically remove old posts from allowed channels
You can alter the age/channels in the code.

#### Check if the author of a message/reaction has moderating privilages
For that, use the **is_mod()** function.



SockoBot is copyrighted under the [MIT LICENSE](https://github.com/Jestemkioskiem/steem-sockobot/blob/master/LICENSE) by the owner of the [Jestemkioskiem](https://github.com/Jestemkioskiem/) Account © 2018.
