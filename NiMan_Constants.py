import NiMan_Helper as helper

global Token
Token = 'OUTDATED_ODI0MzM3MjU4MjQwOTMzOTI5.YFt55Q.8ReNKiJsR2gWt-qPv-QdC-br8HM'

global symbol
symbol = '='

global AppId
AppId = 824337258240933929

global GuildId
GuildId = 671891373682589706

global tenor_key
tenor_key = '1W04JDY0JEQD'
global tenor_limit
tenor_limit = 1

global script_greeting
script_greeting = 'discord_NiMan_NiGreeting.py'

global message_help
message_help = [
                '- say anything with \"ni\" < 250 chars long',
                '- say !n or !N for a surprise!',
                '- use !j [type] for a joke, type can be empty or one of \"misc\", \"programming\", \"dark\", \"pun\", \t\"spooky\", or \"christmas\".',
                '- use !q for inspirational quote.',
                '- use !rs for Ron Swanson quote.',
                '- use !cn for a Chuck Norris quote.'
                ]

chan_bot_tester = 'bot-tester'
chan_general = 'general'
global channels
channels = [
        chan_general,
        chan_bot_tester
        ]

# Users
user_Striker1521_0430 = 'Striker1521#0430'
user_conyay_4754 = 'conyay#4754'
user_TonyStark1414_8839 = 'TonyStark1414#8839'
user_Travis_9127 = 'Travis#9127'
user_Wadewatts77_7340 = 'Wadewatts77#7340'
user_Electabuzz57_8983 = 'Electabuzz57#8983'
user_rt_mahony18_0357 = 'rt_mahony18#0357'
user_NHL_99_0158 = 'NHL_99#0158'
user_QvidNovi_1391 = 'QvidNovi#1391'
users = [
        helper.get_name(user_Striker1521_0430),
        helper.get_name(user_conyay_4754),
        helper.get_name(user_TonyStark1414_8839),
        helper.get_name(user_Travis_9127),
        helper.get_name(user_Wadewatts77_7340),
        helper.get_name(user_Electabuzz57_8983),
        helper.get_name(user_rt_mahony18_0357),
        helper.get_name(user_NHL_99_0158),
        helper.get_name(user_QvidNovi_1391)
        ]

bot_ProRepeater_8180 = 'ProRepeater#8180'
bot_Impersonator_6724 = 'Impersonator#6724'
bot_Rythm_3722 = 'Rythm#3722'
bot_PokeMeow_6691 = 'PokéMeow#6691'
bots =  [
        helper.get_name(bot_ProRepeater_8180),
        helper.get_name(bot_Impersonator_6724),
        helper.get_name(bot_Rythm_3722),
        helper.get_name(bot_PokeMeow_6691)
        ]

ignore_list =   [
                helper.get_name(bot_ProRepeater_8180),
                helper.get_name(bot_Impersonator_6724),
                helper.get_name(bot_Rythm_3722),
                helper.get_name(bot_PokeMeow_6691)
                ]

admin_list =    [
                helper.get_name(user_Striker1521_0430)
                ]

# Preparing the cogs
initial_extensions = [
    'airhorn',
    'basics',
    'fun'
]
