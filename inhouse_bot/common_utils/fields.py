from discord.ext import commands
from discord.ext.commands import ConversionError
from sqlalchemy import Enum
import rapidfuzz
import lol_id_tools

roles_list = ["TOP X", "JGL X", "MID X", "BOT X", "SUP X", "TOP Z", "JGL Z", "MID Z", "BOT Z", "SUP Z"]
role_enum = Enum(*roles_list, name="role_enum")

side_enum = Enum("BLUE", "RED", name="team_enum")

foreignkey_cascade_options = {"onupdate": "CASCADE", "ondelete": "CASCADE"}

# This is a dict used for fuzzy matching
full_roles_dict = {
    "top X": "TOP X",
    "jgl X": "JGL X",
    "jungle X": "JGL X",
    "jungler X": "JGL X",
    "mid X": "MID X",
    "bot X": "BOT X",
    "adc X": "BOT X",
    "sup X": "SUP X",
    "supp X": "SUP X",
    "support X": "SUP X",
    "top Z": "TOP Z",
    "jgl Z": "JGL Z",
    "jungle Z": "JGL Z",
    "jungler Z": "JGL Z",
    "mid Z": "MID Z",
    "bot Z": "BOT Z",
    "adc Z": "BOT Z",
    "sup Z": "SUP Z",
    "supp Z": "SUP Z",
    "support Z": "SUP Z",
}


class RoleConverter(commands.Converter):
    async def convert(self, ctx, argument):
        """
        Converts an input string to a clean role
        """
        matched_string, ratio = rapidfuzz.process.extractOne(argument, full_roles_dict.keys())

        if ratio < 85:
            await ctx.send(f"The role was not understood")
            raise ConversionError

        else:
            return full_roles_dict[matched_string]


class ChampionNameConverter(commands.Converter):
    async def convert(self, ctx, argument):
        """
        Converts an input string to a clean champion ID
        """
        try:
            return lol_id_tools.get_id(argument, input_locale="en_US", object_type="champion")

        except lol_id_tools.NoMatchingNameFound:
            await ctx.send(f"The champion name was not understood")
            raise ConversionError
