import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

questions = [
    {
        'question': 'В каком году был основан Омск?',
        'options': ['1906', '1716', '2018', '918'],
        'correct_answer': '1716'
    },
    {
        'question': 'Какого цвета глаза были у Брежнего?',
        'options': ['карие', 'зеленые', 'синие', 'красные'],
        'correct_answer': 'карие'
    },
    {
        'question': 'Сколько в мире океанов?',
        'options': ['3', '4', '5', '6'],
        'correct_answer': '5'
    },
    {
        'question': 'Как звали кролика в мультфильме смешарики?',
        'options': ['крош', 'ежик', 'совунья', 'пин'],
        'correct_answer': 'крош'
    },
    {
        'question': 'Когда была создан легендарный видеохостинг ютуб?',
        'options': ['14 февраля 2005', '6 июня 2007', '5 октября 2007', '11 сентября 2001'],
        'correct_answer': '14 февраля 2005'
    }
]

user_answers = {}
current_question = 0


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Начать игру')
    item2 = types.KeyboardButton('Информация о боте')
    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Доброго времени суток, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы проверить твои знания".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == 'начать игру')
def start_game(message):
    ask_question(message.chat.id)


@bot.message_handler(func=lambda message: message.text.lower() == 'информация о боте')
def bot_info(message):
    bot.send_message(message.chat.id, 'Бот создан гением этого мира - Никитой Бомбакью')


def ask_question(chat_id):
    global current_question
    question_data = questions[current_question]

    markup = types.InlineKeyboardMarkup(row_width=2)
    for option in question_data['options']:
        button = types.InlineKeyboardButton(option, callback_data=option)
        markup.add(button)

    bot.send_message(chat_id, question_data['question'], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global current_question
    try:
        if call.message:
            user_answer = call.data
            correct_answer = questions[current_question]['correct_answer']
            if user_answer == correct_answer:
                bot.send_message(call.message.chat.id, 'Всё верно! Ты делаешь успехи!')
                current_question += 1
                if current_question < len(questions):
                    ask_question(call.message.chat.id)
                else:
                    bot.send_message(call.message.chat.id, "ПОЗДРАВЛЯЕМ!!!!! ВЫ ВЫИГРАЛИ 16 РУБЛЕЙ, ну а что вы миллион хотели")
            else:
                bot.send_message(call.message.chat.id, 'Неверно. Попробуй-ка еще раз.')
                current_question = 0
                ask_question(call.message.chat.id)

            # remove inline buttons


    except Exception as e:
        print(repr(e))


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    bot.send_message(message.chat.id, 'Выберите одну из кнопочек')


bot.polling(none_stop=True)
