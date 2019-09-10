import functions as f
import defs as d
import discord
import numpy as np

# check if not a PM and check if the user is not in "Current Coaches"
def is_error_input(ctx):
	if not f.is_pm(ctx):
		return True

	user = ctx.author
	if user not in d.drafters:
		return True
	return False

# retreive the list of picks and number of picks for a given user
def get_user_picks(ctx):

	user = ctx.author
	allpickers = d.draft_order[:d.picknum-1]
	num_user_picks = sum(np.array(allpickers) == user)
	user_list = d.lists[user]
	
	return(user_list, num_user_picks)

# get the line to be printed out of all a user's picks
# TODO: update this with cool Embed
def get_list_line(ctx, user_list, num_user_picks):

	
	user = ctx.author
	line = 'List of your draft picks (successful picks in strikethrough, future picks in bold, backups in parenthesis):\n'
	
	# use discord's strikethrough on all picks that have been made so far
	for i in range(num_user_picks):
		line += str(i+1) + '.) ~~' + user_list[i] + '~~\n'
	
	# print out the future picks of a user, bolding the ones that aren't "None"
	for j in range(num_user_picks, len(user_list)):
		line += str(j+1) + '.) '
		if user_list[j] != 'None':
			line += '**' + str(user_list[j]) + '**'
		else:
			line += user_list[j]
			
		if d.backups[user][j] != 'None':
			line += '           (' + d.backups[user][j] + ')'
		line += '\n'
	
	# Embed looks cooler
	line += 'Sorry if the spacing looks bad. Discord isn\'t really good at aligning spaces...'
	return(line)
