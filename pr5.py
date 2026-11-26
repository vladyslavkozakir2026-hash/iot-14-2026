from functools import wraps
from abc import ABC, abstractmethod
import math


def check_not_empty(method_to_dec):
    @wraps(method_to_dec)
    def wrapper(self, *args, **kwargs):
        if not self.fishes:
            print(f"Декоратор в акваріумі {self.title} ще немає рибок для виконання цієї дії!")
            return None
        return method_to_dec(self, *args, **kwargs)     
        
    return wrapper


# Спільний абстрактний базовий клас
class BaseAquarium(ABC):
    @abstractmethod
    def add_fish(self, fish):
        pass


#клас риб
class Fish:
    def __init__(self, name, age, species, size, preffered_food, is_Aggressive, needed_space):
        if not isinstance(age, (int, float)) or isinstance(age, bool):
            raise TypeError("age риби має бути числом!")
        if not math.isfinite(age) or age <= 0:
            raise ValueError("age риби має бути скінченним числом, більшим за 0!")

        if not isinstance(size, (int, float)) or isinstance(size, bool):
            raise TypeError("size має бути числом!")
        if not math.isfinite(size) or size <= 0:
            raise ValueError("size має бути скінченним числом, більшим за 0!")

        if not isinstance(needed_space, (int, float)) or isinstance(needed_space, bool):
            raise TypeError("needed_space має бути числом!")
        if not math.isfinite(needed_space) or needed_space <= 0:
            raise ValueError("needed_space має бути скінченним числом, більшим за 0!")

        if not isinstance(is_Aggressive, bool):
            raise TypeError("Поле is_Aggressive має бути типу bool!")

        self.name = name                         
        self.age = age                           
        self.species = species                
        self.size = size                         
        self.preffered_food = preffered_food       
        self.is_Aggressive = is_Aggressive
        self.needed_space = needed_space
        self.aquarium=None        

    #гетер виду риби
    @property
    def species(self):
        return self.__species
    
    #сеттер виду риби
    @species.setter
    def species(self, new_species):
        if not isinstance(new_species, str):
            raise TypeError("Вид рибки має бути рядком!")
        if not new_species.strip(): #якщо new_species пустий або пустий з пробілами, strip забере їх усі, а також пустий рядок - False. тоді з not- це тру
            raise ValueError("Вид рибки має бути непорожнім рядком!")
        self.__species = new_species.strip()

    #виводимо характеристики рибки
    def __str__(self):
        temper = "Агресивна" if self.is_Aggressive else "Мирна"
        return (
            f"{self.__species} '{self.name}' "
            f"(вік: {self.age} р., розмір: {self.size} см, {temper}, треба {self.needed_space} м³)"
        )
    
    #базові технічні характеристики
    def __repr__(self):
        return f"Fish('{self.name}', '{self.__species}', {self.size} см)"
    

    def __del__(self):
        pass


class Aquarium(BaseAquarium):
    #ініціюєм акваріум
    def __init__(self, totalvol, title):
        if not isinstance(totalvol, (int, float)) or isinstance(totalvol, bool):
            raise TypeError("Об'єм акваріума має бути числом!")
        if not math.isfinite(totalvol) or totalvol <= 0:
            raise ValueError("Об'єм акваріума має бути скінченним числом, більшим за 0!")
        self.__totalvol = totalvol  #заприватили об'єм
        self._fishes = []             
        self.title = title 

    #getter fishes list
    @property
    def fishes(self):
        return tuple(self._fishes)

    
    @property
    def free_space(self):
        used=sum(f.needed_space for f in self._fishes)
        return round(self.totalvol - used, 2)

    #геттер об'єму      
    @property
    def totalvol(self):
        return self.__totalvol
    
    def add_fish(self, fish):

        if fish in self._fishes:
            print (f"[Відмова -> {self.title}] Рибка '{fish.name}' уже є в цьому акваріумі")
            return False
        
        if fish.aquarium is not None:
            print( f"[Відмова -> {self.title}] Рибка '{fish.name}' уже живе в акваріумі "
                f"'{fish.aquarium.title}'!" )
            return False
        
        if fish.needed_space > self.free_space:
            print(
                f"[Відмова -> {self.title}] Замало місця для '{fish.name}'! "
                f"Треба {fish.needed_space} м³, вільно тільки {self.free_space} м³."
            )
            return False

        if len(self._fishes) > 0:
            aq_temper = self.fishes[0].is_Aggressive
            if aq_temper != fish.is_Aggressive:
                curtemp = "агресивну" if fish.is_Aggressive else "мирну"
                print(
                    f"[Відмова -> {self.title}] Не можна підселити {curtemp} рибу "
                    f"'{fish.name}' до риб протилежних за характером!"
                )
                return False

        self._fishes.append(fish)
        fish.aquarium=self

        print(
            f"[Успіх -> {self.title}] Рибку '{fish.name}' додано! "
            f"Вільно місця: {self.free_space} м³."
        )
        return True



    #top 3 найбільші
    
    def get_top_3biggest(self):

        sorted_fishes = sorted(self.fishes, key=lambda f: f.size, reverse=True)
        return sorted_fishes[:3]
    
    @check_not_empty
    def show_top_3biggest(self):
        print(f"\n--- Топ-3 найбільших риб в акваріумі {self.title} ---")
        top_fishes = self.get_top_3biggest()
        for i, fish in enumerate(top_fishes, start=1):
            print(f"{i}. {fish}")

    def __str__(self):
        return (
            f"Акваріум {self.title}: загальний об'єм {self.__totalvol} м³, "
            f"вільно {self.free_space} м³, рибок: {len(self.fishes)}"
        )

    def __del__(self):
        pass

class QuarantineAquarium(Aquarium):
    def __init__(self, totalvol, title, max_fishes=2):
        super().__init__(totalvol, title)
        if not isinstance(max_fishes, int) or isinstance(max_fishes, bool):
            raise TypeError("max_fishes має бути цілим числом!")
        if max_fishes <= 0:
            raise ValueError("max_fishes має бути більшим за 0!")
        self.__max_fishes = max_fishes
    
    #read-only
    @property
    def max_fishes(self):
        return self.__max_fishes
    
    def add_fish(self, fish):
        if len(self.fishes) >= self.max_fishes:
            print(
                f"[Відмова--> {self.title}. "
                f"В акваріумі може бути не більше {self.max_fishes} риб]"
            )
            return False
        return super().add_fish(fish)
 

def main():
    #self, name, age, species, size, prefferedfood, isAggressive, neededspace))) reference
    nemo = Fish("Немо", 1, "Риба-клоун", 6.5, "Планктон", False, 0.2)
    dory = Fish("Дорі", 2, "Блакитний хірург", 12.0, "Водорості", False, 0.3)
    goldie = Fish("Златка", 1.5, "Золота рибка", 15.5, "Корм", False, 0.3)
    angel = Fish("Сніжинка", 3, "Скалярія", 18.0, "Мотиль", False, 0.5)

    shark = Fish("Брюс", 5, "Рифова акула", 120.0, "Риба", True, 2.5)
    piranha = Fish("Зубастик", 2, "Піранья", 25.0, "М'ясо", True, 0.8)
    oscar = Fish("Тайсон", 3, "Астронотус", 30.0, "Креветки", True, 1.0)
    barracuda = Fish("Стріла", 4, "Баракуда", 85.0, "Риба", True, 1.5)

    print("\n=== ПЕРЕВІРКА ПРИВАТНИХ ПОЛІВ ТА @property ===")
    print("\n=== перевіряємо приватні поля та сетер/гетер через декоратор ===")
    print("Вид рибки (через @property):", nemo.species)
    nemo.species = "Амфіпріон (Риба-клоун)"
    print("Оновлений вид:", nemo.species)
    print("Розмір (публічне поле):", nemo.size, "см")

    print("\n=== АКВАРІУМ #1 (МИРНИЙ) ===")
    aq1 = Aquarium(1.0, "#1")
    print("Об'єм акваріума (через @property):", aq1.totalvol, "м³")
    print("Об'єм акваріума:", aq1.totalvol, "м³")

    aq1.add_fish(nemo)
    aq1.add_fish(dory)
    aq1.add_fish(goldie)
    aq1.add_fish(piranha)   
    
    print("\n" + str(aq1))
    aq1.show_top_3biggest()
    
    print("\n=== АКВАРІУМ #2 (ХИЖИЙ) ===")
    aq2 = Aquarium(6.0, "#2")
    aq2.add_fish(shark)
    aq2.add_fish(piranha)
    aq2.add_fish(oscar)
    aq2.add_fish(barracuda)
    aq2.add_fish(nemo)      # Відмова: мирну рибку не можна до хижаків

    print("\n" + str(aq2))
    aq2.show_top_3biggest()

    aq = Aquarium(100.0, "Морський риф")

    print("=== ТЕСТ 1: Виклик на порожньому акваріумі ===")
    result = aq.get_top_3biggest()
    print("Результат:", result)
    
    print("\n=== АКВАРІУМ #3 (карантин) характер риб не залежить ===")
    aq3= QuarantineAquarium(10, "Дурка", 5)

if __name__ == "__main__":
    main()