import sys
sys.path.append("../")
import tokens
import telebot


bot = telebot.TeleBot(tokens.MyBudgetBot)


class User(object):
    def __init__(self):
        self.income = 0
        self.expense = 0
        self.budget = 0
        self.day_budget = 0
        self.balance = 0
        self.condition = "waiting income"

    def start(self, message):
        self.income = 0
        self.expense = 0
        self.budget = 0
        self.day_budget = 0
        bot.send_message(message.chat.id, "Привет\nКакой у тебя месячный доход в рублях?")
        self.condition = "waiting income"
        print("старт и запрос доходов\n")

    def give_income(self, message):
        self.income = int(message.text)
        bot.send_message(message.chat.id, "Окей. Теперь посчитай и пришли мне свои обязательные месячные расходы.")
        self.condition = "waiting expense"
        print("доход: " + message.text)
        print("запрос расходов\n")

    def give_expense(self, message):
        self.expense = int(message.text)
        self.budget = self.income - self.expense
        self.day_budget = round(self.budget / 30.5)
        self.balance += self.day_budget
        bot.send_message(message.chat.id, "Месячный бюджет: " + str(self.budget) + " ₽\nДневной бюджет: " + str(self.day_budget) + " ₽")
        bot.send_message(message.chat.id, "Теперь каждый вечр присылай мне сумму, которую ты потратил сегодня. А я покажу, укладываешся ли ты в свой бюджет.")
        self.condition = "waiting day expense"
        print("расход: " + message.text)
        print("бюджет: " + str(self.day_budget))
        print("запрос дневных расходов\n")

    def give_day_expense(self, message):
        self.balance -= int(message.text)
        bot.send_message(message.chat.id, "Баланс: " + str(self.balance) + " ₽")
        print("траты за день: " + message.text)
        print("баланс: " + str(self.balance) + "\n")
        self.balance += self.day_budget


user = User()


@bot.message_handler(commands=['start'])
def handler(message):
    user.start(message)


@bot.message_handler(content_types=['text'])
def handler(message):
    if user.condition == "waiting income" and message.text.isdigit():
        user.give_income(message)
    elif user.condition == "waiting expense" and message.text.isdigit():
        user.give_expense(message)
    elif user.condition == "waiting day expense" and message.text.isdigit():
        user.give_day_expense(message)



bot.polling()
