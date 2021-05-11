import datetime
import csv

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, MessageHandler, Filters, \
    CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.utils.request import Request

from test import getRow
from ugc.models import Profile, Message, Deposit

CALLBACK_BUTTON1_ID = 'callback_button1_id'
CALLBACK_BUTTON2_CREDIT = 'callback_button2_credit'
CALLBACK_BUTTON3_DEPOSIT = 'callback_button3_deposit'
CALLBACK_BUTTON4_CASH = 'callback_button5_cash'
CALLBACK_BUTTON5_PRODUCT = 'callback_button5_product'
CALLBACK_BUTTON6_BACK = 'callback_button6_BACK'

ID = False

TITLES = {
    CALLBACK_BUTTON1_ID: "ID",
    CALLBACK_BUTTON2_CREDIT: "Оформить кредит",
    CALLBACK_BUTTON3_DEPOSIT: "Открыть депозит",
    CALLBACK_BUTTON4_CASH: "Кредит наличными",
    CALLBACK_BUTTON5_PRODUCT: "Кредит на покупку",
    CALLBACK_BUTTON6_BACK: "Назад"
}


def get_base_inline_keyboard():
    keyword = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_ID], callback_data=CALLBACK_BUTTON1_ID),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_CREDIT], callback_data=CALLBACK_BUTTON2_CREDIT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_DEPOSIT], callback_data=CALLBACK_BUTTON3_DEPOSIT),
        ]
    ]

    return InlineKeyboardMarkup(keyword)


def get_base_inline_keyboard2():
    keyword = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_CASH], callback_data=CALLBACK_BUTTON4_CASH),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_PRODUCT], callback_data=CALLBACK_BUTTON5_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_BACK], callback_data=CALLBACK_BUTTON6_BACK),
        ]

    ]

    return InlineKeyboardMarkup(keyword)


def get_back_inline_keyboard():
    keyword = [
        [InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_BACK], callback_data=CALLBACK_BUTTON6_BACK)],
    ]

    return InlineKeyboardMarkup(keyword)


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    chat_id = query.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': query.message.from_user.username
        }
    )

    if query.data == CALLBACK_BUTTON1_ID:
        p.button_value = query.data
        p.save()
        query.edit_message_text(text='Напишите ID')

    elif query.data == CALLBACK_BUTTON3_DEPOSIT:
        p.button_value = query.data
        p.save()

        d, _ = Deposit.objects.get_or_create(
            profile=p,
        )
        d.delete()

        query.edit_message_text(text='Cумма депозита. ТГ')
        query.edit_message_reply_markup(reply_markup=get_back_inline_keyboard())

    elif query.data == CALLBACK_BUTTON2_CREDIT:
        d, _ = Deposit.objects.get_or_create(
            profile=p,
        )
        d.delete()
        query.edit_message_text(text="Выберите")
        query.edit_message_reply_markup(reply_markup=get_base_inline_keyboard2())

    elif query.data == CALLBACK_BUTTON6_BACK:
        query.edit_message_text(text="Выберите")
        query.edit_message_reply_markup(reply_markup=get_base_inline_keyboard())

    else:
        query.edit_message_text(text=f"Кредит оформлен!!!")
        query.edit_message_reply_markup(reply_markup=get_base_inline_keyboard())


def start(update: Update, _: CallbackContext) -> None:
    reply_markup = get_base_inline_keyboard()

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username
        }
    )

    if p.button_value:
        if p.button_value == CALLBACK_BUTTON1_ID:
            # print(type(text))
            p.button_value = ''
            p.save()

            reply_text = getRow(text)
            update.message.reply_text(
                text=reply_text,
                reply_markup=get_base_inline_keyboard()
            )

        elif p.button_value == CALLBACK_BUTTON3_DEPOSIT:
            d, _ = Deposit.objects.get_or_create(
                profile=p,
            )

            if not d.sum:
                d.sum = text
                d.save()
                reply_text = 'Напишите срок депозита. Год'

                update.message.reply_text(
                    text=reply_text,
                    reply_markup=get_back_inline_keyboard()
                )

            elif not d.deadline:
                d.deadline = text
                d.save()
                reply_text = 'Напишите ежемесячную оплату. ТГ'

                update.message.reply_text(
                    text=reply_text,
                    reply_markup=get_base_inline_keyboard()
                )

            elif not d.emonth:
                d.emonth = text
                d.save()
                reply_text = f'Депозит успешно открыт: \n Сумма: {d.sum} тг, \n Срок: {d.deadline} год, \n ' \
                             f'Ежемесячная Оплата: {d.emonth} тг '
                p.button_value = ''
                p.save()

                update.message.reply_text(
                    text=reply_text,
                    reply_markup=get_base_inline_keyboard()
                )


    else:
        reply_text = 'Выберите'
        update.message.reply_text(
            text=reply_text,
            reply_markup=get_base_inline_keyboard()
        )


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username
        }
    )

    count = Message.objects.filter(profile=p).count()

    update.message.reply_text(
        text=f'У вас {count} сообщении',
    )


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=500.0
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN
        )

        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        message_handler = MessageHandler(Filters.text, do_echo)
        # message_handler2 = CommandHandler('count', do_count)
        # buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler,
        #                                        pass_chat_data=True)
        #
        updater.dispatcher.add_handler(message_handler)
        # updater.dispatcher.add_handler(message_handler2)
        # updater.dispatcher.add_handler(buttons_handler)

        updater.start_polling()
        updater.idle()
