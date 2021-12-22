#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import stat
from aiogram import Bot, types
from aiogram.types import message
from variables import *
from models import *
from sqlalchemy.ext.declarative import declarative_base
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.utils import executor
from aiogram.types import chat, message_entity, reply_keyboard, InputMediaPhoto
from aiogram.types.message import Message
from random import choice, shuffle, random
from scripts import *
from json import *
from keyboards import *
import asyncio
import os
import aiohttp
import time
import datetime
from config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker




states = {}


async def get_event_type(event):
    pass

async def get_user_state_from_inline_commands(message):
    print(message)
    if states.get(message["from"]["id"], False): 
        return states[message["from"]['id']]
    else: 
        MainStateUser = MainState(message)
        states[message["from"]["id"]] = MainStateUser
        return MainStateUser 

async def get_user_state_from_text_commands(message):
    if states.get(message["from"]["id"], False): 
        return states[message["from"]['id']]
    else: 
        MainStateUser = MainState(message)
        states[message["from"]["id"]] = MainStateUser
        return MainStateUser 


class OnboardingState: 
    def __init__(self, message, last_sended_message): 
        self.inline_commands = {"next_onboarding_step": self.set_next_onboarding_step, "prev_onboarding_step": self.set_prev_onboarding_step}
        self.onboarding_step = 1
        self.last_sended_message = last_sended_message


    async def inline_commands_handler(self, message): 
        if self.inline_commands.get(message["data"], False): 
            await self.inline_commands[message["data"]](message)
        else: 
            await message.answer("Произошла непредвиденная ошибка")


class TestState: 
    def __init__(self, sended_story_message, test_number): 
        self.sended_story_message = sended_story_message 
        self.test_number = test_number
        self.current_question = 0
        self.right_answers_count = 0 
        self.wrong_asnwers_count = 0
        self.inline_commands = {"next_btn": self.set_next_test_step}


    async def inline_commands_handler(self, message): 
        if self.inline_commands.get(message["data"], False): 
            await self.inline_commands[message["data"]](message)
        else: 
            await message.answer("Произошла непредвиденная ошибка")


    async def get_test_question(self, message): 
        with open("stories.json", "r", errors="ignore", encoding="utf-8") as file: 
            data = load(file)
        return data[self.test_number]["questions"]

    async def get_test_answers(self, message): 
        with open("stories.json", "r", errors="ignore", encoding="utf-8") as file: 
            data = load(file)
        return data[self.test_number]["answers"]

    async def send_test_step(self, message):
        if 0 <= self.current_question <= 4:
            questions = await self.get_test_question(message)
            question = questions[self.current_question]
            await bot.edit_message_text(
                question,
                chat_id=self.sended_story_message["chat"]["id"],
                message_id=self.sended_story_message["message_id"]
            )
            answers = await self.get_test_answers(message)
            answers = answers[self.current_question]
            answers = sorted(answers, key=lambda el: random())
            keyb = InlineKeyboardMarkup()
            for answer in answers: 
                thatOneAnswer = InlineKeyboardButton(str(answer), callback_data="next_btn")
                keyb.add(thatOneAnswer)
            await bot.edit_message_reply_markup(chat_id=self.sended_story_message["chat"]["id"], message_id=self.sended_story_message["message_id"], reply_markup=keyb)
        elif self.current_question == 5:
            photo = open('map_check.png', 'rb')
            await bot.send_photo(chat_id=self.sended_story_message["chat"]["id"], photo=photo)
            await bot.edit_message_text("✅ Собрано [1/5] карточек\n\nТы ответил правильно на 3 из 5 вопросов! Скорее иди искать следующую карточу!", chat_id=self.sended_story_message["chat"]["id"], message_id=self.sended_story_message["message_id"])


    async def set_next_test_step(self, message):
        if self.current_question < 5:
            self.current_question += 1
            await self.send_test_step(message)

    async def exit_test_state(message):
        MainStateUser = MainState(message)
        states[message["chat_id"]] = MainStateUser
        await bot.send_message(
            message["chat"]["id"],
            "✅ Отлично!\n\nМы рассказали тебе об всём, что знаем о боте, а если что-то пропустили — не беда! Всегда интереснее исследовать что-то самому, без посторонней помощи 😉"
        )


class MainState:
    def __init__(self, message):
        self.id = message["from"]["id"]
        self.username = message["from"]["username"]
        self.text_commands = {"/start": self.start}
        self.inline_commands = {"accept_onboarding_request": self.accept_onboarding_request, "dicline_onboarding_request": self.dicline_onboarding_request, "answer_questions": self.answer_questions}

    async def answer_questions(self, message):
        ts = TestState(self.sended_story_message, self.story_number)
        states[message["from"]["id"]] = ts
        await ts.send_test_step(message)

    async def start(self, message): 
        await message.answer("👋 Привет!\nEnergyQuest – это интерактивная квест-игра, в которой тебе нужно искать карточки внутри корпусов КГЭУ\n\nНайдя карточку, ты можешь прочитать интересные рассказы об энергетике в России, ответить на вопросы после рассказа и получить баллы от своего преподавателя в БРС!", )
        photo = open('map.png', 'rb')
        await bot.send_photo(chat_id=message["chat"]["id"], photo=photo)
        await asyncio.sleep(1)
        await self.send_onboarding_request(message)

    async def accept_onboarding_request(self, message): 
        OnboardingStateUser = OnboardingState(message, self.onboarding_request_message)
        states[message["from"]["id"]] = OnboardingStateUser
        await OnboardingStateUser.send_onboarding_step(message)

    async def dicline_onboarding_request(self, message): 
        await bot.delete_message(self.onboarding_request_message["chat"]["id"], self.onboarding_request_message["message_id"])
        await bot.send_message(
            message["from"]["id"],
            "😤 Хорошо, но если у тебя возникнут вопросы по работе с ботом, можешь пройти обучение по команде /help.",
        )
        mainStateUser = MainState(message)
        states[message["from"]["id"]] = mainStateUser

    async def send_story(self, message): 
        story_number = message["text"].split()[1]
        with open("stories.json", "r", encoding="utf-8", errors="ignore") as file: 
            data = json.load(file)
        self.story_number = story_number
        text = data[story_number]["text"]
        self.sended_story_message = await message.answer(text, reply_markup=answer_questions_keyboard)
        print(self.sended_story_message, "здесь")

    async def send_onboarding_request(self, message): 
        self.onboarding_request_message = await message.answer("Хочешь пройти обучение? Я объясню тебе как играть.", reply_markup=onboarding_request_keyboard)

    async def text_commands_handler(self, message):
        try:
            if len(message["text"].split()) == 1 and message["text"] == "/start": 
                await self.start(message)
            elif len(message["text"].split()) == 2 and  message["text"].split()[0] == "/start": 
                await self.send_story(message)
            else: 
                await self.text_commands[message["text"]](message)
        except KeyError as error:
            await message.answer(
                f"Команда не найдена, введи /exit, чтобы вернуться на начальный экран."
            )

    async def inline_commands_handler(self, message): 
        try:
            await self.inline_commands[message["data"]](message)
        except KeyError as error:
            await message.answer(
                f"Команда не найдена, введи /exit, чтобы вернуться на начальный экран."
            )

    @staticmethod
    async def check_answer(message):
        session = Session()
        customer = (
            session.query(Customer)
            .filter(Customer.id == message["message"]["from"]["id"])
            .first()
        )
        card = session.query(Card).filter(Card.id == Customer.current_word_id).first()
        if card:
            if card.correct_answer == message["data"].split("_")[2]:
                await message.answer(
                    f"😔 Правильно! {card.text} на татарском языке будет {card.correct_answer}"
                )
                await CardsGameState.send_card(message, is_first=False)
            else:
                await message.answer(f"😔 Неправильно, попробуй ещё раз!")




bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def text_commands_handler(message):
    print(states)
    user_state = await get_user_state_from_text_commands(message)
    await states[message["from"]["id"]].text_commands_handler(message)


@dp.callback_query_handler()
async def inline_commands_handler(message):
    print(states)
    user_state = await get_user_state_from_inline_commands(message)
    await states[message["from"]["id"]].inline_commands_handler(message)


@dp.message_handler(content_types=["contact"])
async def get_contact(message):
    user_state = await get_user_state_from_text_commands(message)
    await states[user_state].auth_with_phone(message)


onboarding_steps = {
    1: "Внутри КГЭУ мы оставили карточки в виде QR-кодов, отсканировав которые ты можешь перейти в Telegram - бот и получить",
    2: "*[1/3]* Первым делом стоит изучать теорию, за каждый пройденный шаг теории ты получаешь очки, которые потом обмениваются на достижения и бонусы! 1 шаг = 1 очко.\n\nКроме того, после прохождения некоторых шагов ты получишь возможность решить задания, верно решенное задание = 5 очков.",
    3: "*[2/3]* Теория уже надоела? Тогда сыграй в игры в одиночку или вместе с друзьями.\n\nЧтобы пригласить друга в игру, напиши в чат с другом @tatrikabot, выбери игру и начинай играть!",
    4: "*[3/3]* А что делать, если у меня возник вопрос по учебным материалам или играм?\n\nСмело задавай их своему наставнику через кнопку Задать вопрос!",
}


test_steps = {
    1: ["Электрические трансформаторы", "6 вопросов", "Уровень: легко", "Награда: маленький завод"], 
    2: ["Энергетические машины", "10 вопросов", "Уровень: средне", "Награда: средний завод"], 
    3: ["Энергоснабжение", "5 вопросов", "Уровень: средне", "Награда: большой завод"]
}

suitable_question_length = 140


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
