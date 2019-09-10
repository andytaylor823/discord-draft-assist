import discord
from discord.ext import commands
import numpy as np

# just a bunch of variables that are referred to throughout the system of codes

drafters = []
base_drafters = []
lists = []
backups = []
draft_order = []
taken_mons = []

# the draft channel object, created in make_draft
dc = 'hello'

current_round = 1
picknum = 1
current_drafter = ''
previous_drafter = ''
next_drafter = ''
nnext_drafter = ''

# if the draft order is generated randomly somewhere else, write it here, 
# where each entry is the username of each Coach in the appropriate order
pre_loaded_order = ['AndyT', 'TheBruddamaster', 'shaunald']
#pre_loaded_order = []

pre_loaded_users = []
