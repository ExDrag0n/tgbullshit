import telebot
import pyqrcode
from telebot import types
from path import Path
import cv2 as cv
from pyzbar import pyzbar

TOKEN = "7394170719:AAFBiHYFsiSqKjjS3P4YvO7O9zVYASFG02A"


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Создать QR-код по имеющейся ссылке")
        btn2 = types.KeyboardButton("Расшифровать имеющийся QR-код")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Привет! Я бот для создания или расшифровки QR-кодов!".format(message.from_user), reply_markup=markup)
    except Exception:
        return print('Ошибка выполнения!')


@bot.message_handler(content_types=['text'])
def start_message(message):
    if message.text == 'Расшифровать имеющийся QR-код':
        bot.send_message(message.chat.id, 'Отправьте QR-код который хотите расшифровать:')

        @bot.message_handler(content_types=['photo'])
        def handle_docs_photo(message):
            global path_to_download
            try:
                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = file_info.file_path
                print(src)
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                path_to_download = Path().joinpath(src)

                def decrypt(path_to_download):
                    img = cv.imread(path_to_download)
                    barcodes = pyzbar.decode(img)

                    for barcode in barcodes:
                        barcodeData = barcode
                        return barcodeData

                text_back = decrypt(path_to_download)
                bot.send_message(message.chat.id, text_back)
                bot.send_message(message.chat.id, 'Ваш QR-код успешно расшифрован!')

            except Exception as e:
                bot.reply_to(message, str(e))
    elif message.text == "Создать QR-код по имеющейся ссылке":
        bot.send_message(message.chat.id, 'Введите /make (url)')

    @bot.message_handler(content_types=["text"])
    def make_qrcode(url):
        qrcode = pyqrcode.create(url)
        qrcode.png("QR CODE.png", scale=6)
        with open("QR CODE.png", mode="rb") as file:
            bot.send_photo(message.chat.id, photo=file)
    if message.text.find("/make") != -1:
        get_url = message.text.replace("/make", "")
        make_qrcode(url=get_url)


    def wp(message):
        bot.send_message(message.chat.id, 'Спасибо!')
    if message.text.find('Good Bot!') != -1 or message.text.find('Well done bot!') != -1 or message.text.find('good bot!') != -1 or message.text.find('good bot') != -1:
        wp(message)

bot.polling(none_stop=True, interval=0)
