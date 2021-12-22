from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from sqlalchemy.sql.functions import user


answer_questions_button = InlineKeyboardButton(
    "Ответить на вопросы", callback_data="answer_questions"
)
answer_questions_keyboard = InlineKeyboardMarkup()
answer_questions_keyboard.add(answer_questions_button)

accept_onboarding_request_button = InlineKeyboardButton(
    "Хочу", callback_data="accept_onboarding_request"
)
cancel_onboarding_request_button = InlineKeyboardButton(
    "Пропустить", callback_data="dicline_onboarding_request"
)
onboarding_request_keyboard = InlineKeyboardMarkup()
onboarding_request_keyboard.add(
    accept_onboarding_request_button, cancel_onboarding_request_button
)

first_onboarding_step_keyboard = InlineKeyboardMarkup()
first_onboarding_step_button = InlineKeyboardButton(
    ">", callback_data="next_onboarding_step"
)
first_onboarding_step_keyboard.add(first_onboarding_step_button)

next_onboarding_step_button = InlineKeyboardButton(
    "<", callback_data="prev_onboarding_step"
)
prev_onboarding_step_button = InlineKeyboardButton(
    ">", callback_data="next_onboarding_step"
)
next_prev_onboarding_keyboard = InlineKeyboardMarkup()
next_prev_onboarding_keyboard.add(
    next_onboarding_step_button, prev_onboarding_step_button
)


cards_game_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
next_card_button = KeyboardButton("Следующее слово")
exit_card_game_button = KeyboardButton("Выйти из игры")
cards_game_keyboard.add(next_card_button, exit_card_game_button)

empty_keyboard = ReplyKeyboardRemove()
