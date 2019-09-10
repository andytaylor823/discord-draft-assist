import discord
from discord.ext import commands
import os
import numpy as np
import pandas
import error_messages as em
import defs as d

# read in all the Pokemon data and all the tiers they're in
tiers = pandas.read_csv('Tiers.csv', engine = 'python')
T1s = [i for i in tiers['Tier 1'] if type(i) == str]
T2s = [i for i in tiers['TIER 2'] if type(i) == str]
T3s = [i for i in tiers['TIER 3'] if type(i) == str]
T4s = [i for i in tiers['TIER 4'] if type(i) == str]
T5s = [i for i in tiers['TIER 5'] if type(i) == str]
T5s += [i for i in tiers['TIER 5 cont'] if type(i) == str]
#################################################
fname = 'trashmons.txt'
trashmons = open(fname, 'r').readlines()
for i in range(len(trashmons)):
	trashmons[i] = trashmons[i][:-1]
T5s += trashmons
#################################################

M1s = [i for i in tiers['Mega 1'] if type(i) == str]
M2s = [i for i in tiers['Mega 2'] if type(i) == str]
M3s = [i for i in tiers['Mega 3'] if type(i) == str]
alltiers = [T1s, T2s, T3s, T4s, T5s, M1s, M2s, M3s]

# returns the arguments separated by commas for a command
def get_args(args):

	args = list(args)
	for i in range(len(args)-1):
		args[i] += ' '
	myargs = ''.join(args).split(', ')
	return(myargs)

# checks if the command was entered in a PM with the bot
def is_pm(ctx):
	if isinstance(ctx.channel, discord.DMChannel):		return(True)
	else:							return(False)

# move the draft ahead one pick
def advance_draft():
	
	# add the mon just picked to the taken_mons list
	taken_mon = d.lists[d.current_drafter][d.current_round-1]
	d.taken_mons.append(taken_mon)
	# delete this round's backup of the user who just picked
	d.backups[d.current_drafter][d.current_round-1] = 'None'
	
	# if we're not done with the draft yet, advance the pick number by 1 and the current drafter by 1 in snake order
	if d.picknum < len(d.draft_order):
		d.picknum += 1
		d.previous_drafter = d.draft_order[d.picknum-2]
		d.current_drafter = d.draft_order[d.picknum-1]
	else:
		d.previous_drafter = d.draft_order[-1]
		d.current_drafter = 'END'
	
	# check if we're near the end
	if len(d.draft_order) > d.picknum:	d.next_drafter = d.draft_order[d.picknum]
	else:					d.next_drafter = 'END'

	if len(d.draft_order) > d.picknum + 1:	d.nnext_drafter = d.draft_order[d.picknum+1]
	else:					d.nnext_drafter = 'END'	
	
	# in snake order, advance the round number if the same drafter appears twice in a row
	if d.current_drafter == d.previous_drafter:
		d.current_round += 1

# find the tier a given Pokemon is in
def get_tier(pokemon):

	for i in range(len(alltiers)):
		if pokemon in alltiers[i]:
			break
	
	if i <= 4:	tiername = str(i+1)
	else:		tiername = 'M' + str(i-4)
	return(tiername)

# returns the line that is printed in the draft channel after a pick is made
def draft_pick_line(next_mon):

	# last pick
	if d.next_drafter == 'END':
		line = '**Round \#{} Pick \#{}:** {} drafts **{}**, Tier {}. Great draft, everyone!'
		fmt = (d.current_round, d.picknum, d.current_drafter.mention, next_mon, get_tier(next_mon))
	# 2nd to last pick
	elif d.nnext_drafter == 'END':
		line = '**Round \#{} Pick \#{}:** {} drafts **{}**, Tier {}. Up next is {}. Almost done!'
		fmt = (d.current_round, d.picknum, d.current_drafter.mention, next_mon, get_tier(next_mon), d.next_drafter.mention)
	# not at the end yet
	else:
		line = '**Round \#{} Pick \#{}:** {} drafts **{}**, Tier {}. Up next is {}, {} is on deck'
		fmt = (d.current_round, d.picknum, d.current_drafter.mention, next_mon, get_tier(next_mon), d.next_drafter.mention, d.nnext_drafter.mention)
	return(line, fmt)

# check if any other coaches had queued up the pokemon that was just taken as one of their picks, called a "snipe"
# search all coaches' primary and backup picks
# this is probably not the most elegant way to do this -- needs some cleaning
# known issue: if the coach who just picked also had the mon queued up, that coach will not get pinged that they were sniped
#              just rely on coaches not doing this, since it doesn't really make sense
def check_if_snipe(next_mon):

	sniped, b_sniped, idxs, b_idxs = [[], [], [], []]
	# loop over all coaches
	for coach in d.lists:
		# check if the coach planned on drafting this mon
		# ignore it if the coach is the one who just drafted it
		if next_mon in d.lists[coach] and coach != d.previous_drafter:
			# if so, add the coach to the list of sniped coaches
			# record all the indices in which that coach was sniped
			sniped.append(coach)
			thislist = np.array(d.lists[coach])
			sniped_idxs = []
			tnf = thislist == next_mon
			for i in range(len(tnf)):
				if tnf[i] == True:
					sniped_idxs.append(i)
			sniped_idxs = np.array(sniped_idxs)
			idxs.append(sniped_idxs)
		# do the same for the backups in each coach
		if next_mon in d.backups[coach]:
			b_sniped.append(coach)
			thisblist = np.array(d.backups[coach])
			b_sniped_idxs = []
			tnf = thisblist == next_mon
			for i in range(len(tnf)):
				if tnf[i] == True:
					b_sniped_idxs.append(i)
			b_sniped_idxs = np.array(b_sniped_idxs)
			b_idxs.append(b_sniped_idxs)
			
	return(sniped, idxs, b_sniped, b_idxs)
					
# for each coach who had their primary / backup sniped,
# return that entry to 'None'					
def delete_sniped(users, idxs, b_users, b_idxs):

	idxs = np.array(idxs)
	for i in range(len(users)):
		user = users[i]
		thisidxs = idxs[i]
		for j in range(len(thisidxs)):
			if d.backups[user][thisidxs[j]] != 'None':
				d.lists[user][thisidxs[j]] = d.backups[user][thisidxs[j]]
				d.backups[user][thisidxs[j]] = 'None'
			else:
				d.lists[user][thisidxs[j]] = 'None'
			
	for i in range(len(b_users)):
		user = b_users[i]
		thisbidxs = b_idxs[i]
		for j in range(len(thisbidxs)):
			d.backups[user][thisbidxs[j]] = 'None'
