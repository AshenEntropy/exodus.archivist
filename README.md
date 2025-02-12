Exodus.Archivist
===
---
## Version Info

> * Branch: main
> * State: Stable
> * Version 01.07.02
> > * First Pair  | Major Features/Major Rewrites
> > * Second Pair | Moderate Features/Moderate Rewrites
> > * Third Pair  | Patches/Other Repo Pushes

---
## General

As of now Exodus.Archivist is being solo developed by me with Pycharm Professional. 
It's not *good* in any sense of the word, it exclusively exists for me to mess around with programming; if for whatever 
reason you'd like to talk to me about the project, your best place to contact me is discord `winter.archivist`
### Primary Features:
> * Project: 
>> * Easily Setup
>> * Open Source [GNUGPL 3.0]
>> * Logging /w "Syntax" [See Below]
>> * In Active Development [DEC 2024]

> * Client: 
>> * Slash Commands
>> * Cog Manager
>> * VTM v5 Toolbox

> * Active Development Features (in order of their varying states of functionality)
>> * VTM v5 Toolbox [Functional | Extending Functionality]
>> * Overseer [Non-Functional Test Build | Working On]
>> * Bot Issue Ticket System [N/A | HIATUS]
>> * Notes System [N/A | HIATUS]

> * Currently Abandoned Features (may return)
>> * eaTools [Bot Devtools]

> * Rejected Features (no/little chance)
>> * Automated Diablerie
>> * Integrated Path of Enlightenment/Humanity Rules

---
## USE:
<u>__NOTE:__  This bot is not directly intended for use by other people, but does support such use, please remember to follow the License! </u>

Before using the bot please ensure you understand python, discord.py, 
and the discord developer tools, none of those will be explained here.

> Do ALL the following <u>__BEFORE__</u> trying to run the bot.
> Details on WHY these exist are found in their respective config files.
> 
> * Change the Bot's "TOKEN" [client_config.py]
> * Change the Bot's "RUNNER" and "RUNNER_ID" [main_config.py]
---
## LOGGING
When things are logged they should have a "reason" or prefix attached to the beginning these can be "stacked". 
So if something is a __Minor Error__ *and* comes from a Cog it's prefix would be ``*>`` 
For a __Major Error__ regarding Client __Startup__ would have a prefix of ``***$``

The way in which these are "stacked" is done from top to bottom of the list below. 
Higher they are on the list, the more important/higher "priority" 

> Prefix List
>> SHUTDOWN  :: <<<{text}>>> \
>> Error     :: * \
>> Startup   :: $ \
>> From Tool :: & \
>> From Cog  :: > \
---
