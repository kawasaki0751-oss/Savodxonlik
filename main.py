
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import database

# Tokenni o'zingniki bilan almashtir
TOKEN = "8989007841:AAE89fFAnH0AI4mZdOXRBdtuvOKI53e4-_I"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# FSM holatlari (bot nima qilayotganini tushunishi uchun)
class ExpenseForm(StatesGroup):
    waiting_for_category = State()
    waiting_for_amount = State()

database.init_db()

# Bosh menyu
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Xarajat qo'shish"), KeyboardButton(text="📊 Hisobot")],
            [KeyboardButton(text="🔄 Ma'lumotlarni tozalash")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Xush kelibsiz! Pul hisobini yuritishni boshlaymiz.", reply_markup=main_menu())

# 1. Xarajat qo'shishni boshlash
@dp.message(F.text == "➕ Xarajat qo'shish")
async def add_expense_start(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Ovqatlanish"), KeyboardButton(text="Transport")],
                  [KeyboardButton(text="Kunlik Xarajatlar"), KeyboardButton(text="Uyga bozorlik")]],
        resize_keyboard=True
    )
    await message.answer("Xarajat turini tanlang:", reply_markup=kb)
    await state.set_state(ExpenseForm.waiting_for_category)

# 2. Toifani qabul qilish va summani so'rash
@dp.message(ExpenseForm.waiting_for_category)
async def get_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Endi summani raqam bilan yozing:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ExpenseForm.waiting_for_amount)

# 3. Summani qabul qilish va bazaga saqlash
@dp.message(ExpenseForm.waiting_for_amount)
async def get_amount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, faqat raqam kiriting!")
        return
    
    data = await state.get_data()
    category = data['category']
    amount = int(message.text)
    
    database.add_expense(message.from_user.id, amount, category)
    await message.answer(f"{category} uchun {amount} so'm saqlandi!", reply_markup=main_menu())
    await state.clear()

# Hisobot
@dp.message(F.text == "📊 Hisobot")
async def show_report(message: types.Message):
    results = database.get_report_by_category(message.from_user.id)
    if not results:
        await message.answer("Hozircha xarajatlar yo'q.")
        return
    
    report = "📊 **Sizning xarajatlaringiz:**\n\n"
    grand_total = 0 # Jami summa
    for category, total in results:
        report += f"• {category}: {total:,} so'm\n"
        grand_total += total
    
    report += f"\n💰 **Jami: {grand_total:,} so'm**"
    await message.answer(report, parse_mode="Markdown")
# Ma'lumotlarni tozalash funksiyasi
@dp.message(F.text == "🔄 Ma'lumotlarni tozalash")
async def reset_handler(message: types.Message):
    database.reset_expenses(message.from_user.id)
    await message.answer("Tarix tozalandi! 🧹", reply_markup=main_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())