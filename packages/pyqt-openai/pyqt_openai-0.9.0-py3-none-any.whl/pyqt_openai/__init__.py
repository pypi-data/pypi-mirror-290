"""
This file is used to store the constants and the global variables that are used throughout the application.
"""

import json
import os
from pathlib import Path

import toml

# Load the pyproject.toml file
SRC_DIR = Path(__file__).resolve().parent
ROOT_DIR = SRC_DIR.parent
SETUP_FILENAME = ROOT_DIR / "pyproject.toml"

with open(SETUP_FILENAME, "r") as file:
    pyproject_data = toml.load(file)

# For the sake of following the PEP8 standard, we will declare module-level dunder names.
# PEP8 standard about dunder names: https://peps.python.org/pep-0008/#module-level-dunder-names

__version__ = pyproject_data["project"]["version"]
__author__ = pyproject_data["project"]["authors"][0]['name']

# Constants
# ----------------------------
# APP
APP_NAME = pyproject_data["project"]["name"]
CONTACT = pyproject_data["project"]["authors"][0]['email']
APP_ICON = 'icon.ico'
APP_INITIAL_WINDOW_SIZE = (1280, 768)

TRANSPARENT_RANGE = 20, 100
TRANSPARENT_INIT_VAL = 100

LICENSE = pyproject_data["project"]["license"]['text']
LICENSE_URL = 'https://github.com/yjg30737/pyqt-openai/blob/main/LICENSE'
PAYPAL_URL = 'https://paypal.me/yjg30737'
BUYMEACOFFEE_URL = 'https://www.buymeacoffee.com/yjg30737'
GITHUB_URL = 'https://github.com/yjg30737/pyqt-openai'
DISCORD_URL = 'https://discord.gg/cHekprskVE'
COLUMN_TO_EXCLUDE_FROM_SHOW_HIDE_CHAT = ['id']
COLUMN_TO_EXCLUDE_FROM_SHOW_HIDE_IMAGE = ['id', 'data']
DEFAULT_LANGUAGE = 'en_US'
LANGUAGE_FILE = 'translations.json'
LANGUAGE_DICT = {
    "English": "en_US",
    "Spanish": "es_ES",
    "Chinese": "zh_CN",
    "Russian": "ru_RU",
    "Korean": "ko_KR",
    "French": "fr_FR",
    "German": "de_DE",
    "Italian": "it_IT",
    "Hindi": "hi_IN",
    "Arabic": "ar_AE",
    "Japanese": "ja_JP",
    "Bengali": "bn_IN",
    "Urdu": "ur_PK",
    "Indonesian": "id_ID",
    "Portuguese": "pt_BR"
}

MESSAGE_ADDITIONAL_HEIGHT = 40
MESSAGE_PADDING = 16
MESSAGE_MAXIMUM_HEIGHT = 800
MAXIMUM_MESSAGES_IN_PARAMETER = 20
MESSAGE_MAXIMUM_HEIGHT_RANGE = 300, 1000
MAXIMUM_MESSAGES_IN_PARAMETER_RANGE = 2, 1000

PROMPT_IMAGE_SCALE = 200, 200
TOAST_DURATION = 3

## PARAMETER - OPENAI CHAT
OPENAI_TEMPERATURE_RANGE = 0, 2
OPENAI_TEMPERATURE_STEP = 0.01

MAX_TOKENS_RANGE = 512, 128000

TOP_P_RANGE = 0, 1
TOP_P_STEP = 0.01

FREQUENCY_PENALTY_RANGE = 0, 2
FREQUENCY_PENALTY_STEP = 0.01

PRESENCE_PENALTY_RANGE = 0, 2
PRESENCE_PENALTY_STEP = 0.01

## ICONS
ICON_ADD = 'ico/add.svg'
ICON_CASE = 'ico/case.svg'
ICON_CLOSE = 'ico/close.svg'
ICON_COPY = 'ico/copy.svg'
ICON_CUSTOMIZE = 'ico/customize.svg'
ICON_DELETE = 'ico/delete.svg'
ICON_DISCORD = 'ico/discord.svg'
ICON_EXPORT = 'ico/export.svg'
ICON_FAVORITE_NO = 'ico/favorite_no.svg'
ICON_FAVORITE_YES = 'ico/favorite_yes.svg'
ICON_FULLSCREEN = 'ico/fullscreen.svg'
ICON_GITHUB = 'ico/github.svg'
ICON_HELP = 'ico/help.svg'
ICON_HISTORY = 'ico/history.svg'
ICON_IMPORT = 'ico/import.svg'
ICON_INFO = 'ico/info.svg'
ICON_NEXT = 'ico/next.svg'
ICON_OPENAI = 'ico/openai.png'
ICON_PREV = 'ico/prev.svg'
ICON_PROMPT = 'ico/prompt.svg'
ICON_QUESTION = 'ico/question.svg'
ICON_REFRESH = 'ico/refresh.svg'
ICON_REGEX = 'ico/regex.svg'
ICON_SAVE = 'ico/save.svg'
ICON_SEARCH = 'ico/search.svg'
ICON_SETTING = 'ico/setting.svg'
ICON_SIDEBAR = 'ico/sidebar.svg'
ICON_STACKONTOP = 'ico/stackontop.svg'
ICON_USER = 'ico/user.png'
ICON_VERTICAL_THREE_DOTS = 'ico/vertical_three_dots.svg'
ICON_WORD = 'ico/word.svg'
ICON_SEND = 'ico/send.svg'

## CUSTOMIZE
DEFAULT_ICON_SIZE = (24, 24)
DEFAULT_USER_IMAGE_PATH = ICON_USER
DEFAULT_AI_IMAGE_PATH = ICON_OPENAI
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT_FAMILY = 'Arial'

DEFAULT_BUTTON_HOVER_COLOR = '#A2D0DD'
DEFAULT_BUTTON_PRESSED_COLOR = '#B3E0FF'
DEFAULT_BUTTON_CHECKED_COLOR = '#B3E0FF'
DEFAULT_SOURCE_HIGHLIGHT_COLOR = '#CCB500'
DEFAULT_SOURCE_ERROR_COLOR = '#FF0000'
DEFAULT_FOUND_TEXT_COLOR = '#00A2E8'
DEFAULT_FOUND_TEXT_BG_COLOR = '#FFF200'

## SHORTCUT
DEFAULT_SHORTCUT_GENERAL_ACTION = 'Enter'
DEFAULT_SHORTCUT_FIND_PREV = 'Ctrl+Shift+D'
DEFAULT_SHORTCUT_FIND_NEXT = 'Ctrl+D'
DEFAULT_SHORTCUT_FIND_CLOSE = 'Escape'
DEFAULT_SHORTCUT_PROMPT_BEGINNING = 'Ctrl+B'
DEFAULT_SHORTCUT_PROMPT_ENDING = 'Ctrl+E'
DEFAULT_SHORTCUT_SUPPORT_PROMPT_COMMAND = 'Ctrl+Shift+P'
DEFAULT_SHORTCUT_FULL_SCREEN = 'F11'
DEFAULT_SHORTCUT_FIND = 'Ctrl+F'
DEFAULT_SHORTCUT_JSON_MODE = 'Ctrl+J'
DEFAULT_SHORTCUT_LEFT_SIDEBAR_WINDOW = 'Ctrl+L'
DEFAULT_SHORTCUT_RIGHT_SIDEBAR_WINDOW = 'Ctrl+R'
DEFAULT_SHORTCUT_CONTROL_PROMPT_WINDOW = 'Ctrl+Shift+C'
DEFAULT_SHORTCUT_SETTING = 'Ctrl+Alt+S'
DEFAULT_SHORTCUT_SEND = 'Ctrl+Enter'

## DIRECTORY PATH & FILE'S NAME
MAIN_INDEX = 'main.py'
IMAGE_DEFAULT_SAVE_DIRECTORY = 'image_result'
LLAMA_INDEX_DEFAULT_READ_DIRECTORY = './example'
INI_FILE_NAME = 'pyqt_openai.ini'
DB_FILE_NAME = 'conv'
FILE_NAME_LENGTH = 32
QFILEDIALOG_DEFAULT_DIRECTORY = os.path.expanduser('~')

## EXTENSIONS
TEXT_FILE_EXT_LIST = ['.txt']
IMAGE_FILE_EXT_LIST = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
IMAGE_FILE_EXT_LIST_STR = 'Image File (*.png *.jpg *.jpeg *.gif *.bmp)'
TEXT_FILE_EXT_LIST_STR = 'Text File (*.txt)'
JSON_FILE_EXT_LIST_STR = 'JSON File (*.json)'
READ_FILE_EXT_LIST_STR = f'{TEXT_FILE_EXT_LIST_STR};;{IMAGE_FILE_EXT_LIST_STR}'

## IMAGE
IMAGE_CHATGPT_IMPORT_MANUAL = 'images/import_from_chatgpt.png'

## PROMPT
PROMPT_BEGINNING_KEY_NAME = 'prompt_beginning'
PROMPT_JSON_KEY_NAME = 'prompt_json'
PROMPT_MAIN_KEY_NAME = 'prompt_main'
PROMPT_END_KEY_NAME = 'prompt_ending'
PROMPT_NAME_REGEX = '^[a-zA-Z_0-9]+$'
INDENT_SIZE = 4

# DB
DB_NAME_REGEX = '[a-zA-Z0-9]{1,20}'

THREAD_TABLE_NAME_OLD = 'conv_tb'
THREAD_TRIGGER_NAME_OLD = 'conv_tr'
MESSAGE_TABLE_NAME_OLD = 'conv_unit_tb'

THREAD_TABLE_NAME = 'thread_tb'
THREAD_TRIGGER_NAME = 'thread_tr'
MESSAGE_TABLE_NAME = 'message_tb'

IMAGE_TABLE_NAME = 'image_tb'

THREAD_MESSAGE_INSERTED_TR_NAME_OLD = 'conv_tb_updated_by_unit_inserted_tr'
THREAD_MESSAGE_UPDATED_TR_NAME_OLD = 'conv_tb_updated_by_unit_updated_tr'
THREAD_MESSAGE_DELETED_TR_NAME_OLD = 'conv_tb_updated_by_unit_deleted_tr'

THREAD_MESSAGE_INSERTED_TR_NAME = 'thread_message_inserted_tr'
THREAD_MESSAGE_UPDATED_TR_NAME = 'thread_message_updated_tr'
THREAD_MESSAGE_DELETED_TR_NAME = 'thread_message_deleted_tr'

THREAD_ORDERBY = 'update_dt'

PROPERTY_PROMPT_GROUP_TABLE_NAME_OLD = 'prop_prompt_grp_tb'
PROPERTY_PROMPT_UNIT_TABLE_NAME_OLD = 'prop_prompt_unit_tb'
TEMPLATE_PROMPT_GROUP_TABLE_NAME_OLD = 'template_prompt_grp_tb'
TEMPLATE_PROMPT_TABLE_NAME_OLD = 'template_prompt_tb'
PROPERTY_PROMPT_UNIT_DEFAULT_VALUE = [{'name': 'Task', 'content': ''},
                                      {'name': 'Topic', 'content': ''},
                                      {'name': 'Style', 'content': ''},
                                      {'name': 'Tone', 'content': ''},
                                      {'name': 'Audience', 'content': ''},
                                      {'name': 'Length', 'content': ''},
                                      {'name': 'Form', 'content': ''}]

PROMPT_GROUP_TABLE_NAME = 'prompt_group_tb'
PROMPT_ENTRY_TABLE_NAME = 'prompt_entry_tb'

# DEFAULT JSON FILENAME FOR PROMPT
AWESOME_CHATGPT_PROMPTS_FILENAME = 'prompt_res/awesome_chatgpt_prompts.json'
ALEX_BROGAN_PROMPT_FILENAME = 'prompt_res/alex_brogan.json'

FORM_PROMPT_GROUP_SAMPLE = json.dumps([
    {
        "name": 'Default',
        "data": PROPERTY_PROMPT_UNIT_DEFAULT_VALUE
    }
], indent=INDENT_SIZE)

SENTENCE_PROMPT_GROUP_SAMPLE = '''[
    {
        "name": "alex_brogan",
        "data": [
            {
                "name": "sample_1",
                "content": "Identify the 20% of [topic or skill] that will yield 80% of the desired results and provide a focused learning plan to master it."
            },
            {
                "name": "sample_2",
                "content": "Explain [topic or skill] in the simplest terms possible as if teaching it to a complete beginner. Identify gaps in my understanding and suggest resources to fill them."
            }
        ]
    },
    {
        "name": "awesome_chatGPT_prompts",
        "data": [
            {
                "name": "linux_terminal",
                "content": "I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so. when i need to tell you something in english, i will do so by putting text inside curly brackets {like this}. my first command is pwd"
            },
            {
                "name": "english_translator_and_improver",
                "content": "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. My first sentence is \"istanbulu cok seviyom burada olmak cok guzel\""
            },
        ]
    }
]'''

# Load the default prompt
if os.path.exists(AWESOME_CHATGPT_PROMPTS_FILENAME):
    AWESOME_CHATGPT_PROMPTS = json.load(open(AWESOME_CHATGPT_PROMPTS_FILENAME))[0]
if os.path.exists(ALEX_BROGAN_PROMPT_FILENAME):
    ALEX_BROGAN_PROMPT = json.load(open(ALEX_BROGAN_PROMPT_FILENAME))[0]

# Update the __all__ list with the PEP8 standard dunder names
__all__ = ['__version__',
           '__author__']

# Update the __all__ list with the constants
__all__.extend([name for name, value in globals().items() if name.isupper()])
