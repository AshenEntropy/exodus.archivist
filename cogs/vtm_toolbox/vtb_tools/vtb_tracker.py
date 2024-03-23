import discord
import discord.ui
from zenlog import log

import misc.config.main_config as mc

import cogs.vtm_toolbox.vtb_misc.vtb_utils as vu
import cogs.vtm_toolbox.vtb_misc.vtb_pages as vp
import cogs.vtm_toolbox.vtb_tools.vtb_roller as vr
import cogs.vtm_toolbox.vtb_characters.vtb_character_manager as cm

health_or_willpower_options = [discord.SelectOption(label='One', value='1', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Two', value='2', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Three', value='3', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Four', value='4', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Five', value='5', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Six', value='6', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Seven', value='7', emoji='<:snek:785811903938953227>'),
                               discord.SelectOption(label='Eight', value='8', emoji='<:snek:785811903938953227>')]


async def return_to_home(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
    page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'mint')
    await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
    return None


async def go_to_roller(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Home', '', 'purple')
    page: discord.Embed = await vp.standard_roller_page_modifications(page, CHARACTER)
    await interaction.response.edit_message(embed=page, view=vr.Home(self.CLIENT))
    return None


class Home(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Attributes', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def attributes_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Attributes Page', '', 'mint')

        ATTRIBUTES: tuple = \
            ('strength', 'dexterity', 'stamina', 'charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve')
        CHARACTER_DATA: dict = await CHARACTER.__get_values__(ATTRIBUTES, 'attributes')

        physical_impairment_flag: bool = False
        HEALTH_BASE: int = await CHARACTER.__get_value__('base_health', 'health')
        HEALTH_SUPERFICIAL_DAMAGE: int = await CHARACTER.__get_value__('superficial_health_damage', 'health')
        if HEALTH_BASE <= HEALTH_SUPERFICIAL_DAMAGE:
            page.add_field(name='Physically Impaired.', value='-1 to Physical Dice Pools', inline=False)
            physical_impairment_flag = True

        mental_impairment_flag: bool = False
        WILLPOWER_BASE: int = await CHARACTER.__get_value__('base_willpower', 'willpower')
        WILLPOWER_SUPERFICIAL_DAMAGE: int = await CHARACTER.__get_value__('superficial_willpower_damage', 'willpower')
        if WILLPOWER_BASE <= WILLPOWER_SUPERFICIAL_DAMAGE:
            page.add_field(name='Mentally Impaired', value='-1 to Social & Mental Dice Pools', inline=False)
            mental_impairment_flag = True

        for_var = 0
        for x in ATTRIBUTES:
            if for_var % 3 == 0:
                page.add_field(name='', value='', inline=False)
            count = CHARACTER_DATA[ATTRIBUTES[for_var]]

            # don't like this, but will cope
            if physical_impairment_flag is True or mental_impairment_flag is True:
                if ATTRIBUTES[for_var].lower() in ('strength', 'dexterity', 'stamina'):
                    count -= 1  # Removes one from PHYSICAL attributes since the character is PHYSICALLY impaired.

                if ATTRIBUTES[for_var].lower() in ('charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve'):
                    count -= 1  # Removes one from MENTAL & SOCIAL attributes since the character is MENTALLY impaired.

            emojis = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'

            page.add_field(name=f'{ATTRIBUTES[for_var].capitalize()}', value=f'{emojis}', inline=True)
            for_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Health & Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def hpwp_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def physical_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Physical Skills Page', '', 'mint')

        PHYSICAL_SKILLS: tuple = ('athletics', 'brawl', 'craft', 'drive', 'firearms', 'larceny', 'melee', 'stealth', 'survival')
        PHYSICAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(PHYSICAL_SKILLS, 'skills/physical')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = PHYSICAL_SKILLS_DICT[PHYSICAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(PHYSICAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Social Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def social_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Social Skills Page', '', 'mint')

        SOCIAL_SKILLS: tuple = ('animal_ken', 'etiquette', 'insight', 'intimidation', 'leadership', 'performance', 'persuasion', 'streetwise', 'subterfuge')
        SOCIAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(SOCIAL_SKILLS, 'skills/social')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = SOCIAL_SKILLS_DICT[SOCIAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'

            # This is a special case, because just str.capitalize() will result in the string being 'Animal_ken'
            # I'll sacrifice a little bit of performance, Python isn't supposed to be fast anyway
            if SOCIAL_SKILLS[while_var] == 'animal_ken':
                page.add_field(name=f'Animal Ken', value=f'{emoji}', inline=True)
            else:
                page.add_field(name=f'{str.capitalize(SOCIAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Mental Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def mental_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Mental Skills Page', '', 'mint')

        MENTAL_SKILLS: tuple = ('academics', 'awareness', 'finance', 'investigation', 'medicine', 'occult', 'politics', 'science', 'technology')
        MENTAL_SKILLS_DICT: dict = await CHARACTER.__get_values__(MENTAL_SKILLS, 'skills/mental')

        while_var: int = 0
        while while_var != 9:  # 9 = Skill Count
            count: int = MENTAL_SKILLS_DICT[MENTAL_SKILLS[while_var]]
            emoji: str = f'{count * mc.DOT_FULL_EMOJI} {abs(count - 5) * mc.DOT_EMPTY_EMOJI}'
            page.add_field(name=f'{str.capitalize(MENTAL_SKILLS[while_var])}', value=f'{emoji}', inline=True)
            while_var += 1

        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Hunger', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def hunger_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.hunger_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=Hunger(self.CLIENT))
        return

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def extras_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Extras', '', 'mint')
        await interaction.response.edit_message(embed=page, view=Extras(self.CLIENT))
        return


class Home_n_Roll(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return


class HP_n_WP(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return

    @discord.ui.button(label='Mend', emoji=f'{mc.HUNGER_EMOJI}', style=discord.ButtonStyle.red, row=2)
    async def mend_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        BLOOD_POTENCY: int = await CHARACTER.__get_value__('blood_potency', 'misc')
        if BLOOD_POTENCY <= 1: mend_amount = 1
        elif BLOOD_POTENCY <= 3: mend_amount = 2
        elif BLOOD_POTENCY <= 7: mend_amount = 3
        elif BLOOD_POTENCY <= 9: mend_amount = 4
        elif BLOOD_POTENCY == 10: mend_amount = 5
        else: raise ValueError

        SUPERFICIAL_HEALTH_DAMAGE: int = await CHARACTER.__get_value__('superficial_health_damage', 'health')

        # Prevents a Rouse from occurring if no health can be gained.
        if SUPERFICIAL_HEALTH_DAMAGE == 0:
            page: discord.Embed = await vp.hp_wp_page_builder(interaction)
            page.add_field(name='No Superficial Health to Regain', value='')
            await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
            return

        ROUSE_RESULT: tuple = await CHARACTER.__rouse_check__()
        if ROUSE_RESULT[0] == 'Frenzy' == 'Frenzy':  # .__rouse_check__ handles Frenzy
            return

        # Can't heal damage you don't have
        if mend_amount > SUPERFICIAL_HEALTH_DAMAGE:
            mend_amount = SUPERFICIAL_HEALTH_DAMAGE

        await CHARACTER.__update_value__('superficial_health_damage', int(SUPERFICIAL_HEALTH_DAMAGE - mend_amount), 'health')

        page: discord.Embed = await vp.hp_wp_page_builder(interaction)

        page.add_field(name=f'Rouse {ROUSE_RESULT[0]}', value=f'`{mend_amount}` Health Regained. New Hunger: {ROUSE_RESULT[1] * mc.HUNGER_EMOJI}')
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Take HP/WP Damage', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def to_damage_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return None


class HP_n_WP_Damage(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Return', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def return_to_hpwp_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Superficial HP Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=0)
    async def hp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_HEALTH: int = await CHARACTER.__get_value__('base_health', 'health')

        while damage_amount > 0:
            HEALTH_DAMAGE: dict = await CHARACTER.__get_values__(('superficial_health_damage', 'aggravated_health_damage'), 'health')
            AGG_DMG = HEALTH_DAMAGE['aggravated_health_damage']
            SUP_DMG = HEALTH_DAMAGE['superficial_health_damage']

            if BASE_HEALTH == AGG_DMG:
                # Set up torpor logic later
                # ENTER TORPOR HERE
                log.crit('Someone Torpor\'d')
            elif BASE_HEALTH == SUP_DMG:  # Deals AGG Damage
                await CHARACTER.__update_value__('aggravated_health_damage', int(AGG_DMG + 1), 'health')
            else:  # Deals SUP Damage
                await CHARACTER.__update_value__('superficial_health_damage', int(SUP_DMG + 1), 'health')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Aggravated HP Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=1)
    async def hp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_HEALTH: int = await CHARACTER.__get_value__('base_health', 'health')

        while damage_amount > 0:
            AGG_DMG: int = await CHARACTER.__get_value__('aggravated_health_damage', 'health')

            if BASE_HEALTH == AGG_DMG:
                # Set up torpor logic later
                # ENTER TORPOR HERE
                log.crit('Someone Torpor\'d')
                return

            await CHARACTER.__update_value__('aggravated_health_damage', int(AGG_DMG + 1), 'health')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Superficial WP Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=2)
    async def wp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_WILLPOWER: int = await CHARACTER.__get_value__('base_willpower', 'willpower')

        while damage_amount > 0:
            WILLPOWER_DAMAGE: dict = await CHARACTER.__get_values__(('superficial_willpower_damage', 'aggravated_willpower_damage'), 'willpower')
            AGG_DMG = WILLPOWER_DAMAGE['aggravated_willpower_damage']
            SUP_DMG = WILLPOWER_DAMAGE['superficial_willpower_damage']

            if BASE_WILLPOWER == SUP_DMG:  # Deals AGG Damage
                await CHARACTER.__update_value__('aggravated_willpower_damage', int(AGG_DMG + 1), 'willpower')
            else:  # Deals SUP Damage
                await CHARACTER.__update_value__('superficial_willpower_damage', int(SUP_DMG + 1), 'willpower')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Aggravated WP Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=3)
    async def wp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)

        damage_amount: int = int(select.values[0])

        BASE_WILLPOWER: int = await CHARACTER.__get_value__('base_willpower', 'willpower')

        while damage_amount > 0:
            AGG_DMG: int = await CHARACTER.__get_value__('aggravated_willpower_damage', 'willpower')
            await CHARACTER.__update_value__('aggravated_willpower_damage', int(AGG_DMG + 1), 'willpower')
            damage_amount -= 1

        page: discord.Embed = await vp.hp_wp_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return


class Hunger(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Predator Type', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=2)
    async def predator_type_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(CHARACTER, 'Predator Type Information', '', 'mint')

        PREDATOR_TYPE: str = await CHARACTER.__get_value__('predator_type', 'misc')
        SUPPORTED_PREDATOR_TYPES: tuple = ('SECRET_PREDATOR_TYPE', 'Grim Reaper', 'Sandman',
                                           'Cryptid', 'Alleycat', 'Grave Robber', 'Trapdoor')

        if PREDATOR_TYPE not in SUPPORTED_PREDATOR_TYPES:
            log.error('**> Bad PREDATOR_TYPE given to hunger_page_builder()')
            return

        match PREDATOR_TYPE:
            case 'SECRET_PRED_TYPE':
                pt_pool: str = ''  # Mechanical Stuff
                pt_desc: str = ''
                pt_disciplines: str = ''  # The potential disciplines gained from the predator type
                pt_spec: str = ''  # Specialty/ies from pt
                pt_merit: str = ''  # Advantages/Merits given by pt
                pt_flaws: str = ''  # Flaws given by pt

            case 'Grim Reaper':
                pt_pool: str = 'Intelligence + Awareness/Medicine in order to find victims.'
                pt_desc: str = ('Hunting inside hospice care facilities, assisted living homes, and other places where those'
                                ' who are near death reside. Grim Reapers are constantly on the move in an effort to locate '
                                'new victims near the end of their lives to feed from. Hunting in this style may also earn a'
                                ' taste for specific diseases making them easier to identify. ')
                pt_disciplines: str = 'Auspex or Oblivion (Necromancy/Obtenebration)'
                pt_spec: str = 'Awareness (Death) or Larceny (Forgery)'
                pt_merit: str = 'One dot of Allies or Influence associated with the medical community & Gain 1 Humanity'
                pt_flaws: str = '(•) Prey Exclusion (Healthy Mortals)'

            case 'Sandman':
                pt_pool: str = 'Dexterity + Stealth is for casing a location, breaking in and feeding without leaving a trace.'
                pt_desc: str = ('If they never wake during the feed it never happened, right? Sandman prefers to hunt on '
                                'sleeping mortals than anyone else by using stealth or Disciplines to feed from their '
                                'victims they are rarely caught in the act, though when they are, problems are sure to occur'
                                '. Maybe they were anti-social in life or perhaps they find the route of seduction or '
                                'violence too much for them and find comfort in the silence of this feeding style. ')
                pt_disciplines: str = 'Auspex or Obfuscate'
                pt_spec: str = 'Medicine (Anesthetics) or Stealth (Break-in)'
                pt_merit: str = 'Gain one dot of Resources'
                pt_flaws: str = 'None!'

            case 'Cryptid':
                pt_pool: str = ''
                pt_desc: str = ('Nobody believes in vampires, right? Well, not "nobody", exactly. Know what nobody-nobody '
                                'believes in? Aliens, chupacabras, and sasquatches. You have concocted some incredibly '
                                'fanciful identity for yourself in which you present yourself as some obscure piece of '
                                'occult apocrypha. True Believers are so ready to believe in ghosts or mermaids or whatever,'
                                ' that it will never occur to them you\')re a vampire. Some even seek to serve their '
                                'paranormal masters. "After the probe, the alien took blood samples." "The chupacabra jumped'
                                ' out of nowhere! It got my dog!" "The succubus appears at midnight, and it feels sooo good!"'
                                ' "The Delaware Water Gap Mermaid? That\'s just a tourist legend, still, be careful if you '
                                'swim or boat at night."')
                pt_disciplines: str = 'Obfuscate, Dominate, or Clan Specific'
                pt_spec: str = 'Occult (Cryptids) or Performance (Impersonating Urban Legends)'
                pt_merit: str = 'Three Dots to spend between Herd and/or Retainer'
                pt_flaws: str = 'Stalkers & Suspect'

            case 'Alleycat':
                pt_pool: str = 'Strength + Brawl is to take blood by force or threat. Wits + Streetwise can be used to find criminals as if a vigilante figure.'
                pt_desc: str = ('Those who find violence to be the quickest way to get what they want might gravitate '
                                'towards this hunting style. Alleycats are a vampire who feeds by brute force and outright '
                                'attack and feeds from whomever they can when they can. Intimidation is a route easily taken'
                                ' to make their victims cower or even Dominating the victims to not report the attack or '
                                'mask it as something else entirely.')
                pt_disciplines: str = 'Celerity or Potence'
                pt_spec: str = 'Intimidation (Stickups) or Brawl (Grappling)'
                pt_merit: str = 'Gain three dots of Criminal Contacts'
                pt_flaws: str = 'Lose 1 Humanity'

            case 'Grave Robber':
                pt_pool: str = ('Resolve + Medicine for sifting through the dead for a body with blood. Manipulation + '
                                'Insight for moving among miserable mortals.')
                pt_desc: str = ('Similar to Baggers these kindred understand there\'s no good in wasting good blood, even if'
                                ' others cannot consume it. Often they find themselves digging up corpses or working or '
                                'mortuaries to obtain their bodies, yet regardless of what the name suggests, they prefer '
                                'feeding from mourners at a gravesite or a hospital. This Predator Type often requires a '
                                'haven or other connections to a church, hospital, or morgue as a way to obtain the bodies. ')
                pt_disciplines: str = 'Fortitude or Oblivion (Necromancy)'
                pt_spec: str = 'Occult (Grave Rituals) or Medicine (Cadavers)'
                pt_merit: str = 'Feeding Merit (•••) Iron Gullet & Haven Advantage (•)'
                pt_flaws: str = 'Herd Flaw: (••) Obvious Predator'

            case 'Trapdoor':
                pt_pool: str = ('Charisma + Stealth for the victims that enter expecting a fun-filled night. Dexterity + '
                                'Stealth to feed upon trespassers. Wits + Awareness + Haven dots is used to navigate the '
                                'maze of the den itself. ')
                pt_desc: str = ('Much like the spider, this vampire builds a nest and lures their prey inside. Be it an '
                                'amusement park, an abandoned house, or an underground club, the victim comes to them. '
                                'There the trapdoor might only play with their mind and terrorize them, imprison them to '
                                'drain them slowly, or take a deep drink and then send them home. ')
                pt_disciplines: str = 'Protean or Obfuscate'
                pt_spec: str = 'Persuasion (Marketing) or Stealth (Ambushes or Traps)'
                pt_merit: str = 'Gain one dot of Haven & Gain one dot of either Retainers or Herd, or a second Haven dot.'
                pt_flaws: str = 'Gain one Haven Flaw, either (•) Creepy or (•) Haunted.'

            case _:
                log.error('**> How did we get here? (vtb_pages "case _:")')
                return

        page.add_field(name='Predator Type', value=f'{PREDATOR_TYPE}', inline=True)
        page.add_field(name='PT Pool', value=f'{pt_pool}', inline=False)
        page.add_field(name='PT Description', value=f'{pt_desc}', inline=False)
        page.add_field(name='PT Discipline(s)', value=f'{pt_disciplines}', inline=True)
        page.add_field(name='PT Specialty(ies)', value=f'{pt_spec}', inline=True)
        page.add_field(name='PT Merit(s)', value=f'{pt_merit}', inline=True)
        page.add_field(name='PT Flaw(s)', value=f'{pt_flaws}', inline=True)

        await interaction.response.edit_message(embed=page, view=Predator_Type(self.CLIENT))
        return None


class Predator_Type(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Return', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def return_to_hunger_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.hunger_page_builder(CHARACTER)
        await interaction.response.edit_message(embed=page, view=Hunger(self.CLIENT))
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return


class Extras(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Home', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def home_button_callback(self, interaction, button):
        await return_to_home(self, interaction)
        return

    @discord.ui.button(label='Roll', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.red, row=1)
    async def roll_button_callback(self, interaction, button):
        await go_to_roller(self, interaction)
        return

    @discord.ui.button(label='Diablerie', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def diablerie_button_callback(self, interaction, button):
        raise NotImplementedError

    @discord.ui.button(label='Remorse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def remorse_button_callback(self, interaction, button):
        raise NotImplementedError

    @discord.ui.button(label='Path Rules', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def path_rules_button_callback(self, interaction, button):
        raise NotImplementedError
