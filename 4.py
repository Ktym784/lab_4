import os
import csv

# 3. Наследование: базовый класс для записей
class BaseRecord:
    pass

# 3. Наследование: класс посетителя
class Visitor(BaseRecord):
    # 4. Запись значений в свойства ТОЛЬКО через __setattr__ (контроль типов)
    def __setattr__(self, name, value):
        if name == 'id':
            value = int(value)  # Гарантируем целое число
        elif name == 'is_in':
            # Гарантируем булево значение
            value = str(value).strip().lower() in ('true', 'вход', '1')
        # super() вызывает стандартный механизм присваивания
        super().__setattr__(name, value)

    # 2. Перегрузка стандартной операции __repr__ (красивый вывод объекта)
    def __repr__(self):
        status = "Вход" if getattr(self, 'is_in', False) else "Выход"
        return f"[{getattr(self, 'id', '?')}] {getattr(self, 'dt', '')} | {status} | {getattr(self, 'gender', '')}"


# 3. Наследование: базовый класс для работы с данными и файлами
class BaseDataHandler:
    # 6. Статический метод (не требует создания экземпляра)
    @staticmethod
    def count_files_in_dir(dir_path="."):
        """Считает количество файлов в папке."""
        return sum(1 for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)))


# Основной класс коллекции посетителей
class VisitorCollection(BaseDataHandler):
    def __init__(self, filename):
        self.items = []
        self._idx = 0  # Счётчик для итератора
        if os.path.isfile(filename):
            self._load_csv(filename)

    def _load_csv(self, filename):
        with open(filename, 'r', encoding='cp1251') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Пропускаем заголовок
            for row in reader:
                if not row: continue
                v = Visitor()
                # Присваивание проходит через __setattr__ класса Visitor
                v.id = row[0]
                v.dt = row[1].strip()
                v.is_in = row[2]
                v.gender = row[3].strip()
                self.items.append(v)

    # 5. Доступ к элементам коллекции по индексу
    def __getitem__(self, index):
        return self.items[index]

    # 1. Итератор (позволяет использовать цикл for напрямую по объекту)
    def __iter__(self):
        self._idx = 0
        return self

    def __next__(self):
        if self._idx < len(self.items):
            val = self.items[self._idx]
            self._idx += 1
            return val
        raise StopIteration

    # 7. Генератор: фильтрация (только входы)
    def gen_entries_only(self):
        for item in self.items:
            if item.is_in:
                yield item

    # 7. Генератор: сортировка по полу
    def gen_sorted_by_gender(self):
        for item in sorted(self.items, key=lambda x: x.gender):
            yield item

    # 2. Перегрузка __repr__ для всей коллекции
    def __repr__(self):
        return f"Коллекция посетителей (всего: {len(self.items)})"

    # Сохранение обратно в CSV
    def save_to_csv(self, filename):
        with open(filename, 'w', encoding='cp1251', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['№', 'дата и время', 'вход/выход', 'пол'])
            for v in self.items:
                writer.writerow([v.id, v.dt, v.is_in, v.gender])


# ================= ЗАПУСК И ДЕМОНСТРАЦИЯ =================
if __name__ == "__main__":
    # 1. Подсчёт файлов (используем статический метод)
    files_count = VisitorCollection.count_files_in_dir(".")
    print(f"📁 Файлов в текущей папке: {files_count}\n")

    # Загрузка данных
    csv_file = "data.csv"
    visitors = VisitorCollection(csv_file)
    print(visitors)  # Вызовет __repr__ коллекции
    print("-" * 40)

    # 5. Доступ по индексу
    print("📍 Первый посетитель по индексу [0]:")
    print(visitors[0])  # Вызовет __getitem__ и __repr__ объекта
    print("-" * 40)

    # 1. Использование итератора (цикл for)
    print("🔄 Итерация по всей коллекции (for):")
    for v in visitors:
        print(v)
    print("-" * 40)

    # 2.1 Сортировка по строковому полю (через генератор)
    print(" Отсортировано по полу (генератор):")
    for v in visitors.gen_sorted_by_gender():
        print(v)
    print("-" * 40)

    # 2.3 Фильтрация по критерию (только входы, через генератор)
    print("🚪 Только входы (генератор):")
    entries = list(visitors.gen_entries_only())
    for v in entries:
        print(v)
    print("-" * 40)

    # 3. Сохранение отфильтрованных данных в новый файл
    visitors.items = entries  # Обновляем внутреннюю коллекцию
    visitors.save_to_csv("data_filtered.csv")
    print("💾 Отфильтрованные данные сохранены в data_filtered.csv")
# # Updated: добавлено для лабораторной по Git
