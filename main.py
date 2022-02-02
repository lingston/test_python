from flask import Flask, request, render_template
from datetime import datetime
import json
app = Flask(__name__)

# Список сообщений - массив словарей
db_file = "./data/db.json"
json_db = open(db_file, "rb")
data = json.load(json_db)
messages_list = data["messages_list"]

def save_messages():
    date = {
        "messages_list": messages_list,
    }
    json_db = open(db_file, "w")
    json.dump(data, json_db)

# Функция, которая умеет выводить одно сообщение
def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['date']}")
    print("-" * 50)


# Функция добавления нового сообщения
def add_message(name, txt):
    message = {
        "text": txt,
        "sender": name,
        "date": datetime.now().strftime("%H:%M"),
    }
    messages_list.append(message)  # Добавляем новое сообщение в список

# Пройдем по всем элементам списка (переменная m - конкретный элемент списка)
# for m in messages_list:
# print_message(m)

#главная страница
@app.route("/")
def index_page():
    return "Привет Looser"

#раздел со списком сообщений
@app.route("/get_messages")
def get_messages():
    return {"messages" : messages_list}

#раздел для отправки сообщения
@app.route("/send_message")
def send_message():
    name = request.args["name"]
    text = request.args["text"]
    if len(name) > 2 and len(name) < 101 :
        if len(text)>0 and len(text) < 3001 :
            add_message(name, text)
            save_messages()
            return "все отработало отлично!"
        else :
            add_message(name, "ERROR ПРОВЕРЬТЕ ПРАВИЛЬНОСТЬ НАБОРА ТЕКСТА")
            return "ERROR"
    else:
        add_message("ОШИБКА", "ERROR ПРОВЕРЬТЕ ПРАВИЛЬНОСТЬ НАБОРА ИМЕНИ" )
        return "ERROR"

#раздел с визуальным интерфейсом
@app.route("/form")
def form():
    return render_template("form.html")
app.run()
