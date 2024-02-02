ExodusAutomaton Rewrite
===
---
## General

As of now ExodusAutomaton Rewrite is being solo developed by me with Pycharm Professional. \
> Primary Features: 
>> * Project: 
>>> * Easily Setup
>>> * Open Source [GNUGPL 3.0]
>>> * Logging /w "Syntax" [See Below]
>>> * Dangerously Cheesy [so much spaghetti]
>>> * In Active Development [FEB 2024]
>> * Client: 
>>> * Slash Commands
>>> * CogManager
>>> * VTM v5 Toolbox

> Active Development Features:
>> * VTM v5 Toolbox [Currently: Adding Extra Features to /kindred-tracker]
>> * aeTerminal; aka devtools
>> * Bot Related Ticket System; aka easier Issue Reporting

> Heavily Work-In-Progress Features: 
>> * Notes System [Currently on Pause]
---
## USE:
<u>__NOTE:__  This bot is not directly intended for use by other people, but does support such use, please remember to follow the License! </u>

Before using the bot please ensure you understand python, discord.py, and the discord developer tools, none of those will be explained here.
* Change the Bot's TOKEN [found in: client_config.py]
* Change the Bot's RUNNER and RUNNER_ID [found in: misc/config/main_config.py]
---
## LOGGING
When things are logged they should have a "reason" or prefix attached to the beginning these can be "stacked". \
So if something is a __Minor Error__ *and* comes from a Cog it's prefix would be ``*>`` \
For a __Major Error__ regarding Client __Startup__ would have a prefix of ``***$``

The way in which these are "stacked" is done from top to bottom of the list below. \
Higher they are on the list, the more important/higher "priority" \

---
> Prefix List
>> SHUTDOWN :: <<<{text}>>> \
>> Error     :: * \
>> Startup   ::  $ \
>> From Cog  ::  >
---
