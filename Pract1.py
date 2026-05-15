# 3.	Створіть програму, яка приймає два числа від користувача та виводить їх суму.
num1 = float(input("Введіть перше число: "))
num2 = float(input("Введіть друге число: "))

sum_result = num1 + num2

print(f"Сума чисел {num1} та {num2} дорівнює: {sum_result}\n")

# 3.	Створіть програму, яка приймає два числа від користувача та виводить їх суму.
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

number = int(input("Введіть ціле число для перевірки: "))

if is_prime(number):
    print(f"Число {number} є простим.\n")
else:
    print(f"Число {number} не є простим.\n")

    
for n in range(2, number + 1):
    if is_prime(n):
        print(n)

# 3.	Створіть клас "Калькулятор" з методами для додавання, віднімання, множення та ділення. 
# Виведіть результат обчислень для певного прикладу.
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Ділити на нуль не можна."
        return a / b

my_calc = Calculator()

x = 26
y = 0

print(f"Результати для чисел {x} та {y}:")
print(f"Додавання: {my_calc.add(x, y)}")
print(f"Віднімання: {my_calc.subtract(x, y)}")
print(f"Множення: {my_calc.multiply(x, y)}")
print(f"Ділення: {my_calc.divide(x, y)}\n")

#3.	Створіть клас "Книготека" з можливістю додавання та видалення книг, 
# а також виведення списку усіх книг.
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book_title):
        self.books.append(book_title)
        print(f"Книгу '{book_title}' додано.")

    def remove_book(self, book_title):
        if book_title in self.books:
            self.books.remove(book_title)
            print(f"Книгу '{book_title}' видалено.")
        else:
            print(f"Книги '{book_title}' немає в списку.")

    def show_all_books(self):
        if not self.books:
            print("Книготека порожня.")
        else:
            print("\nСписок усіх книг:")
            for index, book in enumerate(self.books, 1):
                print(f"{index}. {book}")

my_library = Library()
my_library.show_all_books()
my_library.add_book("Якийсь нейм")
my_library.add_book("Ляляля")
my_library.show_all_books()
my_library.remove_book("Нейм")
my_library.remove_book("Якийсь нейм")
my_library.show_all_books()