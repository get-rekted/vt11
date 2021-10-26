# в venv установить PyTelegramBotAPI, telegram, python-telegram-bot, pycoingecko, py-currency-converter


from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert

cg = CoinGeckoAPI()

# Переменные
view = "Crypto 📈"
usd = 'USD to 📊'
faq = 'FAQ 📌'
feedback = 'Feedback 🔥'

# Кнопка просмотра курса криптовалют
def button_view_handler(update: Update, context: CallbackContext):
    price = cg.get_price(ids='bitcoin,litecoin,ethereum,terra-luna, solana, ripple, polkadot, dogecoin, chainlink', vs_currencies='usd')
    update.message.reply_text(
        text=f"Bitcoin (BTC) — {price['bitcoin']['usd']:.2f}$"
        + f"\nLitecoin (LTC) — {price['litecoin']['usd']:.2f}$"
        + f"\nEthereum (ETH) — {price['ethereum']['usd']:.2f}$"
        + f"\nTerra (LUNA) — {price['terra-luna']['usd']:.2f}$"
        + f"\nSolana (SOL) — {price['solana']['usd']:.2f}$"
        + f"\nXRP (XRP) — {price['ripple']['usd']:.2f}$"
        + f"\nPolkadot (DOT) — {price['polkadot']['usd']:.2f}$"
        + f"\nDogecoin (DOGE) — {price['dogecoin']['usd']:.2f}$"
        + f"\nChainlink (LINK) — {price['chainlink']['usd']:.2f}$"
        )

# Кнопка FAQ
def button_faq_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
    text='Ответы на вопросы:\n\n 1) С какого сайта бот берет цены? - С сайта CoinGecko.\n\n 2) Почему CoinGecko? - '
         'Ежеминутное обновление курса монет и наличие API.\n\n 3) Как пришла идея о создании данного бота? - '
         'Спонтанно. '
    )

# Кнопка Feedback
def button_feedback_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
    text='Создатель бота - Арутюнян А. Д.\n\n VK - https://vk.com/arutyunyan__777\n\n TG - @durov'
    )

# Кнопка просмотра курса доллара
def button_usd_handler(update: Update, context: CallbackContext):
    course = convert(amount=1, to=['RUB', 'EUR', 'UAH'])
    update.message.reply_text(
        text=f"1 USD = {course['RUB']} RUB"
        + f"\n1 USD = {course['EUR']} EUR"
        + f"\n1 USD = {course['UAH']} UAH"
    )

# Ответ юзеру после /start
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == view:
        return button_view_handler(update=update, context=context)
    elif text == usd:
        return button_usd_handler(update=update, context=context)
    elif text == faq:
        return button_faq_handler(update=update, context=context)
    elif text == feedback:
        return button_feedback_handler(update=update, context=context)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
            KeyboardButton(text=view),
            KeyboardButton(text=usd),
            KeyboardButton(text=faq),
            KeyboardButton(text=feedback)
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text='Привет! Что хочешь узнать?\n\nСписок команд:\n \nCrypto — узнать актуальный курс 10 самых популярных '
             'криптовалют в мире\nUSD to — узнать курс доллара по отношению к RUB, EUR, UAH\nFAQ — ответы на '
             'вопросы\nFeedback — написать сообщение создателю бота',
        reply_markup=reply_markup,
    )

# Начало
def main():
    print('Статус бота — online!')
    updater = Updater(
    token='2083304857:AAGPdusBhGpRgIeO90ReNK8CQ2u-wrEkrWQ',
    use_context=True,
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()