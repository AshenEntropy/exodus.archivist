ExodusAutomaton
===
---
## Version Info

> * Branch: new_character_system
> * Version 01.02.02
> > * Major: 01 | Large Overhauls
> > * Minor: 02 | Non-Major Features
> > * Patch: 02 | Other Repo Pushes
> * State: Stable
> * DateTime: Feb 16th 2024 | 2:35am

---
## General

As of now ExodusAutomaton Rewrite is being solo developed by me with Pycharm Professional. 
It's not *good* in any sense of the word, it exclusively exists for me to mess around with programming; if for whatever 
reason you'd like to talk to me about the project, your best place to contact me is discord `.ashywinter`
### Primary Features:
> * Project: 
>> * Easily Setup
>> * Open Source [GNUGPL 3.0]
>> * Logging /w "Syntax" [See Below]
>> * Dangerously Cheesy [so much spaghetti]
>> * In Active Development [FEB 2024]

> * Client: 
>> * Slash Commands
>> * Cog Manager
>> * VTM v5 Toolbox 

> * Active Development Features (varying states of functionality) 
>> * VTM v5 Toolbox [Extending Functionality]
>> * Bot Issue Ticket System [HIATUS]
>> * Notes System [HIATUS]

> * Currently Abandoned Features (may return)
>> * eaTools [Bot Devtools]

> * Rejected Features (no chance)
>> * N/A

---
## USE:
<u>__NOTE:__  This bot is not directly intended for use by other people, but does support such use, please remember to follow the License! </u>

Before using the bot please ensure you understand python, discord.py, 
and the discord developer tools, none of those will be explained here.

> Do ALL the following <u>__BEFORE__</u> trying to run the bot
> 
> * Change the Bot's "TOKEN" [clientConfig.py]
> * Change the Bot's "RUNNER" and "RUNNER_ID" [misc/config/mainConfig.py]
---
## LOGGING
When things are logged they should have a "reason" or prefix attached to the beginning these can be "stacked". 
So if something is a __Minor Error__ *and* comes from a Cog it's prefix would be ``*>`` 
For a __Major Error__ regarding Client __Startup__ would have a prefix of ``***$``

The way in which these are "stacked" is done from top to bottom of the list below. 
Higher they are on the list, the more important/higher "priority" 

> Prefix List
>> SHUTDOWN :: <<<{text}>>> \
>> Error     :: * \
>> Startup   ::  $ \
>> From Tool :: & \
>> From Cog  ::  >
---
