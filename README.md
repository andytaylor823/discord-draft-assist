# discord-draft-assist
A Discord bot that automates a Fantasy-style Pokemon draft

-------------------------------------------------------------------------------------------------

WHAT IS A DRAFT LEAGUE?

In a similar manner as Fantasy Football with NFL players, people have created Pokemon Draft Leagues, where each member ("coach") of the league participates in a draft, selecting a squad of 11 Pokemon to be on their roster for the season. Coaches battle one other coach per week, bringing 6 Pokemon from the 11 they drafted to their battle. A coach may bring different Pokemon each week, or the exact same team every time, but they are restricted to the 11 Pokemon they drafted at the beginning of the season. At the end of the season, the league may host playoffs, where the coaches with the best records battle each other in a single-elimination tournament to determine the winning coach of that season.

Like players in Fantasy Football, not all Pokemon are equally good. In Draft Leagues, Pokemon are assigned point values according to their power level. During the draft, coaches spend a pre-determined amount of points to build the best team they can. In the draft league format, each Pokemon may only be drafted by one coach -- there is only one Tapu Koko in the whole league. As leagues grow larger with more active coaches, there are therefore fewer top-tier Pokemon available for each coach, so less-powerful Pokemon will need to be drafted. Often, the best coaches are the ones who are able to make the best use out of their low-tier Pokemon.

During the season, if a coach is unsatisfied with their draft, they may seek trades with other coaches in a Waiver Wire, or they may exchange members of their roster with undrafted Pokemon in the Free Agency. After a trade is completed, the coach's point totals must balance out so that their team is not worth more points than they originally had to spend, ensuring a level playing field for all.

To learn more about the Draft League format, refer to the popular YouTubers ADrive, Emvee, and PokeaimMD. 

-------------------------------------------------------------------------------------------------

ABOUT THIS CODE:

This code uses the Discord package from Python to run a Discord bot that automates a Pokemon Draft League draft. The bot creates a list of coaches participating in the season by pulling all users who have "Current Coaches" in their list of roles. Users may submit picks to the bot, as well as backup picks, and when it is the user's turn in the draft, the bot will automatically fulfill their pick, then advance the draft forward one coach. The ability for coaches to leave picks with the bot means that coaches need not be glued to their computer screen for a few days while the draft takes place.

The code is mainly housed in the "run_bot" script. This script calls on the other scripts in the repository to run the commands necessary for the bot to automate the draft. Each command has its own separate script that the main "run_bot" script calls upon for helper functions. These command scripts are named by adding a "c" to the beginning of each command name (such as "cpick" or "clist").

The remaining files in this directory (defs, error_messages, and functions) support the main script but are not tied to a specific command. The "defs" script is where several important variables are defined so that they may be accessed by all scripts, such as the draft channel (a Discord channel object). The "error_messages" script houses all the possible error messages that may be called upon to respond to various accounted-for errors. Much of the main code consists of error-handling, as we cannot expect the coaches that interact with the bot to always eg. use proper syntax. Finally, the "functions" script contains general functions that are used by several different commands.

-------------------------------------------------------------------------------------------------

MISCELLANEOUS:

Before this code may be run, a unique Discord bot must first be created and added to the appropriate server (eg. steps 2-4 of https://www.digitaltrends.com/gaming/how-to-make-a-discord-bot/). The bot must have the appropriate privileges, as it will create a draft channel when the draft is started. Once the bot is created and added to the server, replace the right-hand side of line 20 in "run_bot.py" with your bot's token. Be sure not to give out this token, as it will allow whomever has it to control your bot!

For any questions on how the commands work or what they do, any user may send the command !help in a channel where the bot is active to be sent a private message on how to interact with the bot. Similarly, one may also refer to the "chelp.py" script in this repository for the same help on how to use the bot.

This code assumes a certain tiering system, similar to the tiers used by the GBA Draft League. If this bot is used for a different draft league with a different tiering system, the Tiers.csv (and trashmons.txt) file(s) will need to be adjusted accordingly.

This bot has been run successfully, but it is still a work-in-progress. If you have any comments or questions about this project, feel free to contact me at andytaylor823@gmail.com. Thanks, and happy drafting!
