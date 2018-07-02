# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import datetime
import os
import json
import requests
from steem import Steem
from steem.post import Post
from steem.blog import Blog
from steem.instance import set_shared_steemd_instance
from steem.account import Account
from steem.steemd import Steemd
from discord.ext.commands import Bot
from discord.ext import commands


# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. @client.command is strongly discouraged, edit your commands into the command() function instead.
client = Bot(description="Onelovebot", command_prefix='$', pm_help = True)

BOT_USER_NAME =  os.getenv('SB_NAME') # Put your bot's steem username in here.
BOT_PRIVATE_POSTING_KEY = os.getenv('SB_KEY') # Put your bot's private posting key in here. Don't worry, it's protected by an encrypted wallet (on your first run you will be asked to set the password via shell).

REGISTRATION = False # True to enable the use of the REGISTER command.
if REGISTRATION:
	ROLE_NAME = 'Registered' # Put Discord server's granted role name, used with the REGISTER command.
	SERVER_ID = 'putidhere' # Put Discord server's ID
	minimum_payment = 0.001 # Price of registration, in STEEM

s = Steem(nodes=["https://api.steemitstage.com", "https://rpc.buildteam.io"], keys=[BOT_PRIVATE_POSTING_KEY])
steemd_nodes = [
    'https://api.steemitdev.com',
    'https://gtg.steem.house:8090/',
    'https://steemd.steemitstage.com/',
    'https://steemd.steemgigs.org/'
    'https://steemd.steemit.com/',
]
set_shared_steemd_instance(Steemd(nodes=steemd_nodes)) # set backup API nodes

account = Account(BOT_USER_NAME, steemd_instance=s)
bot_role = 'Onelovebot' # Set a role for your bot here. Temporary fix.
all_posts = [] # Need this global var later. Temporary fix.
react_dict = {}

moderating_roles = ['' # A temporary way to handle moderation.
]

channels_list = [ # Channels that the bot should remove old messages from with del_old_mess()
]

registered_users = {
	
}

voting_power = { # Decides how big of an upvote each channel gets.
'base' : 100, # Basic value for channels not present in this dictionary.

}


help_message = str('One Love Bot--Delegate to keep the bot alive. \n\n \
**Commands and their arguments:**\n\n\
%(p)s*ping*\n\
Contact a mod should you need  help') % {'p' : client.command_prefix}


error_message = str("The command you tried doesn't exist or you didn't provide enough arguments to run it. Use %shelp to see a list of commands and their arguments.") %(client.command_prefix)

session = requests.Session()

#########################
# DEFINE FUNCTIONS HERE #
#########################

 # Used to run any commands. Add your custom commands here, each under a new elif command.startswith(name):.
async def command(msg,text):

	text = str(text)
	text = text[1:]
	if text.lower().startswith('ping'):
		await client.send_message(msg.channel,":ping_pong: Pong!")

	elif text.lower().startswith('help'):
		if client.pm_help == True:
			await client.send_message(msg.author, help_message)
		else:
			await client.send_message(msg.channel, help_message)
	elif text.lower().startswith('wallet'):
		try:
			user_name = text.split(' ')[1]
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return 0
		
		acc = Account(user_name, steemd_instance=s)
		url = requests.get('https://steemitimages.com/u/' + user_name + '/avatar/small', allow_redirects=True).url

		sp = calculate_steem_power(vests)
		rec_sp = calculate_steem_power(rec_vests)

	
		sp_diff = round(rec_sp - del_sp, 2)
		voting_power = round(float(Account(user_name)['voting_power'] / 100), 2)
		estimated_upvote = round(calculate_estimated_upvote(user_name), 2)

		embed=discord.Embed(color=0xe3b13c)
		embed.set_author(name='@' + user_name, icon_url=url)
		embed.set_footer(text="SockoBot - a Steem bot by Jestemkioskiem#5566 (@jestemkioskiem)")

		await client.send_message(msg.channel, embed=embed)		

	elif text.lower().startswith('sp'):
		try:
			user_name = text.split(' ')[1]
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return 0

		acc = Account(user_name, steemd_instance=s)
		url = requests.get('https://steemitimages.com/u/' + user_name + '/avatar/small', allow_redirects=True).url
		
		vests = float(acc['vesting_shares'].replace('VESTS', ''))
		sp = calculate_steem_power(vests)
		rec_vests = float(acc['received_vesting_shares'].replace('VESTS', ''))
		rec_sp = calculate_steem_power(rec_vests)
		del_vests = float(acc['delegated_vesting_shares'].replace('VESTS', ''))
		del_sp = calculate_steem_power(del_vests)
		sp_diff = round(rec_sp - del_sp, 2)

		embed=discord.Embed(color=0xe3b13c)
		embed.set_author(name='@' + user_name, icon_url=url)
		if sp_diff >= 0:
			embed.add_field(name="Delegations", value="+" + str(sp_diff), inline=True)
		else:
			embed.add_field(name="Delegations", value=str(sp_diff), inline=True)

		await client.send_message(msg.channel, embed=embed)	
	
		
	elif text.lower().startswith('register'):
		try:
			user_name = text.split(' ')[1]
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return 0
		if REGISTRATION:
			await client.send_message(msg.author, "<@" + msg.author.id + ">, to register send transaction for " + str(minimum_payment) + " STEEM to @" + BOT_USER_NAME + " with memo: " + msg.author.id)
		else:
			await client.send_message(msg.author, "Registration is disabled on this server.")

	else:
		command_error = await client.send_message(msg.channel, error_message)
		await asyncio.sleep(6)
		await client.delete_message(command_error)

async def authorize(msg,user):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	if check_age(p,0,48): 
		upvote_post(msg,BOT_USER_NAME)
		await client.send_message(msg.channel, 'Post authored by **@' + str(p.author) + '** nominated by ' + str('<@'+ msg.author.id +'>') + ' o ID *' + str(msg.id) +'* was accepted by ' + str('<@'+ user.id +'>'))

# Gets info about a post while taking in a message with said post.
async def get_info(msg):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])

	embed=discord.Embed(color=0xe3b13c)
	embed.add_field(name="Title", value=str(p.title), inline=False)
	embed.add_field(name="Author", value=str("@"+p.author), inline=True)
	embed.add_field(name="Nominator", value=str('<@'+ msg.author.id +'>'), inline=True)
	embed.add_field(name="Age", value=str(p.time_elapsed())[:-10] +" hours", inline=False)
	embed.set_footer(text="Onelovebot")
	return embed

# Checks if the post's age is between low and high, returns True or False accordingly.
def check_age(post,low,high):
	if post.time_elapsed() > datetime.timedelta(hours=low) and post.time_elapsed() < datetime.timedelta(hours=high):
		return True
	else:
		return False

# Returns true if message's author has a moderating_roles role.
def is_mod(reaction, user): 
	auth_roles = []
	for x in user.roles:
		auth_roles.append(x.name.lower())

	for x in moderating_roles:
		if x in auth_roles:
			return True
			break
		else:
			return False
# Upvotes a post while taking in a message with said post.
def upvote_post(msg, user):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	try:
		p.upvote(float(voting_power[msg.channel.id]),voter=user)
	except KeyError:
		p.upvote(float(voting_power['base']),voter=user)
	
def session_post(url, post):
	headers = {
		'User-Agent': 'sockobot'
	}
	return session.post(url, data = post, headers = headers, timeout = 30)



# Calculates given user's steem power.
def calculate_steem_power(vests):
	post = '{"id":1,"jsonrpc":"2.0","method":"get_dynamic_global_properties", "params": []}'
	response = session_post('https://api.steemit.com', post)
	data = json.loads(response.text)
	data = data['result']

	total_vesting_fund_steem = float(data['total_vesting_fund_steem'].replace('STEEM', ''))
	total_vesting_shares = float(data['total_vesting_shares'].replace('VESTS', ''))

	return round(total_vesting_fund_steem * (float(vests)/total_vesting_shares), 2)


# Calculates the estimated upvote of a given user.
# Takes in 3 arguments and turns them into a link, then returns it.
def delegate(sp, user_name, target_user_name):
	link = 'https://v2.steemconnect.com/sign/delegateVestingShares?delegator=%s&delegatee=%s&vesting_shares=%s' % (user_name, target_user_name, round(sp, 3))
	return link + '%20SP'

# Deletes posts in channel_list channels older than given hours.
async def del_old_mess(hours): 
	currtime = datetime.datetime.now() - datetime.timedelta(hours=hours)
	chn = []
	for x in client.get_all_channels():
		if x.id in channels_list:
			chn.append(x)
	for x in chn:
		async for y in client.logs_from(x,limit=100,before=currtime):
			await client.delete_message(y)

# Returns true if message's author has a moderating_roles role.
def is_mod(reaction, user): 
	auth_roles = []
	for x in user.roles:
		auth_roles.append(x.name.lower())

	for x in moderating_roles:
		if x in auth_roles:
			return True
			break
		else:
			return False

async def check_for_payments():
	await client.wait_until_ready()
	role = discord.utils.get(client.get_server(SERVER_ID).roles, name=ROLE_NAME)
	
	while not client.is_closed:
		transfers = account.history_reverse(filter_by='transfer')
		now = datetime.datetime.now() - datetime.timedelta(days=7) # check only last 7 days
		
		for t in transfers:
				
			#print('Received from: ' + t['from'] + ' +' + t['amount'] + '. Memo: ' + t['memo'] + ' at ' + t['timestamp'])
			
			if now > datetime.datetime.strptime(t['timestamp'], "%Y-%m-%dT%H:%M:%S"):
				break
				
			if t['from'] == BOT_USER_NAME: # skip mine transactions
				continue
			
			if not t['memo'].isdigit(): # skip invalid MEMO
				continue
			
			if 'STEEM' in t['amount']: # STEEM payment only?
				payment = float(t['amount'].replace("STEEM", ""))
				if payment >= minimum_payment:
					member = discord.utils.get(client.get_server(SERVER_ID).members, id=t['memo']) # get member by id
					if role in member.roles:
						continue

					registered_users[t['from']] = msg.author.id # Storing registered users in a dictionary for later database functionality.
					await client.add_roles(member, role) # add role to member
					await client.send_message(member, "<@" + member.id + ">, You have been successfully registered :)")
				
		await asyncio.sleep(60) # check every minute

######################
# DEFINE EVENTS HERE #
######################

@client.event
async def on_ready():
	print('\nInvite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Socko-Bot was built by Vctr#5566')
	print('Steemit profile: https://steemit.com/@jestemkioskiem')


# This is our event check. For simplicity's sake, everything happens here. You may add your own events, but commands are discouraged, for that, edit the command() function instead.
@client.event
async def on_message(message):
	
	await del_old_mess(72)
	if message.content.startswith('https://steemit') or message.content.startswith('https://busy') or message.content.startswith('https://utopian'):
		embed = await get_info(message)
		botmsg = await client.send_message(message.channel, embed=embed)
		react_dict[message.id] = botmsg.id
	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

@client.event
async def on_reaction_add(reaction, user):
	if reaction.emoji == '☑':
		await authorize(reaction.message, user)
		botmsg = await client.get_message(reaction.message.channel, react_dict[reaction.message.id])
		await client.delete_message(botmsg)
if __name__ == '__main__': # Starting the bot.
	if REGISTRATION:
		client.loop.create_task(check_for_payments())

client.run(os.getenv('SB_TOKEN'))
