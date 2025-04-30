from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from packs.user import load_profiles, save_profiles, create_or_update_profile, get_top_position
import time, random
import re


TOKEN = "7757241377:AAFspPE2PO-CAJMEONYCNi1zReXE9EN1k5w"


#обработчик сообщений!
async def start(update: Update, context):
    user = update.message.from_user
    await update.message.reply_text(f"Привет, {user.first_name}! Готов ли ты, стать настоящим гоем, чтобы греть других гоев и заставлять их рабоать на тябя? Жми на кнопку и вперёд!\n ")

async def info(update: Update, context):
    await update.message.reply_text("*Инфо:* \n /start - презагрузка бота \n /profil - окрыть профиль \n /farm - фармить койны /bet <сколько> <цисло от 1 до 6>")

async def profile(update: Update, context):
    user = update.message.from_user
    profil = create_or_update_profile(user.id, user.first_name)
    await update.message.reply_text(
            f"👤 Профиль игрока: {profil["name"] }\n"
            f"💵Баланс: {profil["balance"]} ГК\n"
            f"🎮 Уровень: {profil["xp"] / 10}\n"
            f"🏆Место в топе: {get_top_position(user.id)} \n"
    )

async def farm(update: Update, context):
    user = update.message.from_user
    profiles = load_profiles()
    prof = create_or_update_profile(user.id, user.first_name)
    current_time = time.time()
    if current_time - prof['last_farm_time'] < 600:
        remaining = int(600 - (current_time - prof["last_farm_time"]))
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        await update.message.reply_text(f"⏳ До следующей фармы осталось {minutes} минут.")
        return
    else:
        bricks_received = random.randint(1, prof["xp"])
        prof["balance"] += bricks_received
        xppp = random.choice([10, 20, 30, 40, 50])
        prof["xp"] += xppp
        prof["last_farm_time"] = current_time
        profiles[str(user.id)] = prof
        save_profiles(profiles)
        await update.message.reply_text(f"🎉 Вы получили {bricks_received} ГК!\n Опыта полученно: {xppp}")

async def transfer(update: Update, context):
    if not context.args:  # Проверяем, передан ли аргумент
        await update.message.reply_text("❌ Ошибка! Используйте: `/transfer <количество>`")
        return

    if not context.args[0].isdigit():  # Проверяем, является ли аргумент числом
        await update.message.reply_text("❌ Ошибка! Введите число для перевода, например: `/transfer 50`")
        return
    
    coin = int(context.args[0])  # Конвертируем в число

    if update.message.reply_to_message:  # Проверяем, ответ ли это на сообщение
        profiles = load_profiles()  # Загружаем профили
        
        rep_user = update.message.reply_to_message.from_user  # Получатель перевода
        user = update.message.from_user  # Отправитель перевода

        # Создаем или обновляем профили
        rep_profil = create_or_update_profile(rep_user.id, rep_user.first_name)
        profil = create_or_update_profile(user.id, user.first_name)

        # Проверяем баланс
        if profil["balance"] >= coin:
            profil["balance"] -= coin
            rep_profil["balance"] += coin
            
            # Обновляем словарь профилей
            profiles[str(rep_user.id)] = rep_profil
            profiles[str(user.id)] = profil
            
            save_profiles(profiles)  # Сохраняем изменения
            
            await update.message.reply_text(f"✅ Вы перевели {coin} ГК игроку {rep_user.first_name}! 🥳")
        else:
            await update.message.reply_text(f"❌ {user.first_name}, у вас недостаточно ГК для перевода!")
    else:
        await update.message.reply_text("❌ Ошибка! Ответьте на сообщение того, кому хотите отправить монеты.")

async def bet(update: Update, context):
    if not context.args:
        await update.message.reply_text("Ведите число и ставку /bet <сколько> <ставка от 1 до 6>")
        return
    if not context.args[0].isdigit():  # Проверяем, является ли аргумент числом
        await update.message.reply_text("❌ Ошибка! Введите число!")
        return
    if not context.args[1].isdigit():  # Проверяем, является ли аргумент числом
        await update.message.reply_text("❌ Ошибка! Введите число!")
        return
    
    user = update.message.from_user

    profiles = load_profiles()
    prof = create_or_update_profile(user.id, user.first_name)


    coin = int(context.args[0])
    stavka = int(context.args[1])

    # Отправка кубика с анимацией
    msg = await update.message.reply_dice(emoji="🎲")
    if stavka == msg.dice.value:
        coin = coin * 10
        prof["balance"] += coin
        profiles[str(user.id)] = prof
        save_profiles(profiles)
        await update.message.reply_text(f"{user.first_name} ваша ставка выиграла!🥳 Вы получаете {coin * 10}")
    else:
        prof["balance"] -= coin
        profiles[str(user.id)] = prof
        save_profiles(profiles)






async def textuser(update: Update, context):
    user_text = update.message.text.lower()
    if user_text.startswith(("фарма", "фармить")):
        user = update.message.from_user
        profiles = load_profiles()
        prof = create_or_update_profile(user.id, user.first_name)

        current_time = time.time()
        if current_time - prof['last_farm_time'] < 600:
            remaining = int(600 - (current_time - prof["last_farm_time"]))
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            await update.message.reply_text(f"⏳ До следующей фармы осталось {minutes} минут.")
            return
        else:
            bricks_received = random.randint(1, prof["xp"])
            prof["balance"] += bricks_received
            prof["xp"] += 10
            prof["last_farm_time"] = current_time
            profiles[str(user.id)] = prof
            print(profiles)
            save_profiles(profiles)
            await update.message.reply_text(f"🎉 Вы получили {bricks_received} ГК!\n")

    elif user_text.startswith("топ"):
        profiles = load_profiles()
        sorted_profiles = sorted(profiles.items(), key=lambda x: x[1]["balance"], reverse=True)
        top_message = "🏆 *Топ пользователей:*\n"
        for index, (user_id, profile) in enumerate(sorted_profiles[:10], start=1):  # Ограничение на топ-10
            top_message += f"{index}. {profile['name']} — {profile['balance']} ГойКойнов\n"
        if not sorted_profiles:
            top_message = "Никто ещё не создал профиль или не заработал ГойКойны!."
        await update.message.reply_text(top_message)

    elif user_text.startswith("профиль"):
        if update.message.reply_to_message:
            rep_user = update.message.reply_to_message.from_user
            rep_profil = create_or_update_profile(rep_user.id, rep_user.first_name)
            await update.message.reply_text(
            f"👤 Профиль игрока: {rep_profil["name"] }\n"
            f"💵Баланс: {rep_profil["balance"]} ГК\n"
            f"🎮 Уровень: {rep_profil["xp"] / 10}\n"
            f"🏆Место в топе: {get_top_position(user.id)} \n"
        )
        else:
            user = update.message.from_user
            profil = create_or_update_profile(user.id, user.first_name)
            await update.message.reply_text(
            f"👤 Профиль игрока: {profil["name"] }\n"
            f"💵Баланс: {profil["balance"]} ГК\n"
            f"🎮 Уровень: {profil["xp"] / 10}\n"
            f"🏆Место в топе: {get_top_position(user.id)} \n"
            )
   



async def transfer_without_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем текст сообщения, убираем лишние пробелы
    user_text = update.message.text.strip()

    # Приводим текст к нижнему регистру и проверяем, начинается ли с "перевод"
    if user_text.lower().startswith("перевод"):
        # Разбиваем сообщение по пробелам
        parts = user_text.split()
        if len(parts) < 2:
            await update.message.reply_text("❌ Ошибка! Используйте: `перевод <количество>`")
            return

        # Проверяем, что второй элемент – число (поддержка отрицательных значений, если нужно)
        if not parts[1].replace("-", "").isdigit():
            await update.message.reply_text("❌ Ошибка! Введите число для перевода, например: `перевод 50`")
            return

        # Преобразуем строку в число
        coin = int(parts[1])
        
        # Проверяем, что сообщение является ответом на другое сообщение
        if update.message.reply_to_message:
            # Загружаем профили; если функция load_profiles() может вернуть None, подставляем {}
            profiles = load_profiles() or {}
            
            # Определяем отправителя (тот, кто делает перевод) и получателя (тот, кому ответили)
            rep_user = update.message.reply_to_message.from_user  # Получатель перевода
            user = update.message.from_user  # Отправитель перевода

            # Создаем или обновляем профили для обоих пользователей
            rep_profil = create_or_update_profile(rep_user.id, rep_user.first_name)
            profil = create_or_update_profile(user.id, user.first_name)

            # Проверяем, достаточно ли средств у отправителя для перевода
            if profil["balance"] >= coin:
                profil["balance"] -= coin
                rep_profil["balance"] += coin

                # Обновляем словарь профилей (ключи приведены к строке для единообразия)
                profiles[str(rep_user.id)] = rep_profil
                profiles[str(user.id)] = profil

                # Сохраняем изменения
                save_profiles(profiles)

                await update.message.reply_text(f"✅ Вы перевели {coin} ГК игроку {rep_user.first_name}! 🥳")
            else:
                await update.message.reply_text(f"❌ {user.first_name}, у вас недостаточно ГК для перевода!")
        else:
            await update.message.reply_text("❌ Ошибка! Ответьте на сообщение того, кому хотите отправить монеты.")












def main():
    #создаю приложение 
   app = Application.builder().token(TOKEN).build()
   
   #commds
   app.add_handler(CommandHandler("start", start))
   app.add_handler(CommandHandler("info", info))
   app.add_handler(CommandHandler("profil", profile))
   app.add_handler(CommandHandler("farm", farm))
   app.add_handler(CommandHandler("transfer", transfer))
   app.add_handler(CommandHandler("bet", bet))


   app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, textuser))

   app.add_handler(MessageHandler(filters.TEXT, transfer_without_command))


   app.run_polling()



if __name__ == "__main__":
    main()