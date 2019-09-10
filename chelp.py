import functions as f
import defs as d
import discord
import numpy as np

# this is now obsolete -- see the function help()
# returns a line about each useful command in this whole code
def help_line():

	l = '--------------------------------------------\n'
	l1 = '**Command:** !pick\n'
	l2 = 'To select your next draft pick, use the command "!pick ROUND, POKEMON, TIER". This command only works in a PM with me.\n'
	l3 = 'Common errors in this command come from your spelling/capitalization of the Pokemon\'s name not agreeing with mine. I take my data from the most recently updated Porch League spreadsheet.\n'
	l4 = 'Acceptable tier names are 1, 2, 3, 4, 5, M1, M2, and M3.\n'
	help1 = l + l1 + l2 + l3 + l4 + l
	
	l5 = '**Command:** !backup\n'
	l6 = 'To select a backup draft pick in case your primary gets sniped, use the command "!backup ROUND, POKEMON, TIER"\n'
	help2 = l + l5 + l6 + l3 + l4 + l
	
	l7 = '**Command:** !delpick\n'
	l8 = 'It is possible to overwrite a future pick using the command !pick, but this command is for when you want to remove your pick entirely, setting it to "None". This command only works in a PM with me.'
	l9 = 'To delete a pick entirely from your list, use the command "!delpick ROUND, WHICH"\n'
	l10 = 'Here, the argument "WHICH" accepts two values: "p" and "b". The former deletes your primary pick (and replaces it with your backup, if it exists). The latter deletes your backup pick and does not replace it.'
	help3 = l + l7 + l8 + l9 + l10 + l
	
	l11 = '**Command:** !list\n'
	l12 = 'To see a list of your future picks that you have queued up, use the command "!list". This command only works in a PM with me.'
	l13 = 'This command takes no arguments.'
	help4 = l + l11 + l12 + l13 + l
	
	return(help1, help2, help3, help4)

# returns an array of the commands and an array of the descriptions of each command
# uses the cool-looking Embed from discord
def help():

	c1 = '!pick ROUND, PKMN, TIER'
	d1 = 'The "pick" command is used to select a future draft pick. This command only works in a PM with me -- don\'t post your !pick in a public channel! To use the command, enter 3 arguments after "!pick": the round you\'re picking for, the Pokemon you want to draft, and the tier that Pokemon is in. The spelling must be exactly the same as on the Porch League sheet, and the only accepted tiers are 1, 2, 3, 4, 5, M1, M2, and M3. Some examples of successful "!pick"s:\n'
	d1 += '!pick 1, Azumarill, 1\n'
	d1 += '!pick 6, Slowbro-Mega, M2\n'
	d1 += '!pick 11, Dugtrio-Alola, 5\n'
	d1 += '!pick 2, Dugtrio, 2           (bad -- should be "Dugtrio (Arena Trap)")'
	
	c2 = '!backup ROUND, PKMN, TIER'
	d2 = 'The "backup" command is used to select a backup for a future round, in case your primary gets sniped. Similar to the "pick" command, this only works in a PM with me. The syntax is exactly the same as in the "pick" command.'
	
	c3 = '!delpick ROUND, WHICH'
	d3 = 'The "delpick" command is used to completely delete a pick from your queue. While the "pick" and "backup" comands can be used to overwrite future picks, they are incapable of being used to pause the draft. If you accidentally queue up the wrong Pokemon with the "pick" command but don\'t know what you want to pick in that round yet, the "delpick" command sets your draft for that round to "None", ensuring you don\'t accidentally pick the wrong Pokemon.\n'
	d3 += 'As with the previous two commands, this only works in a PM with me. The argument WHICH only accepts two values, "p" (if you want to delete your primary) or "b" (if you want to delete your backup). Some examples of successful "!delpick"s:\n'
	d3 += '!delpick 3, p\n'
	d3 += '!delpick 10, b'
	
	c4 = '!list'
	d4 = 'The "list" command displays a list of your past and future picks in a list format. As with the three previous commands, this only works in a PM with me. The "list" command takes no arguments. Discord isn\'t very good at spacing, so sorry if it looks ugly...'
	
	c5 = '!make_draft'
	d5 = 'The "make_draft" command starts the drafting process. I will pull from all users in this server with the "Current Coaches" role and compile a drafting order. I will print out the order as I create it and ask if that is okay. If it is, respond with "y", and a drafting channel will be created that I will use to write out users\' picks. If you would rather enter your own order, respond with "n" and follow the prompts to enter in your own draft order.'
	
	c6 = '!draft_order'
	d6 = 'After using the previous command, I should have presented you with my list of the preliminary draft order. If a different draft order is desired, the "draft_order" command allows users to set the draft order by hand. When prompted, tag users with the "@" symbol in the correct draft order.'
	
	commands = [c1, c2, c3, c4, c5, c6]
	descriptions = [d1, d2, d3, d4, d5, d6]
	
	return(commands, descriptions)
