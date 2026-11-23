from abc import ABC, abstractmethod

# Спільний абстрактний базовий клас
class AquaticEntity(ABC):
    @abstractmethod
    def __str__(self):
        pass
#клас риб
class Fish(AquaticEntity):
    def __init__(self, name, age, species, size, prefferedfood, isAggressive, neededspace):
        self.name = name                         
        self.age = age                           
        self.__species = species                
        self.size = size                         
        self.prefferedfood = prefferedfood       
        self.isAggressive = isAggressive
        self.neededspace = neededspace           

    #гетер виду риби
    @property
    def species(self):
        return self.__species
    
    #сеттер виду риби
    @species.setter
    def species(self, new_species):
        if not isinstance(new_species, str) or not new_species.strip():
            raise ValueError("Вид рибки має бути непорожнім рядком!")
        self.__species = new_species.strip()
    #виводимо характеристики рибки
    def __str__(self):
        temper = "Агресивна" if self.isAggressive else "Мирна"
        return (
            f"{self.__species} '{self.name}' "
            f"(вік: {self.age} р., розмір: {self.size} см, {temper}, треба {self.neededspace} м³)"
        )
    
    #базові технічні характеристики
    def __repr__(self):
        return f"Fish('{self.name}', '{self.__species}', {self.size} см)"
    

    def __del__(self):
        pass


class Aquarium(AquaticEntity):
    #ініціюєм акваріум
    def __init__(self, totalvol, title):
        if not isinstance(totalvol, (int, float)) or totalvol <= 0:
            raise ValueError("Об'єм акваріума має бути більшим за 0!")
        self.__totalvol = totalvol  #заприватили об'єм
        self.freespace = totalvol  
        self.fishes = []             
        self.title = title 

    #геттер об'єму      
    @property
    def totalvol(self):
        return self.__totalvol
    
    def add_fish(self, fish):

        if fish.neededspace > self.freespace:
            print(
                f"[Відмова -> {self.title}] Замало місця для '{fish.name}'! "
                f"Треба {fish.neededspace} м³, вільно тільки {self.freespace} м³."
            )
            return False

        if len(self.fishes) > 0:
            aq_temper = self.fishes[0].isAggressive
            if aq_temper != fish.isAggressive:
                curtemp = "агресивну" if fish.isAggressive else "мирну"
                print(
                    f"[Відмова -> {self.title}] Не можна підселити {curtemp} рибу "
                    f"'{fish.name}' до риб протилежних за характером!"
                )
                return False

        self.fishes.append(fish)
        self.freespace = round(self.freespace - fish.neededspace, 2)
        print(
            f"[Успіх -> {self.title}] Рибку '{fish.name}' додано! "
            f"Вільно місця: {self.freespace} м³."
        )
        return True

    #top 3 найбільші
    def get_top_3biggest(self):
        """Повертає 3 найбільші риби за розміром."""
        if not self.fishes:
            print(f"В акваріумі {self.title} ще немає рибок!")
            return []
        sorted_fishes = sorted(self.fishes, key=lambda f: f.size, reverse=True)
        return sorted_fishes[:3]

    def show_top_3biggest(self):
        print(f"\n--- Топ-3 найбільших риб в акваріумі {self.title} ---")
        top_fishes = self.get_top_3biggest()
        for i, fish in enumerate(top_fishes, start=1):
            print(f"{i}. {fish}")

    def __str__(self):
        return (
            f"Акваріум {self.title}: загальний об'єм {self.__totalvol} м³, "
            f"вільно {self.freespace} м³, рибок: {len(self.fishes)}"
        )

    def __del__(self):
        pass


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

    print("\n=== перевіряємо приватні поля та сетер/гетер через декоратор ===")
    print("Вид рибки (через @property):", nemo.species)
    nemo.species = "Амфіпріон (Риба-клоун)"
    print("Оновлений вид:", nemo.species)
    print("Розмір (публічне поле):", nemo.size, "см")

    print("\n=== АКВАРІУМ #1 (МИРНИЙ) ===")
    aq1 = Aquarium(1.0, "#1")
    print("Об'єм акваріума:", aq1.totalvol, "м³")

    aq1.add_fish(angel)
    aq1.add_fish(dory)
    aq1.add_fish(nemo)
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


if __name__ == "__main__":
    main()

#custom decorator, через супери імплементувати add_fish 