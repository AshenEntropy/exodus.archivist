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
    page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'mint')
    await interaction.response.edit_message(embed=page, view=Home(self.CLIENT))
    return None


async def go_to_roller(self, interaction: discord.Interaction) -> None:
    CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
    page: discord.Embed = await vp.basic_page_builder(interaction, 'Home', '', 'purple')
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
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Attributes Page', '', 'mint')

        attributes: tuple = \
            ('strength', 'dexterity', 'stamina', 'charisma', 'manipulation', 'composure', 'intelligence', 'wits', 'resolve')
        character_data: dict = await CHARACTER.__get_values__(attributes, 'attributes')

        emoji_result = f'{character_data["strength"] * mc.DOT_FULL_EMOJI} {abs(character_data["strength"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Strength', value=emoji_result, inline=True)

        emoji_result = f'{character_data["dexterity"] * mc.DOT_FULL_EMOJI} {abs(character_data["dexterity"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Dexterity', value=emoji_result, inline=True)

        emoji_result = f'{character_data["stamina"] * mc.DOT_FULL_EMOJI} {abs(character_data["stamina"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Stamina', value=emoji_result, inline=True)

        page.add_field(name='', value='', inline=False)

        emoji_result = f'{character_data["charisma"] * mc.DOT_FULL_EMOJI} {abs(character_data["charisma"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Charisma', value=emoji_result, inline=True)

        emoji_result = f'{character_data["manipulation"] * mc.DOT_FULL_EMOJI} {abs(character_data["manipulation"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Manipulation', value=emoji_result, inline=True)

        emoji_result = f'{character_data["composure"] * mc.DOT_FULL_EMOJI} {abs(character_data["composure"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Composure', value=emoji_result, inline=True)

        page.add_field(name='', value='', inline=False)

        emoji_result = f'{character_data["intelligence"] * mc.DOT_FULL_EMOJI} {abs(character_data["intelligence"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Intelligence', value=emoji_result, inline=True)

        emoji_result = f'{character_data["wits"] * mc.DOT_FULL_EMOJI} {abs(character_data["wits"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Wits', value=emoji_result, inline=True)

        emoji_result = f'{character_data["resolve"] * mc.DOT_FULL_EMOJI} {abs(character_data["resolve"] - 5) * mc.DOT_EMPTY_EMOJI}'
        page.add_field(name='Resolve', value=emoji_result, inline=True)
        await interaction.response.edit_message(embed=page, view=Home_n_Roll(self.CLIENT))
        return

    @discord.ui.button(label='Health & Willpower', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def hpwp_button_callback(self, interaction, button):
        page: discord.Embed = await vp.hp_wp_page_builder(interaction)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.button(label='Physical Skills', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=0)
    async def physical_skills_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Physical Skills Page', '', 'mint')

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
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Social Skills Page', '', 'mint')

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
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Mental Skills Page', '', 'mint')

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

    @discord.ui.button(label='Extras', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=1)
    async def extras_button_callback(self, interaction, button):
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Extras', '', 'mint')
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
        CHARACTER: cm.vtb_Character = cm.vtb_Character(interaction)  # This is kept so the __init__ can run the owner checker
        page: discord.Embed = await vp.basic_page_builder(interaction, 'Take HP/WP Damage', '', 'mint')
        await interaction.response.edit_message(embed=page, view=HP_n_WP_Damage(self.CLIENT))
        return None


class HP_n_WP_Damage(discord.ui.View):
    def __init__(self, CLIENT):
        super().__init__()
        self.CLIENT = CLIENT

    @discord.ui.button(label='Return', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.blurple, row=4)
    async def return_to_hpwp_button_callback(self, interaction, button):
        page: discord.Embed = await vp.hp_wp_page_builder(interaction)
        await interaction.response.edit_message(embed=page, view=HP_n_WP(self.CLIENT))
        return

    @discord.ui.select(placeholder='Take Superficial Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=0)
    async def hp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        character_name: str = await vU.getCharacterName(interaction)
        damage_amount: int = int(select.values[0])

        with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])

            while damage_amount > 0:
                hc_sup: int = int(cursor.execute('SELECT healthSUP from health').fetchone()[0])
                hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])

                if hc_base == hc_agg:
                    # Set up torpor logic later
                    # ! ENTER TORPOR
                    log.crit('Someone Torpor\'d')
                    quit()
                elif hc_sup == hc_base:
                    # Deals AGG Damage
                    cursor.execute('UPDATE health SET healthAGG=?', ((str(int(hc_agg + 1))),))  # ! Parentheses are NOT redundant
                else:
                    # Deals SUP Damage
                    cursor.execute('UPDATE health SET healthSUP=?', ((str(int(hc_sup + 1))),))  # ! Parentheses are NOT redundant

                damage_amount -= 1
                db.commit()

        response_page, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Take Aggravated Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=1)
    async def hp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        character_name: str = await vU.getCharacterName(interaction)
        damage_amount: int = int(select.values[0])

        with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            hc_base: int = int(cursor.execute('SELECT healthBase from health').fetchone()[0])

            while damage_amount > 0:
                hc_agg: int = int(cursor.execute('SELECT healthAGG from health').fetchone()[0])

                if hc_base == hc_agg:
                    # Set up torpor logic later
                    # ! ENTER TORPOR
                    log.crit('Someone Torpor\'d')
                    quit()

                # Deals AGG Damage
                cursor.execute('UPDATE health SET healthAGG=?', ((str(int(hc_agg + 1))),))  # ! Parentheses are NOT redundant

                damage_amount -= 1
                db.commit()

        response_page, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Take Superficial Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=2)
    async def hp_sup_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        character_name: str = await vU.getCharacterName(interaction)
        damage_amount: int = int(select.values[0])

        with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            wpc_base: int = int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0])

            while damage_amount > 0:
                wpc_sup: int = int(cursor.execute('SELECT willpowerSUP from willpower').fetchone()[0])
                wpc_agg: int = int(cursor.execute('SELECT willpowerAGG from willpower').fetchone()[0])

                if wpc_sup == wpc_base:
                    # Deals AGG Damage
                    cursor.execute('UPDATE willpower SET willpowerAGG=?', ((str(int(wpc_agg + 1))),))  # ! Parentheses are NOT redundant
                else:
                    # Deals SUP Damage
                    cursor.execute('UPDATE willpower SET willpowerSUP=?', ((str(int(wpc_sup + 1))),))  # ! Parentheses are NOT redundant

                damage_amount -= 1
                db.commit()

        response_page, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))

    @discord.ui.select(placeholder='Take Aggravated Damage', options=health_or_willpower_options, max_values=1, min_values=1, row=3)
    async def hp_agg_dmg_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        character_name: str = await vU.getCharacterName(interaction)
        damage_amount: int = int(select.values[0])

        with sqlite3.connect(f'cogs//vampire//vtb_characters//{str(interaction.user.id)}//{character_name}//{character_name}.sqlite') as db:
            cursor = db.cursor()
            wpc_base: int = int(cursor.execute('SELECT willpowerBase from willpower').fetchone()[0])

            while damage_amount > 0:
                wpc_agg: int = int(cursor.execute('SELECT willpowerAGG from willpower').fetchone()[0])

                if wpc_agg > wpc_base:
                    return

                # Deals AGG Damage
                cursor.execute('UPDATE willpower SET willpowerAGG=?', ((str(int(wpc_agg + 1))),))  # ! Parentheses are NOT redundant

                damage_amount -= 1
                db.commit()

        response_page, response_view = await vPS.pageEVNav(interaction, 'tracker.hp/wp')
        await interaction.response.edit_message(embed=response_page, view=response_view(self.CLIENT))


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
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Remorse', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def remorse_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))

    @discord.ui.button(label='Path Rules', emoji='<:ExodusE:1145153679155007600>', style=discord.ButtonStyle.gray, row=1)
    async def path_rules_button_callback(self, interaction, button):
        response_embed, response_view = await vPS.pageEVNav(interaction, 'tracker.home')
        await interaction.response.edit_message(embed=response_embed, view=response_view(self.CLIENT))
