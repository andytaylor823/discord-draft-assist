import functions as f
import defs as d
import discord
import error_messages as em
import numpy as np

# check for bad input using the functions defined here
def check_bad_pick_input(ctx, rd, pokemon, tier):

	e = ''
	i = 0
	test_fns = [check_bad_rd, check_bad_pkmn, check_bad_tier, check_past_this_round, check_already_taken, check_pick_two_megas]
	while e == '' and i < len(test_fns):
		e = test_fns[i](ctx, rd, pokemon, tier)
		i += 1
		
	return(e)

# round must be an integer and between 1 and 11, inclusive
def check_bad_rd(ctx, rd, pokemon, tier):

	try:
		rd = float(rd)
		if rd != int(rd):			return(em.bad_rd)
	except(ValueError):				return(em.bad_rd)		
	if rd not in range(1, 12):			return(em.bad_rd2)
	return('')

# check if the user spelled the Pokemon right	
def check_bad_pkmn(ctx, rd, pokemon, tier):

	for tier in f.alltiers:
		if pokemon in tier:
			return('')
	return(em.bad_pkmn)

# make sure the user knows which tier the pokemon they entered is in	
def check_bad_tier(ctx, rd, pokemon, tier):
	
	# find the index of the tier that the pokemon is actually correctly in
	for i in range(len(f.alltiers)):
		if pokemon in f.alltiers[i]:
			break
	
	if i <= 4:	tiername = str(i+1)
	else:		tiername = 'M' + str(i-4)

	if tier != tiername:				return(em.bad_tier.format(pokemon, str(tier), str(tiername)))
	return('')

# can't pick a Pokemon that has already been taken
def check_already_taken(ctx, rd, pokemon, tier):

	if pokemon in d.taken_mons:
		return(em.already_taken)
	return('')

# can't adjust your picks in a round that has already passed
def check_past_this_round(ctx, rd, pokemon, tier):
	
	user = ctx.author
	allpickers = d.draft_order[:d.picknum-1]
	num_user_picks = sum(np.array(allpickers) == user)
	if int(rd) <= num_user_picks:
		return(em.past_this_round)
	return('')

# make sure users can only choose one mega, only allows users to select megas in one round
# this may not be necessary if users are capable of self-policing on this
def check_pick_two_megas(ctx, rd, pokemon, tier):

	user = ctx.author
	idx = -1
	rd = int(rd)
	if tier == 'M1' or tier == 'M2' or tier == 'M3':
		for i in range(len(d.lists[user])):
			if '-Mega' in d.lists[user][i] or '-Mega' in d.backups[user][i]:
				idx = i
				break
		if idx != -1 and idx != rd-1:
			return(em.pick_two_megas)
	return('')

# if no errors, apply the pick and send a confirmation message
def apply_pick(author, rd, pokemon, tier):

	msg = 'Done! I have registered your Round {} pick as {} (Tier {})!\n'
	msg = msg.format(str(rd), pokemon, str(tier))
	msg += 'Remember, you can use the command "!list" at any time to see the list of the picks you have made and the ones you have planned!'
	d.lists[author][int(rd)-1] = pokemon
	return(msg)

# check if the pick just made is the next pick in the draft	
def is_next_pick(ctx, rd, pokemon, tier):

	return(d.current_drafter == ctx.author and d.current_round == int(rd))	
