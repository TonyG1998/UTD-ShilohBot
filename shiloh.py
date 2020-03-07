import os
import discord
import random
import faceit_login
import api
import sql_test as sql
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands, tasks
import asyncio

load_dotenv(dotenv_path=r'./resources/.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')



client = discord.Client()


bot = commands.Bot(command_prefix='!')
bot.remove_command('help')


@tasks.loop(seconds=5.0)
async def test_print():
	#TODO moveteams function implemented into loop, check for ongoing matches and move
	print('hello?')

@test_print.after_loop
async def after_test_print():
	print('done!')


@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')

faceit_login.sel_login()

@bot.command(name='pop', help = 'Displays the number of members needed to pop the 10 man queue')
async def queue_response(ctx):
	num_in_queue = faceit_login.queue_data()
	inverse = 10 - num_in_queue
	response = "+" + str(inverse)
	await ctx.send(response)

@bot.command(name='queue', help = 'Displays members in the queue')
async def who_response(ctx):
	#TODO fix queue response on mac
	#returns a list of dicts with keys "name" and "skill"
	response = faceit_login.members_in_queue()
	num_in_queue = str(len(response))
	formatted_text = "***USERS IN QUEUE: *** \n\n"
	formatted_text = formatted_text + "*(" + num_in_queue + "/10)*\n"

	
	


	for member in response:
		name = member['username']
		# winky face
		if name == 'Ryker':
			custom = ':rotating_light: ' + name + ' :rotating_light:' 
			name = custom

		line = "**" + name + "**   -   Lvl " + member['skill'] + "\n"
		formatted_text = formatted_text + line

	#find num of ongoing matches and include in data
	ongoing = api.num_of_ongoing_matches()
	if ongoing == 1:
		formatted_text = formatted_text + "\n*" + str(ongoing) + " ongoing match*"
	elif ongoing > 1:
		formatted_text = formatted_text + "\n*" + str(ongoing) + " ongoing matches*"

	await ctx.send(formatted_text)

@bot.command(name='help')
async def help(ctx):
	author = ctx.message.author

	embed = discord.Embed(color = discord.Colour.blue())

	embed.set_author(name = 'Help')
	embed.add_field(name='!queue', value='Displays members in 10 man queue, and if there are any ongoing matches', inline=False)
	embed.add_field(name='!pop', value='Displays the amount of members needed to pop the queue', inline=False)
	embed.add_field(name='!matches', value='Shows ongoing match, if any', inline=False)
	embed.add_field(name='!goodboy', value='woof', inline=False)

	await ctx.send(embed=embed)

@bot.command(name='matches')
async def match_response(ctx):
	#returns a python dict of match data, contains keys (team1, team2, map, team1_roster, team2_roster)
	data = api.ongoing_match_data()

	if data == 0:
		await ctx.send('*No ongoing matches*')
	else:
		response = '__**MATCH:**__ \n' + '*' + data['map'] + '*\n\n' + '**' + data['team1'] + '**\n'

		for player in data['team1_roster']:
			response += player + '\n'

		response += '\n**' + data['team2'] + '**\n'

		for player in data['team2_roster']:
			response += player + '\n'

	await ctx.send(response)

@bot.command(name='goodboy')
async def woof(ctx):
	await ctx.send(file=discord.File(faceit_login.shiloh_pic()))

@bot.command(name='faceit')
async def link_user(ctx, arg):
	#links the users account to a faceit profile, and enters it into the database
	faceit_name = arg
	discord_id = str(ctx.message.author.id)

	print(discord_id)
	print(type(discord_id))
	print(faceit_name)
	print(type(faceit_name))
	#create user tuple that follows how data is inserted
	user = (discord_id, faceit_name)
	

	#link the database
	conn = sql.create_connection("resources/users.db")
	with conn:
		sql.create_user(conn, user)

	await ctx.send("You have linked your discord profile with the \"" + faceit_name + "\" faceit profile")

@bot.command(name='move-test')
async def movetest(ctx):
	await bot.wait_until_ready()
	UTD_GUILD = bot.get_guild(363147231974522881)
	teamA = ['asauce']
	teamB = ['yakuza']


	await faceit_login.place_teams(teamA, teamB, UTD_GUILD)



async def move_teams():
	#returns a python dict of match data, contains keys (team1, team2, map, team1_roster, team2_roster)
	data = api.ongoing_match_data()

	UTD_GUILD = bot.get_guild(363147231974522881)
	if data != 0:
		teamA = data['team1_roster']
		teamB = data['team2_roster']

		await faceit_login.place_teams(teamA, teamB, UTD_GUILD)




















bot.run(TOKEN)
