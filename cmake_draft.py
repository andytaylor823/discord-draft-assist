import functions as f
import defs as d
import discord
import numpy as np

# initializes the drafter arrays and creates the line saying who started the draft
def initialize(ctx):

	# reset all taken Pokemon
	d.taken_mons = []

	# create arrays of all the users participating in the draft
	d.drafters = md.get_current_coaches(ctx)
	d.base_drafters = md.get_current_coaches(ctx)
	
	# create a list of picks for each user who is signed up to be in the draft
	md.create_pick_lists()
	
	# create the line that says who started the draft
	line = md.draft_created_line(ctx)
	return(line)

# search all users in the server, returns only those who have the role "Current Coaches"
def get_current_coaches(ctx):
	drafters = []
	allusers = ctx.channel.members
	for user in allusers:
		if "Current Coaches" in [y.name for y in user.roles]:
			drafters.append(user)
	return(list(drafters))

# return a line that says who started the draft and who is participating in it
def draft_created_line(ctx):

	line = 'A new draft has been declared by {0.mention}!\n'.format(ctx.author)
	line += '-------------------------------------------------\n'
	line += 'The coaches who will be part of this draft are:\n'
	
	# check if someone has already pre-loaded a draft order (see "defs.py")
	# if not, just use the randomly-generated order already created
	if len(d.pre_loaded_order) == 0:
		for user in d.drafters:
			line += '{0.mention}\n'.format(user)

	# if there is a pre-loaded order, search all Current Coaches for each username and 
	# print them out in the appropriate order
	else:
		names = d.pre_loaded_order
		ccs = get_current_coaches(ctx)
		user_order = []
		for n in names:
			for cc in ccs:
				if n == cc.name:
					user_order.append(cc)
		d.pre_loaded_users = user_order
		for u in user_order:
			line += '{0.mention}\n'.format(u)
	line += '-------------------------------------------------\n'
	line += 'If this list of coaches is incorrect, please be sure the "Current Coaches" role is updated.\n'
#	line += 'Happy drafting!'
	
	return(line)

# create a dictionary for each coach and their pick/backup lists
# the keys are the user objects of each Current Coach, and
# the values are the lists of each of their picks and backups
# initialize all to None
def create_pick_lists():

	l = []
	for i in range(len(d.drafters)):
		l.append(['None']*11)
		
	l1 = []
	for i in range(len(d.drafters)):
		l1.append(['None']*11)
		
	d.lists = {d.drafters[i]:l[i][:] for i in range(len(d.drafters))}
	d.backups = {d.drafters[i]:l1[i][:] for i in range(len(d.drafters))}

# turn the draft order into snake order w/ 11 picks each
def flip_and_add(arr):

	base = arr
	inv = [arr[-i] for i in range(1, len(arr)+1)]
	
	# starts with one length
	# add 5x2 lengths, end with 11 lengths
	new = inv+base
	arr += 5*new
	
	return(arr)

# set the previous, current, next, and on-deck drafters are
def initialize_current_next_drafters():

	d.current_round = 1
	d.current_drafter = d.draft_order[0]
	d.previous_drafter = d.draft_order[0]
	d.next_drafter = d.draft_order[1]
	d.nnext_drafter = d.draft_order[2]
	d.picknum = 1

# line stating that a new draft has been declared
def new_draft_channel_first_line(ctx):

	line = '{} has declared the start of a new draft! Up first is {} with {} on deck!'
	fmt = (ctx.author.mention, d.current_drafter.mention, d.next_drafter.mention)
	return(line, fmt)
