import discord
from discord.ext import commands
import functions as f
import error_messages as em
import defs as d
import time
import numpy as np
import clist as l
import chelp as h
import cpick as p
import cmake_draft as md
import coverride as o
import cbackup as b
import cdelpick as dp
import asyncio

# the bot responds to commands beginning with "!"
# input your own token after creating a bot on discord
bot = commands.Bot(command_prefix = '!')
TOKEN = 'NTcxMzEzMzk3NDU1NTE5NzQ1.XML9ng.sPSlZjobZhkNRUAmt5J9Hs5Dz30'

# tell users that someone else is using the bot if the command is on cooldown
# else, raise the error
@bot.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(em.cooldown)
	else:
		raise(error)

# begin the draft
@bot.command()
async def make_draft(ctx):

	# initializes the drafter arrays and creates the line saying who started the draft
	draft_created_line = md.initialize(ctx)
	await ctx.send(line)
	
	# make and set up the draft channel
	dc_name = 'season-9-3-draft-bot'
	await ctx.message.guild.create_text_channel(dc_name)
	d.dc = discord.utils.get(ctx.guild.text_channels, name = dc_name)
	
	# ask the user if the displayed order is correct
	# if so, continue on and set up the draft order as the given order
	# if not, ask the user to set the draft order themselves with the !draft_order command
	await ctx.send("Would you like to use the pre-loaded draft order above (y/n)?")
	msg = ctx.message
	def check(m):	return m.author == ctx.author and m.channel == ctx.channel
	while msg.content.lower() not in ['y', 'yes', 'n', 'no']:
		msg = await bot.wait_for('message', check = check)
		if msg.content.lower() in ['y', 'yes']:
			await ctx.send('Okay, this is the order I\'ll use then.')
			break
		elif msg.content.lower() in ['n', 'no']:
			await ctx.send("All right then. To enter the draft order by hand, use the command \"!draft_order\"")
			return
		else:
			await ctx.send('I didn\'t understand what you said. Please enter \"y\" or \"n\".')

	
	# sets the draft order, and makes it snake order for 11 total picks
	# if the code-editor has already created a pre-loaded order, use that
	if len(d.pre_loaded_users) == 0:	d.draft_order = d.drafters[:]
	else:					d.draft_order = d.pre_loaded_users[:]
	d.draft_order = md.flip_and_add(d.draft_order)
	d.drafters = d.base_drafters
	
	# declare who the "current" and "next" and "nnext" drafters are
	# also set roundnum = 1 and picknum = 1
	md.initialize_current_next_drafters()
	
	# write the first line in the new draft channel
	line, fmt = md.new_draft_channel_first_line(ctx)
	await d.dc.send(line.format(*fmt))

# lets the user enter the draft order themselves
@bot.command()
async def draft_order(ctx):
	
	# reset the draft order
	d.draft_order = []

	# function to make sure the user responding is the expected one and the channel is the expected one
	def check(m):	return m.author == ctx.author and m.channel == ctx.channel

	# prompt the user to enter the draft order themselves
	await ctx.send("I have that %i coaches are in for this draft, so I need you to mention the coaches in order that the draft goes in, and I'll make it snake order." %len(d.drafters))
	
	# ask the user to tag the coaches in the appropriate order
	for i in range(len(d.drafters)):
		await ctx.send('Who is pick \#%i? Tag them with the \"@\" symbol.' %(i+1))
		msg = await bot.wait_for('message', check = check)
		if '@' not in msg.content:
			await ctx.send('Did you read my directions? Begin all users names with the "@" symbol. Start over.')
			return
	
		# read in a user-tag and turn it into a discord-user object
		u = msg.content.split('@')[-1]
		idnum = u.split('>')[0]
		if '!' in idnum:
			idnum = int(idnum.split('!')[1])
		else:
			idnum = int(idnum)
	
		# check for error
		for user in ctx.channel.members:
			if int(idnum) == user.id:
				if user in d.draft_order:
					await ctx.send("You already told me this user. Start over.")
					d.draft_order = []
					return
				if user not in d.drafters:
					await ctx.send("This user is not listed as a possible drafter for this season. Start over.")
					d.draft_order = []
					return
				else:
					d.draft_order.append(user)
		time.sleep(1)
	
	# print out draft order 
	# ask the user to confirm to make sure nothing went wrong
	await ctx.send("Okay. Here is the draft order I have: ")
	await ctx.send("(Give me a second to write this all out -- I'm sometimes slow at this part)")
	for i in range(len(d.draft_order)):
		await ctx.send('Pick \#{}: {}'.format(i+1, d.draft_order[i].mention))
	await ctx.send('Is this correct (y/n)?')

	yn = msg
	while yn.content.lower() not in ['y', 'n', 'yes', 'no']:
		yn = await bot.wait_for('message', check = check)
		if yn.content.lower() in ['n', 'no']:
			await ctx.send('Okay, something went wrong. Start the command over again.')
			d.draft_order = []
			return
		if yn.content.lower() in ['y', 'yes']:
			await ctx.send('Great! This is the draft order now, in snake order. Happy drafting!')
		else:
			await ctx.send('I didn\'t understand what you said. Is this correct (y/n)?')
	
	# apply the user-created draft order
	d.draft_order = md.flip_and_add(d.draft_order)
	
	# declare who the "current" and "next" and "nnext" drafters are
	# also set roundnum = 1 and picknum = 1
	md.initialize_current_next_drafters()
	
	# write the first line in the new draft channel
	line, fmt = md.new_draft_channel_first_line(ctx)
	await d.dc.send(line.format(*fmt))

# the command users use to submit their picks to the bot to store	
@bot.command()
@commands.cooldown(1, 1000)
async def pick(ctx, *args):
	author = ctx.author
	# check if pick is declared in a PM or not
	if not f.is_pm(ctx):
		pick.reset_cooldown(ctx)
		return
	
	# check if the draft has been set up yet
	if len(d.drafters) == 0:
		pick.reset_cooldown(ctx)
		return

	# read in the args from the user, rejecting them if the syntax is wrong
	myargs = f.get_args(args)
	if len(myargs) != 3:
		await ctx.send(em.not_enough_args)
		pick.reset_cooldown(ctx)
		return
	rd, pokemon, tier = myargs
	
	# check all the possible ways of entering a bad pick, besides syntax
	err_message = p.check_bad_pick_input(ctx, rd, pokemon, tier)
	if err_message != '':
		await ctx.send(err_message)
		pick.reset_cooldown(ctx)
		return

	# ask the user for confirmation, commented out since I didn't think it was necessary
#	await ctx.send("Are you sure you want your Round {} pick to be {}, Tier {}? (y/n)".format(rd, pokemon, tier))
#	def check(m):
#		return m.author == author and m.channel == ctx.channel
#	try:
#		yn = await bot.wait_for('message', timeout = 5, check = check)
#		if yn.content.lower() not in ['y', 'yes']:
#			await ctx.send(em.pick_did_not_go_through)
#			pick.reset_cooldown(ctx)
#			return
#	except asyncio.TimeoutError:
#		await ctx.send("Your request timed out. Please try again.")
#		pick.reset_cooldown(ctx)
#		return

	# tell them their pick went through and update their list accordingly
	confirmation_message = p.apply_pick(author, rd, pokemon, tier)
	await ctx.send(confirmation_message)
	
	# check if the draft was waiting on them
	# if so, send their pick through and advance the draft
	if p.is_next_pick(ctx, rd, pokemon, tier):
		line, fmt = f.draft_pick_line(pokemon)
		f.advance_draft()
		time.sleep(4)
		await d.dc.send(line.format(*fmt))
		
	pick.reset_cooldown(ctx)

# the command users use to submit their backups to the bot
@bot.command()
@commands.cooldown(1, 1000)
async def backup(ctx, *args):
	# do nothing if not in a PM
	if not f.is_pm(ctx):
		backup.reset_cooldown(ctx)
		return
	
	# do nothing if the draft has not been set up yet
	if len(d.drafters) == 0:
		backup.reset_cooldown(ctx)
		return
	
	# check if the user used incorrect syntax
	myargs = f.get_args(args)
	if len(myargs) != 3:
		await ctx.send(em.not_enough_args)
		backup.reset_cooldown(ctx)
		return
	rd, pokemon, tier = myargs
	
	# check if the user messed something else up
	err_message = p.check_bad_pick_input(ctx, rd, pokemon, tier)
	if err_message != '':
		await ctx.send(err_message)
		backup.reset_cooldown(ctx)
		return
	err_message = b.check_bad_input(ctx, rd, pokemon, tier)
	if err_message != '':
		await ctx.send(err_message)
		backup.reset_cooldown(ctx)
		return

	# ask the user for confirmation, commented out since I didn't think it was necessary	
#	def check(m):
#		return m.author == ctx.author		
#	await ctx.send("Are you sure you want to set {}, Tier {} as your Round {} backup pick? \nIf your Round {} pick gets sniped, this will be the Pokemon drafted instead. \nPlease answer y/n:".format(pokemon, tier, rd, rd))
#	
#	try:
#		yn = await bot.wait_for('message', timeout = 10, check = check)
#		if yn.content.lower() not in ['y', 'yes']:
#			await ctx.send(em.backup_did_not_go_through)
#			backup.reset_cooldown(ctx)
#			return
#	except asyncio.TimeoutError:
#		await ctx.send("Your request timed out. Please try again.")
#		return
	
	# let the user know their pick went through and apply their backup pick
	confirmation_message = b.apply_backup(ctx, rd, pokemon, tier)
	await ctx.send(confirmation_message)	
		
	backup.reset_cooldown(ctx)

# the command users use to completely remove a pick from their list
@bot.command()
@commands.cooldown(1, 1000)
async def delpick(ctx, *args):
	# ignore if not in a PM
	if not f.is_pm(ctx):
		delpick.reset_cooldown(ctx)
		return
	
	# ignore if the draft hasn't been set up yet
	if len(d.drafters) == 0:
		delpick.reset_cooldown(ctx)
		return
	
	# check for bad syntax
	myargs = f.get_args(args)
	if len(myargs) != 2:
		await ctx.send(em.not_enough_args_delpick)
	rd, which = myargs
	
	# check for otherwise bad input
	err_message = dp.check_bad_input(ctx, rd, which)
	if err_message != '':
		await ctx.send(err_message)
		delpick.reset_cooldown(ctx)
		return
	
	# ask the user for confirmation before deleting their pick
	def check(m):		return m.author == ctx.author and m.channel == ctx.channel
	msg = "Are you sure you want to delete your Round {} ".format(rd)
	if which.lower() == 'p':	msg += 'primary pick (y/n)? This will set your backup as your new primary pick.'
	else:				msg += 'backup pick (y/n)?'
	await ctx.send(msg)
	
	# give the user 5 seconds to respond, or else the request fails
	try:
		yn = await bot.wait_for('message', timeout = 5, check = check)
		if yn.content.lower() not in ['y', 'yes']:
			# if they don't say "y" or "yes", the pick does not go through
			await ctx.send(em.delpick_did_not_go_through)
			delpick.reset_cooldown(ctx)
			return
	except asyncio.TimeoutError:
		await ctx.send("Your request timed out. Please try again.")
		return
	
	# if they confirmed it, apply the deletion and send a confirmation mesage
	confirmation_message = dp.apply_delete(ctx, rd, which)
	await ctx.send(confirmation_message)
	
	delpick.reset_cooldown(ctx)

# what the bot does whenever a message is posted anywhere
@bot.event
async def on_message(msg):
	content = msg.content
	channel = msg.channel
	author = msg.author

	# check if the bot is going to reply to itself in the draft channel
	# if not, ignore it
	if author == bot.user and channel == d.dc:
	
		# if no one has picked yet, ignore and move on
		if len(d.taken_mons) < 1:	return
		
		# check to see if the mon just picked was a snipe on anyone
		# if so, delete it from their list and PM them to re-pick
		mon_just_picked = d.taken_mons[-1]
		users, idxnums, b_users, b_idxnums = f.check_if_snipe(mon_just_picked)
		f.delete_sniped(users, idxnums, b_users, b_idxnums)
		
		for i in range(len(users)):
			await users[i].send(em.you_got_sniped % (idxnums[i][0] + 1))
		for i in range(len(b_users)):
			await b_users[i].send(em.you_got_sniped_backup % (b_idxnums[i][0]+1))
		time.sleep(2)
	
		# if we have not finished the draft, see who is picking next
		if d.current_drafter != 'END':
			# find the next mon to see if the draft can move forward another step
			next_mon = d.lists[d.current_drafter][d.current_round-1]
			if next_mon != 'None' and next_mon not in d.taken_mons:
			
				# if the draft can move forward another step, state the pick and advance the draft
				line, fmt = f.draft_pick_line(next_mon)
				f.advance_draft()
				time.sleep(2)
				await d.dc.send(line.format(*fmt))
						
	# this needs to be here for the bot to accept commands
	await bot.process_commands(msg)

# the command a user enters to see the picks they have made and the picks they have queued up
@bot.command()
@commands.cooldown(1, 1000)
async def list(ctx):
	
	# ignore if the draft has not been set up yet
	if len(d.drafters) == 0:
		list.reset_cooldown(ctx)
		return
	
	# ignore if bad input
	if l.is_error_input(ctx):
		list.reset_cooldown(ctx)
		return
	
	# TODO: make this look neater with an embed?
	
	# get the user's list of future and past picks, as well as the number that have already gone through
	user_list, num_user_picks = l.get_user_picks(ctx)
	
	# create the line of the user's list and send it
	line = l.get_list_line(ctx, user_list, num_user_picks)
	await ctx.send(line)
	list.reset_cooldown(ctx)

# the command a user enters if something has gone catastrophically wrong and the draft needs to be reset from a certain point
# this is a delicate command, so it must be tested very carefully before being implemented
# this needs more work
@bot.command()
async def override(ctx, *args):
	# not done, needs more work
	return
	
	err_message = o.check_bad_input(ctx, args)
	if err_message != '':
		await ctx.send(err_message)
		return
	
	line = o.get_error_line(ctx, args)
	await d.dc.send(line)
	
	o.reset_draft_lists(ctx, args)

# erase the given "help" command and replace it with my own
bot.remove_command('help')
@bot.command()
async def help(ctx):
	# updated to allow for non-PM requests; the help response should be in a PM
#	if not f.is_pm(ctx):
#		return

	# updated: use cool discord embeds rather than just printing out lines
	embed = discord.Embed(title='Command help', description='Here\'s a bit of help with using the commands in this bot.')
	commands, descriptions = h.help()
	for c, d in zip(commands, description):
		embed.add_field(name=c, value=d, inline=False)
	
	await ctx.author.send(embed=embed)	
	
	# get the help prompt and send it
#	all_lines = h.help_line()
#	for helpline in all_lines:
#		await ctx.send(helpline)

# print out that the bot is ready to go
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

 
# a command to create a draft without pinging all the users -- used for testing purposes
@bot.command()
async def mdnp(ctx):
	d.drafters = md.get_current_coaches(ctx)
	d.base_drafters = md.get_current_coaches(ctx)
	
	# create a list of picks for each user who is signed up to be in the draft
	md.create_pick_lists()
	
	d.draft_order = d.drafters[:]
	d.draft_order = md.flip_and_add(d.draft_order)
	d.drafters = d.base_drafters
	md.initialize_current_next_drafters()
	
	
# last line, used to run the bot  
bot.run(TOKEN)
