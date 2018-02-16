![](https://steemit-production-imageproxy-thumbnail.s3.amazonaws.com/U5dred14zXwb47ouJw2YJtYciEktt1K_1680x8400)

Welcome to the steem-sockobot deployment tutorial! Here you will learn how to set up SockoBot on your own Discord server!

# Creating a Discord application

Creating a Discord application is very easy. The first step is to go to [here](https://discordapp.com/developers/applications/me), log in and create a new application. After this you should be greeted by the following page

![](https://i.imgur.com/gqxeDbV.png)

Fill in all the fields and create the application! Once you've done this you should scroll down and bundle a bot user with your application by clicking the "Create a Bot User" button

![](https://i.imgur.com/ZsiNbO4.png)

Now all that is left is getting your bot's token. This can be done by clicking the "click to reveal" link and copying the revealed token.

![](https://i.imgur.com/5lCQ3cR.png)

# Deploying the bot to Discord

Adding your bot to Discord is also relatively straight-forward. To do this we need to clone the repository, add environment variables and edit bot.py. In this tutorial I will assume you are using Ubuntu and know how to edit files using a text editor.

### Cloning the repository

To clone SockoBot's repository and enter its directory execute the following commands in your terminal

```
$ git clone https://github.com/Jestemkioskiem/steem-sockobot
$ cd steem-sockobot
```

### Adding environment variables

To add the environment variables `NAME`, `KEY` and `TOKEN` you simply need to edit your `.bashrc` file. To do this execute the following command in your terminal to open it with gedit, which is the default text editor of the GNOME desktop environment

```
$ gedit ~/.bashrc
```
and add the follow to the end of the file

```
export SB_NAME="your-bots-name"
export SB_KEY="your-bots-key"
export SB_TOKEN="your-bots-token"
```
where `SB_NAME` is a Steemit username, `SB_KEY` is that account's private posting key and `SB_TOKEN` is the bot's token we acquired in the previous section. Once you've done this, save the file and type the following command in your terminal

```
$ source ~/.bashrc
```

### Editing bot.py

Now all that's left is to add your server's ID and the bot's role to `bot.py`. You can find your server's ID by right-clicking your server in the sidebar on Discord, navigating to "Server Settings" and clicking "Widget"

![](https://i.imgur.com/5KVFzXp.png)

Once you have this, open `bot.py` with your favourite text editor and modify the variables `SERVER_ID` and `ROLE_NAME` on line 27 and 28 respectively. This should look something like this, for example.

Mind, that this step is only necessary if you want to use the `$register` command. If you wish to use it, set the `REGISTRATION` variable on line 25 to `True`.

```
SERVER_ID = '413394798255407114' # Discord server's ID
ROLE_NAME = 'VIP'           # Discord server's granted role name
```

### Running bot.py

All variables have been defined, but before you can run bot.py you need to install some Python packages first; `discord`, `coinmarketcap` and `steem`. You can do this by executing the following command in your terminal

```
$ pip3 install discord coinmarketcap steem
```

After installing everything you are now ready to run bot.py. You can do this by executing the following command in your terminal

```
$ python3 bot.py
```

which should output something similar to this

```
Invite link: https://discordapp.com/oauth2/authorize?client_id=413405585036279808&scope=bot&permissions=8
--------
Socko-Bot was built by Vctr#5566
Steemit profile: https://steemit.com/@jestemkioskiem
```

Clicking the invite link should take you to a page that looks like this

![](https://i.imgur.com/bG20fLv.png)

Here you can select which server you want to add your bot to. Once you select your server click the "Authorize" button and your bot will be added to the server! Congratulations!

![](https://i.imgur.com/nxtetc9.png)
