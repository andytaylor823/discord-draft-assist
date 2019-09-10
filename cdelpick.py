import functions as f
import defs as d
import discord
import error_messages as em
import numpy as np

# check for bad input with the error functions defined here
def check_bad_input(ctx, rd, which):

	e = ''
	i = 0
	test_fns = [check_bad_rd, check_past_this_round, check_no_pick_yet, check_bad_which]
	while e == '' and i < len(test_fns):
		e = test_fns[i](ctx, rd, which)
		i += 1
		
	return(e)

# rounds must be integers and between 1 and 11 inclusive
def check_bad_rd(ctx, rd, which):

	try:
		rd = float(rd)
		if int(rd) != rd:				return(em.bad_rd)
	except(ValueError):					return(em.bad_rd)
	if rd not in range(1, 12):				return(em.bad_rd2)
	return('')

# can't edit picks that have already been made
def check_past_this_round(ctx, rd, which):
	
	user = ctx.author
	allpickers = d.draft_order[:d.picknum-1]
	num_user_picks = sum(np.array(allpickers) == user)
	if int(rd) <= num_user_picks:
		return(em.past_this_round)
	return('')

# check if the "which" argument is bad (isn't either "p" or "b")
def check_bad_which(ctx, rd, which):

	if which.lower() not in ['p', 'b']:
		return(em.which_to_delete)
	return('')

# can't delete a pick if one does not exist yet
def check_no_pick_yet(ctx, rd, which):

	user = ctx.author
	r = int(rd)-1
	if which.lower() == 'b':
		if d.backups[user][r] == 'None':
			return(em.cant_delete_empty)
	else:
		if d.lists[user][r] == 'None':
			return(em.cant_delete_empty)
	
	return('')

# if there's no errors, apply the delete and send a confirmation message
def apply_delete(ctx, rd, which):

	user = ctx.author
	r = int(rd)-1
	
	# three possible cases, confirmation for each
	m1 = "Done! I have deleted your Round {} primary pick and replaced it with your current backup pick.".format(rd)
	m2 = "Done! I have deleted your Round {} primary pick. You had no backup pick listed, so you will need to pick a new Pokemon for this round.".format(rd)
	m3 = "Done! I have deleted your Round {} backup pick.".format(rd)
	
	mend = "\nFeel free to check your list of future picks at any time using the command \"!list\" to make sure I did this right."
	
	# apply the deletion
	if which.lower() == 'p':
		if d.backups[user][r] != 'None':
			d.lists[user][r] = d.backups[user][r]
			d.backups[user][r] = 'None'
			return(m1 + mend)
		else:
			d.lists[user][r] = 'None'
			return(m2 + mend)
	elif which.lower() == 'b':
		d.backups[user][r] = 'None'
		return(m3 + mend)
	# it should never get to here
	else:
		return("Something went catastrophically wrong. Nothing has been changed, but try again...differently?")
