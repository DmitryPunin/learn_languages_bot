import aiogram
import asyncio
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery, InlineKeyboardButton
from aiogram import html
from aiogram.utils.formatting import Text, Bold, Italic, TextLink
from datetime import datetime, timedelta, timezone
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import requests
from LanguageManager import LanguageManager
from LanguagePair import LanguagePair
from Vocab import Vocab
import conf
token = conf.token
bot = aiogram.Bot(token)
dp = aiogram.Dispatcher()

Ln = LanguageManager()
Ln.load_languages()

user_language_pair = {}
user_language_data = {}
user_language_themes = {}
user_vocab = {}
user_language = {}
class states(StatesGroup):
    training = State()
async def language_prompt(message:Message):
    id = message.from_user.id
    if id in user_language:
        return True
    else:
        buttons = []
        for code, lang in Ln.get_available_user_langs():
            buttons.append([InlineKeyboardButton(text=lang, callback_data=f'choose_user_lang_{code}')])
        m = InlineKeyboardMarkup(inline_keyboard=buttons, one_time_keyboard=True, resize_keyboard=True)

        await bot.send_message(message.chat.id,'Выберите ваш язык/Choose your language',reply_markup=m)
        return False



@dp.message(Command('start'))
async def start(message:Message):
    if not await language_prompt(message):
        return
    btn_choose_option = InlineKeyboardButton(text=await get_text(message,'choose_lang'), callback_data='choose_lang')
    kb = InlineKeyboardMarkup(resize_keyboard=True, inline_keyboard=[[btn_choose_option]])
    await bot.send_message(message.chat.id,await get_text(message,'welcome'),reply_markup=kb)
async def get_text(message,text):
    return Ln.get_text(user_language[message.from_user.id],text)

@dp.callback_query()
async def choose_pair(call:CallbackQuery):
    if call.data == 'choose_lang':
        buttons = []
        for l in Ln.get_available_langs(Ln.get_user_lang(user_language[call.from_user.id])):
            buttons.append([InlineKeyboardButton(text=l, callback_data=f'choose_pair_{l}')])
        m = InlineKeyboardMarkup(inline_keyboard=buttons,one_time_keyboard=True, resize_keyboard=True)
        await bot.send_message(call.message.chat.id,await get_text(call,'choose_lang'),reply_markup=m)
    elif call.data.startswith('choose_pair'):
        lang = call.data.split('_')[2]
        buttons = []
        for from_lang, to_lang, code in Ln.filter(lang,Ln.get_user_lang(user_language[call.from_user.id])):
            buttons.append([InlineKeyboardButton(text='-'.join((from_lang,to_lang)),callback_data=code)])
        m = InlineKeyboardMarkup(inline_keyboard=buttons,one_time_keyboard=True, resize_keyboard=True)
        await bot.send_message(call.message.chat.id,await get_text(call,'choose_pair'),reply_markup=m)
    elif call.data.startswith('choose_user_lang_'):
        lang = call.data.split('_')[3]
        user_language[call.from_user.id] = lang
        await bot.send_message(call.message.chat.id,f'Вы успешно выбрали {lang} язык ')

    elif call.data in Ln.code_to_pair:
        pair = Ln.code_to_pair[call.data]
        user_language_pair[call.from_user.id] = pair

        btn1 = InlineKeyboardButton(text=await get_text(call,'sentences'), callback_data='sentences')
        btn2 = InlineKeyboardButton(text=await get_text(call,'words'), callback_data='vocab')
        m = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]], one_time_keyboard=True, resize_keyboard=True)
        await bot.send_message(call.message.chat.id, await get_text(call,'choose_vocab'), reply_markup=m)
    elif call.data in ['vocab', 'sentences']:
        user_language_data[call.from_user.id] = call.data
        pair = user_language_pair[call.from_user.id]
        v:Vocab = getattr(pair,call.data)
        user_vocab[call.from_user.id] = v
        buttons = []
        for t in v.themes:
            buttons.append([InlineKeyboardButton(text=t,callback_data=t)])

        markup = InlineKeyboardMarkup(inline_keyboard=buttons,
                                        one_time_keyboard=True, resize_keyboard=True)
        await bot.send_message(call.message.chat.id, await get_text(call,'choose_theme'),
                                reply_markup=markup)
    elif call.data in user_vocab[call.from_user.id].themes:
        user_language_themes[call.from_user.id] = call.data
        await bot.send_message(call.message.chat.id,await get_text(call,'setup_ready'))

    await call.answer()
@dp.message(Command('train'))
async def train(message: Message, state:FSMContext):
    if ((message.from_user.id not in user_language_themes) or
        (message.from_user.id not in user_vocab)):
        await bot.send_message(message.chat.id,await get_text(message,'data_error'))
        return
    theme = user_language_themes[message.from_user.id]
    vocab:Vocab = user_vocab[message.from_user.id]
    translation_pair = vocab.random_pair(theme)
    await bot.send_message(message.chat.id,f'{await get_text(message,'translate_text')}\n{translation_pair[0]}')
    await state.update_data(translation_pair=translation_pair)
    await state.set_state(states.training)
@dp.message(states.training)
async def training(message: Message, state:FSMContext):
    theme = user_language_themes[message.from_user.id]
    vocab: Vocab = user_vocab[message.from_user.id]
    translation_pair = await state.get_value('translation_pair')

    if vocab.check(theme,translation_pair[0],message.text):
        await bot.send_message(message.chat.id,await get_text(message,'right_answer'))
        new_translation_pair = vocab.random_pair(theme)

        await bot.send_message(message.chat.id,f'{await get_text(message,'translate_text')}\n{new_translation_pair[0]}')
        await state.update_data(translation_pair=new_translation_pair)
        await state.update_data(mistake=None)
        await state.update_data(variants=None)
    else:
        mistake = await state.get_value('mistake')
        if mistake is None:
            await state.update_data(mistake=True)
            variants = vocab.generate_variants(theme,3,translation_pair[1])
            await state.update_data(variants=variants)
        else:
            variants = await state.get_value('variants')
        await bot.send_message(message.chat.id, f'{await get_text(message,'wrong_answer')}\n{await get_text(message,'variants')}\n{'\n'.join(variants)}')







    















asyncio.run(dp.start_polling(bot))