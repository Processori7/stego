import tkinter as tk
from translate import Translator
from re import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageDraw
from random import randint

root = tk.Tk()
root.title("Encrypt/Decrypt")
root.geometry("800x600")

def encrypt():
    translator = Translator(from_lang="ru", to_lang="en")
    keys = []
    filename = askopenfilename()
    if filename:
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)
        width, height = img.size
        pix = img.load()
        with open('keys.txt', 'w') as f:
            text_input = text_input_entry.get("1.0", "end-1c")
            translation_en = translator.translate(text_input)
            result_label.config(text=translation_en)
            for elem in ([ord(elem) for elem in translation_en]):
                key = (randint(1, width - 10), randint(1, height - 10))
                g, b = pix[key][1:3]
                draw.point(key, (elem, g, b))
                f.write(str(key) + '\n')
        key_label.config(text='Ключ был записан в файл keys.txt, он необходим для расшифровки соощения')
        image_label.config(text="Сейчас появиться новая картинка с именем newimage, в которой будет записано послание.")
        img.save("newimage.png", "PNG")
        text_input_entry.delete("1.0", "end")

def decrypt():
    translator = Translator(from_lang="en", to_lang="ru")
    a = []
    keys = []
    message_label.config(text="Пожалуйста, выберите изображение для декодирования")
    filename = askopenfilename()
    if filename:
        message_label.config(text="Пожалуйста, выберите файл с ключами")
        filename1 = askopenfilename()
        if filename1:
            img = Image.open(filename)
            pix = img.load()
            with open(filename1, 'r', encoding="utf-8") as f:
                y = str([line.strip() for line in f])
                for i in range(len(findall(r'(\d+)\,', y))):
                    keys.append((int(findall(r'(\d+)[\,]', y)[i]), int(findall(r'[\,]\s(\d+)\)', y)[i])))
            for key in keys:
                a.append(pix[tuple(key)][0])
            message = ''.join([chr(elem) for elem in a])
            message_label.config(text=f"Ваше сообщение: {translator.translate(message)}")
        else:
            message_label.config(text="Пожалуйста, выберите файл с ключами")
    else:
        message_label.config(text="Пожалуйста, выберите изображение для декодирования")

text_input_label = tk.Label(root, text="Введите текст:")
text_input_label.pack(pady=10)

text_input_entry = tk.Text(root, width=60, height=5)
text_input_entry.pack(pady=10)

encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt)
encrypt_button.pack(pady=20)

decrypt_button = tk.Button(root, text="Расшифровать", command=decrypt)
decrypt_button.pack(pady=20)

result_label = tk.Label(root)
result_label.pack(pady=10)

key_label = tk.Label(root)
key_label.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

message_label = tk.Label(root)
message_label.pack(pady=10)

root.mainloop()