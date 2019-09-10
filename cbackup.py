import functions as f
import defs as d
import discord
import error_messages as em
import numpy as np

# look for bad input with the error functions defined here
def check_bad_input(ctx, rd, pokemon, tier):

	testfns = [check_no_primary_yet, check_backup_equals_primary]
	e = ''
	i = 0
	while e == '' and i < len(testfns):
		e = testfns[i](ctx, rd, pokemon, tier)
		i += 1
	return(e)

# check if the user has not already selected a primary
# if they have, they can't select a backup
def check_no_primary_yet(ctx, rd, pokemon, tier):

	rd = int(rd)
	user = ctx.author
	if d.lists[user][rd-1] == 'None':
		return(em.no_primary_yet)
	return('')

# the user can't select the same backup as their primary
def check_backup_equals_primary(ctx, rd, pokemon, tier):

	user = ctx.author
	rd = int(rd)
	user_primary = d.lists[user][rd-1]
	
	if user_primary == pokemon:
		return(em.backup_equals_primary)
	return('')

# if the command has been entered correctly, apply the backup
def apply_backup(ctx, rd, pokemon, tier):

	author = ctx.author
	msg = 'Done! I have registered your Round {} backup as {} (Tier {})!\n'
	msg = msg.format(str(rd), pokemon, str(tier))
	msg += 'Remember, you can use the command "!list" at any time to see the list of the picks you have made and the ones you have planned!'
	d.backups[author][int(rd)-1] = pokemon
	return(msg)
