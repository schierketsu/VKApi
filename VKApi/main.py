import tkinter as tk
from tkinter.ttk import Combobox
import tkinter.ttk as ttk
import vk_api

def add_like(vk, owner_id, item_id, type, v, status_label):
    try:
        vk.likes.add(owner_id=owner_id, item_id=item_id, type=type, v=v)
        status_label.config(text="Лайк успешно добавлен.")
    except Exception as e:
        status_label.config(text=f"Ошибка при добавлении лайка: {str(e)}")

def join_group(vk, group_id, v, status_label):
    try:
        vk.groups.join(group_id=group_id, v=v)
        status_label.config(text="Успешно вступили в группу.")
    except Exception as e:
        status_label.config(text=f"Ошибка при вступлении в группу: {str(e)}")

def leave_group(vk, group_id, v, status_label):
    try:
        vk.groups.leave(group_id=group_id, v=v)
        status_label.config(text="Успешно покинули группу.")
    except Exception as e:
        status_label.config(text=f"Ошибка при покидании группы: {str(e)}")

def process_choice():
    choice = choice_var.get()

    # Получение введенных токенов из виджета
    tokens = tokens_text.get("1.0", "end").strip().splitlines()

    if choice == "1":
        owner_id = owner_id_entry.get()
        item_id = item_id_entry.get()
        type_val = type_entry.get()
        v = v_combobox.get()

        for i, token in enumerate(tokens):
            session = vk_api.VkApi(token=token)
            vk = session.get_api()
            status_label = status_labels[i]
            add_like(vk, owner_id, item_id, type_val, v, status_label)

    elif choice == "2":
        group_id = group_id_entry.get()
        v = v_combobox.get()

        for i, token in enumerate(tokens):
            session = vk_api.VkApi(token=token)
            vk = session.get_api()
            status_label = status_labels[i]
            join_group(vk, group_id, v, status_label)

    elif choice == "3":
        group_id = group_id_entry.get()
        v = v_combobox.get()

        for i, token in enumerate(tokens):
            session = vk_api.VkApi(token=token)
            vk = session.get_api()
            status_label = status_labels[i]
            leave_group(vk, group_id, v, status_label)

def handle_choice_change(*args):
    choice = choice_var.get()

    if choice == "2" or choice == "3":
        type_label.config(state=tk.DISABLED)
        type_entry.config(state=tk.DISABLED)
        owner_id_label.config(state=tk.DISABLED)
        owner_id_entry.config(state=tk.DISABLED)
        item_id_label.config(state=tk.DISABLED)
        item_id_entry.config(state=tk.DISABLED)
    else:
        type_label.config(state=tk.NORMAL)
        type_entry.config(state=tk.NORMAL)
        owner_id_label.config(state=tk.NORMAL)
        owner_id_entry.config(state=tk.NORMAL)
        item_id_label.config(state=tk.NORMAL)
        item_id_entry.config(state=tk.NORMAL)

    if choice == "1":
        group_id_label.config(state=tk.DISABLED)
        group_id_entry.config(state=tk.DISABLED)
    else:
        group_id_label.config(state=tk.NORMAL)
        group_id_entry.config(state=tk.NORMAL)

# Создание графического интерфейса
root = tk.Tk()
root.title("VK API")
root.geometry("768x428")
root.iconbitmap("icon.ico")
def handle_key(event):
    if event.state == 12 and event.keycode == 47:
        clipboard = root.clipboard_get()
        tokens_text.delete("1.0", "end")
        tokens_text.insert("insert", clipboard)

root.bind("<Key>", handle_key)

# Выбор действия
choice_label = tk.Label(root, text="Выберите действие:")
choice_label.place(x=10, y=10)

choice_var = tk.StringVar()
choice_var.set("0")
choice_var.trace("w", handle_choice_change)

choice_radio_1 = tk.Radiobutton(root, text="Добавить лайк", variable=choice_var, value="1")
choice_radio_1.place(x=10, y=30)

choice_radio_2 = tk.Radiobutton(root, text="Вступить в группу", variable=choice_var, value="2")
choice_radio_2.place(x=10, y=50)

choice_radio_3 = tk.Radiobutton(root, text="Покинуть группу", variable=choice_var, value="3")
choice_radio_3.place(x=10, y=70)

# Ввод параметров
owner_id_label = tk.Label(root, text="Введите id владельца объекта:")
owner_id_label.place(x=10, y=100)

owner_id_entry = tk.Entry(root)
owner_id_entry.place(x=10, y=120)

item_id_label = tk.Label(root, text="Введите id объекта:")
item_id_label.place(x=10, y=150)

item_id_entry = tk.Entry(root)
item_id_entry.place(x=10, y=170)

type_label = tk.Label(root, text="Введите тип:")
type_label.place(x=10, y=200)

type_entry = tk.Entry(root)
type_entry.place(x=10, y=220)

group_id_label = tk.Label(root, text="Введите id группы:")
group_id_label.place(x=10, y=250)

group_id_entry = tk.Entry(root)
group_id_entry.place(x=10, y=270)

v_label = tk.Label(root, text="Выберите v*:")
v_label.place(x=10, y=300)

v_values = ["5.92", "5.131"]  # Возможные значения для v
v_combobox = Combobox(root, values=v_values)
v_combobox.place(x=10, y=320)

tokens_label = tk.Label(root, text="Введите токены (каждый токен на новой строке):")
tokens_label.place(x=200, y=10)

tokens_text = tk.Text(root, height=6, width=50, borderwidth=0, wrap="none")
tokens_text.place(x=200, y=30)
style = ttk.Style()
style.configure("Status.TLabel", foreground="blue", font=("Helvetica", 10, "bold"))
# Окна статуса для каждого токена
status_labels = []
for i in range(10):  # Предполагается, что будет не более 5 токенов
    status_label = tk.Label(root, text="")
    status_label.place(x=200, y=140 + i * 20)
    status_labels.append(status_label)

# Кнопка для выполнения действия
process_button = tk.Button(root, text="Выполнить", command=process_choice)
process_button.place(x=10, y=350)

root.mainloop()