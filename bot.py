# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import datetime
import os
import json
import requests
import random
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

BOT_USER_NAME =  os.getenv('NAME') # Put your bot's steem username in here.
BOT_PRIVATE_POSTING_KEY = os.getenv('KEY') # Put your bot's private posting key in here. Don't worry, it's protected by an encrypted wallet (on your first run you will be asked to set the password via shell).
SERVER_ID = '' # Put Discord server's ID
ROLE_NAME = '' # Put Discord server's granted role name

steemd_nodes = [
    'https://api.steemit.com/',
    'https://gtg.steem.house:8090/',
    'https://steemd.steemitstage.com/',
    'https://steemd.steemgigs.org/'
    'https://steemd.steemit.com/',
]
s = Steem(nodes=steemd_nodes, keys=[BOT_PRIVATE_POSTING_KEY])
set_shared_steemd_instance(Steemd(nodes=steemd_nodes)) # set backup API nodes
account = Account(BOT_USER_NAME, steemd_instance=s)

cmc = Market() # Coinmarketcap API call.
bot_role = 'sockobot' # Set a role for your bot here. Temporary fix.
all_posts = [] # Need this global var later. Temporary fix.
react_dict = {}

ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
btc_usd = cmc.ticker("bitcoin", limit="3", convert="USD")[0].get("price_usd", "none")
eth_usd = cmc.ticker("ethereum", limit="3", convert="USD")[0].get("price_usd", "none")

moderating_roles = ['' # A temporary way to handle moderation.
]

channels_list = [ # Channels that the bot should remove old messages from with del_old_mess()
]

registered_users = {
	
}

voting_power = { # Decides how big of an upvote each channel gets.
# 'channels_id' : 0-100 (% of your vote)
}

minimum_payment = 1.000 # 1 STEEM

session = requests.Session()

#########################
# DEFINE FUNCTIONS HERE #
#########################

 # Used to run any commands. Add your custom commands here, each under a new elif command.startswith(name):.
async def command(msg,command):
	command = str(command)
	command = command[1:]
	if command.lower().startswith('ping'):
		await client.send_message(msg.channel,":ping_pong: Pong!")

	elif command.lower().startswith('price'):
		coin = command.split(' ')[1]
		btc_usd = cmc.ticker("bitcoin", limit="3", convert="USD")[0].get("price_usd", "none")
		ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
		sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")

		if coin.lower() == 'ste' or coin.lower() == "steem":
			await client.send_message(msg.channel, "Current price of **STEEM (STE):** " + ste_usd + " USD")
		elif coin.lower() == 'sbd':
			await client.send_message(msg.channel, "Current price of **Steem Dollar (SBD):** " + sbd_usd + " USD")
		elif coin.lower() == 'btc' or coin.lower() == "bitcoin":
			await client.send_message(msg.channel, "Current price of **Bitcoin (BTC):** " + btc_usd + " USD")
		elif coin.lower() == 'eth' or coin.lower() == "ethereum":
			await client.send_message(msg.channel, "Current price of **Ethereum (ETH):** " + eth_usd + " USD")	
		else:
			await client.send_message(msg.channel, "I only know the price of STEEM, SBD and BTC.")

	elif command.lower().startswith('payout'):
		user_name = command.split(' ')[1]

		try:
			days = command.split(' ')[2]
		except IndexError:
			days = 7

		ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
		sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
		total_p = fetch_payouts_by_blog(user_name, days)
		total_c = fetch_payouts_by_comments(user_name, days)
		total_payout = await payout(total_p + total_c,sbd_usd)
		url = requests.get('https://steemitimages.com/u/' + user_name + '/avatar/small', allow_redirects=True).url
		em = discord.Embed(description=total_payout + 'USD')
		em.set_author(name='@' + user_name, icon_url=url)
		await client.send_message(msg.channel, embed=em)
		
	elif command.lower().startswith('vote'):
		user_name = command.split(' ')[1]
		account = Account(BOT_USER_NAME, steemd_instance=s)

		voting_power = round(float(Account(user_name)['voting_power'] / 100), 2)
		estimated_upvote = round(calculate_estimated_upvote(user_name), 2)
		estimated_upvote_now = round(estimated_upvote * voting_power / 100, 2)
		
		url = requests.get('https://steemitimages.com/u/' + user_name + '/avatar/small', allow_redirects=True).url
		em = discord.Embed(description='Voting power: ' + str(voting_power) + '%\nEstimated 100% powered upvote: $' + str(estimated_upvote) + ', currently: $' + str(estimated_upvote_now))
		em.set_author(name='@' + user_name, icon_url=url)
		await client.send_message(msg.channel, embed=em)
		
	elif command.lower().startswith('register'):
		await client.send_message(msg.author, "<@" + msg.author.id + ">, to register send transaction for " + str(minimum_payment) + " STEEM to @" + BOT_USER_NAME + " with memo: " + msg.author.id)

	elif command.lower().startswith('dice'):
		await client.send_message(msg.author, "<@" + msg.author.id + ">, to gamble send transaction for between 1 and 5 STEEM to @" + BOT_USER_NAME + " with memo: 'dice'")

	else:
		command_error = await client.send_message(msg.channel, "Wrong command.")
		await asyncio.sleep(6)
		await client.delete_message(command_error)

async def authorize(msg,user):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	if check_age(p,0,48): 
		upvote_post(msg,BOT_USER_NAME)
		await client.send_message(msg.channel, 'Post authored by **@' + str(p.author) + '** nominated by ' + str('<@'+ msg.author.id +'>') + ' o ID *' + str(msg.id) +'* was accepted by ' + str('<@'+ user.id +'>'))

async def get_info(msg):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])

	embed=discord.Embed(color=0xe3b13c)
	embed.add_field(name="Title", value=str(p.title), inline=False)
	embed.add_field(name="Author", value=str("@"+p.author), inline=True)
	embed.add_field(name="Nominator", value=str('<@'+ msg.author.id +'>'), inline=True)
	embed.add_field(name="Age", value=str(p.time_elapsed())[:-10] +" hours", inline=False)
	embed.add_field(name="Payout", value=str(p.reward), inline=True)
	embed.add_field(name="Payout in USD", value=await payout(p.reward,sbd_usd), inline=True)
	embed.set_footer(text="SockoBot - a Steem bot by Vctr#5566 (@jestemkioskiem)")
	return embed

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
def upvote_post(msg, user):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	p.upvote(float(voting_power[msg.channel.id]),voter=user)
	
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
			
def calculate_estimated_upvote(user_name):
	account = Account(user_name)
	reward_fund = s.get_reward_fund()
	sbd_median_price = get_current_median_history_price()
	
	vests = float(account['vesting_shares'].replace('VESTS', '')) + float(account['received_vesting_shares'].replace('VESTS', ''))
	vestingShares = int(vests * 1e6);
	rshares = 200 * vestingShares / 10000
	estimated_upvote = rshares / float(reward_fund['recent_claims']) * float(reward_fund['reward_balance'].replace('STEEM', '')) * sbd_median_price
	
	return estimated_upvote
			
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

# Calculates the potential payout of all posts on the blog.
async def payout(total,sbd):
	total = float(total) * 0.8 # Currator cut, anywhere between 0.85 and 0.75.
	totalsbd = str(total * 0.5 * float(sbd))[:6]
	totalsp = str(total * 0.5)[:6]
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
				if payment >= minimum_payment and payment <= 5
					if t['memo'].startswith("r"):
						
						register(t['memo'][1:])
						registered_users[t['from']] = t['memo'][1:] # Storing registered users in a dictionary for later database functionality.
					
					elif t['memo'].lower().startswith("dice"):
						winnings = payment*1.95
						result = gamble()
						if result > 50:
							transfer(t['from'],,STEEM,memo="You won " + winnings " STEEM with a roll of " + result "!",account=BOT_USER_NAME)
							await client.send_message(member, "<@" + member.id + ">, you won " + winnings " STEEM with a roll of " + result "!")
						if result <= 50:
							await client.send_message(member, "<@" + member.id + ">, you lost " + payment " STEEM with a roll of " + result " :(")


						
				
		await asyncio.sleep(60) # check every minute

async def register(id, role_name):
	role = discord.utils.get(client.get_server(SERVER_ID).roles, name=role_name)
	member = discord.utils.get(client.get_server(SERVER_ID).members, id=id) # get member by id
	if role in member.roles:
		continue

	await client.add_roles(member, role) # add role to member
	await client.send_message(member, "<@" + member.id + ">, You have been successfully registered :)")

async def gamble():
	result = randint(0,100)
	return result

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
	ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
	sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
	btc_usd = cmc.ticker("bitcoin", limit="3", convert="USD")[0].get("price_usd", "none")
	eth_usd = cmc.ticker("ethereum", limit="3", convert="USD")[0].get("price_usd", "none")
	
	await del_old_mess(72)
	if message.content.startswith('https'):
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
	client.loop.create_task(check_for_payments())
	client.run(os.getenv('TOKEN'))
