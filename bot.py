# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import datetime
import os
import json
import requests
from coinmarketcap import Market
from steem import Steem
from steem.post import Post
from steem.blog import Blog
from steem.instance import set_shared_steemd_instance
from steem.account import Account
from steem.steemd import Steemd
from discord.ext.commands import Bot
from discord.ext import commands


# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. @client.command is strongly discouraged, edit your commands into the command() function instead.
client = Bot(description="Socko-Bot", command_prefix='$', pm_help = True)

BOT_USER_NAME =  os.getenv('SB_NAME') # Put your bot's steem username in here.
BOT_PRIVATE_POSTING_KEY = os.getenv('SB_KEY') # Put your bot's private posting key in here. Don't worry, it's protected by an encrypted wallet (on your first run you will be asked to set the password via shell).

REGISTRATION = False # True to enable the use of the REGISTER command.
if REGISTRATION:
	ROLE_NAME = '' # Put Discord server's granted role name, used with the REGISTER command.
	SERVER_ID = '' # Put Discord server's ID
	minimum_payment = 1.000 # Price of registration, in STEEM

s = Steem(nodes=["https://api.steemit.com", "https://rpc.buildteam.io"], keys=[BOT_PRIVATE_POSTING_KEY])
steemd_nodes = [
    'https://api.steemit.com/',
    'https://gtg.steem.house:8090/',
    'https://steemd.steemitstage.com/',
    'https://steemd.steemgigs.org/'
    'https://steemd.steemit.com/',
]
set_shared_steemd_instance(Steemd(nodes=steemd_nodes)) # set backup API nodes

account = Account(BOT_USER_NAME, steemd_instance=s)
cmc = Market() # Coinmarketcap API call.
bot_role = 'sockobot' # Set a role for your bot here. Temporary fix.
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
# 'channels_id' : 0-100 (% of your vote)
}


help_message = str('Please, refer to <https://github.com/Jestemkioskiem/steem-sockobot/blob/master/README.md> for more desriptive help. \n\n \
**Commands and their arguments:**\n\n\
%(p)s*ping*\n\
%(p)s*convert* <value> <coin1> <coin2>\n\
%(p)s*delegate* <delegator> <value> <delegatee>\n\
%(p)s*payout* <username> <days>\n\
%(p)s*price* <coin>\n\
%(p)s*register* <username>\n\
%(p)s*sp* <username>\n\
%(p)s*vote* <username>\n\
%(p)s*wallet* <username>\n\n\
To get help regarding non-command functionality, refer to the github page\'s README.md file and it\'s Wiki, or contact the developer at Jestemkioskiem#5566') % {'p' : client.command_prefix}


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

	elif text.lower().startswith('delegate'):
		try:
			user_name = text.split(' ')[1].lower()
			value = float(text.split(' ')[2])
			target_user_name = text.split(' ')[3].lower()
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return None

		await client.send_message(msg.channel, 'To delegate using **SteemConnect**, click the link below: \n %s' % (delegate(value, user_name, target_user_name)))

	elif text.lower().startswith('convert'):
		try:
			value = text.split(' ')[1]
			coin1 = text.split(' ')[2].lower()
			coin2 = text.split(' ')[3].lower()
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return None

		try:
			price1 = cmc.ticker(coin1, limit="3", convert="USD")[0].get("price_usd", "none")
			price2 = cmc.ticker(coin2, limit="3", convert="USD")[0].get("price_usd", "none")
		except Exception:
			await client.send_message(msg.channel, str("You need to provide the full name of the coin (as per coinmarketcap)."))
		
		conv_rate = float(price1)/float(price2)
		outcome = float(value) * conv_rate

		await client.send_message(msg.channel, str("You can receive %s **%s** for %s **%s**." % (outcome, coin2, value, coin1) ))

	elif text.lower().startswith('wallet'):
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
		voting_power = round(float(Account(user_name)['voting_power'] / 100), 2)
		estimated_upvote = round(calculate_estimated_upvote(user_name), 2)

		embed=discord.Embed(color=0xe3b13c)
		embed.set_author(name='@' + user_name, icon_url=url)
		embed.add_field(name="Steem", value=str(str(acc['balance'].replace('STEEM', ''))), inline=True)
		embed.add_field(name="Steem Dollars", value=str(acc['sbd_balance'].replace('SBD', '')), inline=True)
		if sp_diff >= 0:
			embed.add_field(name="Steem Power", value=str(sp) + " ( +" + str(sp_diff) + ")", inline=True)
		else:
			embed.add_field(name="Steem Power", value=str(sp) + " ( " + str(sp_diff) + ")", inline=True)
		embed.add_field(name="Estimated Account Value", value=str(calculate_estimated_acc_value(user_name)), inline=True)
		embed.add_field(name="Estimated Vote Value", value=str(estimated_upvote) + " $", inline=True)
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
		embed.add_field(name="Steem Power", value=str(sp), inline=True)
		if sp_diff >= 0:
			embed.add_field(name="Delegations", value="+" + str(sp_diff), inline=True)
		else:
			embed.add_field(name="Delegations", value=str(sp_diff), inline=True)

		await client.send_message(msg.channel, embed=embed)	

	elif text.lower().startswith('price'):
		try:
			coin = text.split(' ')[1].lower()
		except IndexError:
			await client.send_message(msg.channel, error_message)
		
		try: 
			value = cmc.ticker(coin, limit="3", convert="USD")[0].get("price_usd", "none")
			await client.send_message(msg.channel, str("The current price of **%s** is: *%s* USD." % (coin, value)))
		except Exception:
			await client.send_message(msg.channel, str("You need to provide the full name of the coin (as per coinmarketcap)."))		 

	elif text.lower().startswith('payout'):
		try:
			user_name = text.split(' ')[1]
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return 0

		try:
			days = text.split(' ')[2]
		except IndexError:
			days = 7

		ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
		sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
		total_p = fetch_payouts_by_blog(user_name, days)
		total_c = fetch_payouts_by_comments(user_name, days)
		total_payout = await payout(total_p + total_c,sbd_usd,ste_usd)
		url = requests.get('https://steemitimages.com/u/' + user_name + '/avatar/small', allow_redirects=True).url
		em = discord.Embed(description=total_payout + 'USD')
		em.set_author(name='@' + user_name, icon_url=url)
		await client.send_message(msg.channel, embed=em)
		
	elif text.lower().startswith('vote'):
		try:
			user_name = text.split(' ')[1]
		except IndexError:
			await client.send_message(msg.channel, error_message)
			return 0
		
		voting_power = round(float(Account(user_name)['voting_power'] / 100), 2)
		estimated_upvote = round(calculate_estimated_upvote(user_name), 2)
		estimated_upvote_now = round(estimated_upvote * voting_power / 100, 2)
		
		url = requests.get('https://steemitimages.com/u/' + user_name + '/avatar/small', allow_redirects=True).url
		em = discord.Embed(description='Voting power: ' + str(voting_power) + '%\nEstimated 100% powered upvote: $' + str(estimated_upvote) + ', currently: $' + str(estimated_upvote_now))
		em.set_author(name='@' + user_name, icon_url=url)
		await client.send_message(msg.channel, embed=em)
		
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
	sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
	ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")

	embed=discord.Embed(color=0xe3b13c)
	embed.add_field(name="Title", value=str(p.title), inline=False)
	embed.add_field(name="Author", value=str("@"+p.author), inline=True)
	embed.add_field(name="Nominator", value=str('<@'+ msg.author.id +'>'), inline=True)
	embed.add_field(name="Age", value=str(p.time_elapsed())[:-10] +" hours", inline=False)
	embed.add_field(name="Payout", value=str(p.reward), inline=True)
	embed.add_field(name="Payout in USD", value=await payout(p.reward,sbd_usd,ste_usd), inline=True)
	embed.set_footer(text="SockoBot - a Steem bot by Jestemkioskiem#5566 (@jestemkioskiem)")
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
		'User-Agent': 'Socko-Bot'
	}
	return session.post(url, data = post, headers = headers, timeout = 30)

def fetch_payouts_by_blog(user, days):
	total = 0.0
	
	post = '{"id":1,"jsonrpc":"2.0","method":"get_discussions_by_blog","params":[{"tag":"' + user + '","limit":50}]}' # retrieve last 50 blog posts
	response = session_post('https://api.steemit.com', post)
	data = json.loads(response.text)
	if 'result' in data:
		x = 0
		while x < len(data['result']):
			post = data['result'][x]
			if post['author'] == user and datetime.datetime.strptime(post['created'][:10], "%Y-%m-%d").date() <= datetime.date.today() - (datetime.timedelta(days=7) - datetime.timedelta(days=int(days))):
				reward = float(post['pending_payout_value'].replace("SBD", "")) # we take 'pending_payout_value' parameter which lasts 7 days
				total+= reward
			x+= 1
	else:
		raise Exception('User does not exist!')

	return total

def fetch_payouts_by_comments(user, days):
	total = 0.0
	
	post = '{"id":1,"jsonrpc":"2.0","method":"get_discussions_by_comments","params":[{"start_author":"' + user + '","limit": 50}]}' # retrieve last 50 blog posts
	response = session_post('https://api.steemit.com', post)
	data = json.loads(response.text)
	
	if 'result' in data:
		x = 0
		while x < len(data['result']):
			post = data['result'][x]
			if post['author'] == user and datetime.datetime.strptime(post['created'][:10], "%Y-%m-%d").date() >= datetime.date.today() - datetime.timedelta(days=int(days)):
				reward = float(post['pending_payout_value'].replace("SBD", "")) # we take 'pending_payout_value' parameter which lasts 7 days
				total+= reward
			x+= 1
	else:
		raise Exception('User does not exist!')

	return total

# Calculates given user's steem power.
def calculate_steem_power(vests):
	post = '{"id":1,"jsonrpc":"2.0","method":"get_dynamic_global_properties", "params": []}'
	response = session_post('https://api.steemit.com', post)
	data = json.loads(response.text)
	data = data['result']

	total_vesting_fund_steem = float(data['total_vesting_fund_steem'].replace('STEEM', ''))
	total_vesting_shares = float(data['total_vesting_shares'].replace('VESTS', ''))

	return round(total_vesting_fund_steem * (float(vests)/total_vesting_shares), 2)

# Calculates the estimated account value in USD.
def calculate_estimated_acc_value(user_name):
	steem_price = float(cmc.ticker('steem', limit="3", convert="USD")[0].get("price_usd", "none"))
	sbd_price = float(cmc.ticker('steem-dollars', limit="3", convert="USD")[0].get("price_usd", "none"))

	acc = Account(user_name, steemd_instance=s)
	vests = float(acc['vesting_shares'].replace('VESTS', ''))
	sp = calculate_steem_power(vests)
	steem_balance = float(acc['balance'].replace('STEEM', ''))
	sbd_balance = float(acc['sbd_balance'].replace('SBD', ''))
	outcome = round(((sp + steem_balance) * steem_price ) + (sbd_balance * sbd_price), 2)

	return str(outcome) + " USD"

# Calculates the estimated upvote of a given user.
def calculate_estimated_upvote(user_name):
	account = Account(user_name)
	reward_fund = s.get_reward_fund()
	sbd_median_price = get_current_median_history_price()
	
	vests = float(account['vesting_shares'].replace('VESTS', '')) + float(account['received_vesting_shares'].replace('VESTS', '')) - float(account['delegated_vesting_shares'].replace('VESTS', ''))
	vestingShares = int(vests * 1e6);
	rshares = vestingShares * 0.02
	estimated_upvote = rshares / float(reward_fund['recent_claims']) * float(reward_fund['reward_balance'].replace('STEEM', '')) * sbd_median_price
	
	return estimated_upvote

# Gets current median history price of SBD in the blockchain.
def get_current_median_history_price():
	price = 0.0

	data = '{"id":1,"jsonrpc":"2.0","method":"get_current_median_history_price"}'
	response = session_post('https://api.steemit.com', data)
	data = json.loads(response.text)
	
	if 'result' in data:
		price = float(data['result']['base'].replace('SBD', ''))		
	else:
		raise Exception('Couldnt get the SBD price!')
	
	return price

# Takes in 3 arguments and turns them into a link, then returns it.
def delegate(sp, user_name, target_user_name):
	link = 'https://v2.steemconnect.com/sign/delegateVestingShares?delegator=%s&delegatee=%s&vesting_shares=%s' % (user_name, target_user_name, round(sp, 3))
	return link + '%20SP'

# Calculates the potential payout of all posts on the blog.
async def payout(total,sbd,ste):
	total = float(total) * 0.8 # Currator cut, anywhere between 0.85 and 0.75.
	totalsbd = str(total * 0.5 * float(sbd))[:6]
	totalsp = total * 0.5 * float(ste)
	totalsp = str(totalsp * 1/float(ste))[:6] # SBD is always worth 1$ in the steem blockchain, so price of SBD to price of STE is always 1/STE.
	payout = str(float(totalsbd) + float(totalsp))[:6]
	return payout
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
