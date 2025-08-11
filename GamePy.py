def lcg(seed, modulus=2**32, a=1664525, c=1013904223, n=1):
    state = seed
    random_numbers = []
    for _ in range(n):
        state = (a * state + c) % modulus
        random_numbers.append(state / modulus)
    return random_numbers if n > 1 else random_numbers[0]

seed = 12345

def log(message):
    print(message)
    with open("game_log.txt", "a", encoding="utf-8") as file:
        file.write(message + "\n")

def start_game():
    log("Добро пожаловать в таинственный лес!")
    log("Вы отправляетесь на поиски древнего артефакта, который, по легенде, приносит неограниченные силы.")
    log("Но будьте осторожны, лес полон загадок и опасностей.")

def choose_path():
    log("Вы стоите на распутье: налево ведет узкая тропинка, направо - широкая дорога, а прямо - темный лес.")
    path = input("Куда вы пойдете? (налево/направо/прямо): ").lower()
    log(f"Игрок выбрал путь: {path}")
    return path

def encounter_creature(inventory, defeated_creatures, rng_seed):
    creatures = ["волк", "гоблин", "тролль", "дракон", "колдун"]
    rng_seed, rand_idx = next_rng(rng_seed)
    creature = creatures[int(rand_idx * len(creatures))]
    log(f"Вы встречаете {creature}. Он может помочь вам, но может и навредить.")
    action = input("Что вы сделаете? (поговорить/сразиться/игнорировать): ").lower()
    log(f"Игрок выбрал действие: {action}")

    if action == "сразиться":
        log("\nВаш инвентарь:")
        for item, quantity in inventory.items():
            log(f"{item}: {quantity}")
        use_item = input("\nКаким предметом вы будете обороняться? ").lower()
        log(f"Игрок использует предмет: {use_item}")

        if use_item in inventory and inventory[use_item] > 0:
            inventory[use_item] -= 1
            if use_item == "меч":
                log(f"Вы использовали меч и победили {creature}!")
                defeated_creatures[creature] = defeated_creatures.get(creature, 0) + 1
                return True, rng_seed
            elif use_item == "зелье":
                log(f"Вы использовали зелье и исцелили себя, но {creature} остается.")
                return False, rng_seed
            elif use_item == "факел":
                log(f"Вы использовали факел и отпугнули {creature}!")
                defeated_creatures[creature] = defeated_creatures.get(creature, 0) + 1
                return True, rng_seed
            else:
                log("Этот предмет не помог вам в бою.")
                return False, rng_seed
        else:
            log("У вас нет этого предмета или он закончился.")
            return False, rng_seed
    elif action == "поговорить":
        log(f"{creature} оказывается добрым духом леса и помогает вам найти путь.")
        inventory["амулет"] = 1
        return True, rng_seed
    else:
        log(f"Вы игнорируете {creature} и продолжаете свой путь.")
        return False, rng_seed

def find_artifact():
    log("Вы наконец-то находите древний артефакт, сверкающий в полумраке.")
    action = input("Возьмете его? (да/нет): ").lower()
    log(f"Игрок выбрал: {action}")
    return action

def explore_forest():
    log("Вы углубляетесь в темный лес и видите несколько возможных путей.")
    path = input("Выберите путь: (река/пещера/долина/болото): ").lower()
    log(f"Игрок выбрал путь: {path}")
    return path

def final_choice():
    log("Возле артефакта вы видите три пути: один ведет в безопасное место, другой в неизвестность, третий назад в лес.")
    path = input("Какой путь вы выберете? (безопасный/неизвестность/лес): ").lower()
    log(f"Игрок выбрал путь: {path}")
    return path

def meet_wise_hermit(inventory):
    log("Вы встречаете мудрого отшельника. Он может научить вас древнему искусству или дать ценный предмет.")
    choice = input("Что вы выберете? (наука/предмет): ").lower()
    log(f"Игрок выбрал: {choice}")

    if choice == "наука":
        log("Отшельник учит вас древнему искусству. Вы получаете способность лечить себя.")
        inventory["способность исцеления"] = 1
    else:
        log("Отшельник дает вам древний амулет, защищающий от зла.")
        inventory["древний амулет"] = 1

def random_event(inventory, status, treasures, defeated_creatures, rng_seed):
    events = ["вы нашли сундук с сокровищами", "вас атакует бандит", "вы встретили странного старца"]
    rng_seed, rand_idx = next_rng(rng_seed)
    event = events[int(rand_idx * len(events))]
    log(f"Случайное событие: {event}")

    if event == "вы нашли сундук с сокровищами":
        treasure = ["золото", "драгоценный камень", "магический свиток"]
        rng_seed, rand_idx = next_rng(rng_seed)
        found_item = treasure[int(rand_idx * len(treasure))]
        log(f"Вы нашли {found_item}!")
        if found_item == "золото":
            treasures.append((found_item, 100))
        elif found_item == "драгоценный камень":
            treasures.append((found_item, 200))
        else:
            treasures.append((found_item, 50))
    elif event == "вас атакует бандит":
        if "меч" in inventory and inventory["меч"] > 0:
            log("Вы используете меч и побеждаете бандита.")
            inventory["меч"] -= 1
            defeated_creatures["бандит"] = defeated_creatures.get("бандит", 0) + 1
        else:
            log("У вас нет оружия, чтобы защититься. Вы теряете здоровье.")
            status["здоровье"] -= 20
    elif event == "вы встретили странного старца":
        log("Старец предлагает вам выбор: мудрость или богатство.")
        choice = input("Что вы выберете? (мудрость/богатство): ").lower()
        log(f"Игрок выбрал: {choice}")
        if choice == "мудрость":
            log("Старец обучает вас древнему заклинанию.")
            inventory["древнее заклинание"] = 1
        else:
            log("Старец дает вам мешочек с золотом.")
            treasures.append(("золото", 50))

    return rng_seed

def search_area(treasures, rng_seed):
    log("Вы решаете осмотреться вокруг и найти что-то ценное.")
    rare_items = {
        "древний меч": 300,
        "магический амулет": 150,
        "редкий кристалл": 250
    }
    rng_seed, rand_idx = next_rng(rng_seed)
    found_item, value = list(rare_items.items())[int(rand_idx * len(rare_items))]
    log(f"Вы нашли {found_item} стоимостью {value} монет!")
    treasures.append((found_item, value))
    return rng_seed

def use_treasure(treasures):
    if treasures:
        log("\nВаши сокровища:")
        for i, (item, value) in enumerate(treasures):
            log(f"{i + 1}. {item} стоимостью {value} монет")

        choice = input("Выберите сокровище, которое хотите использовать (введите номер или 'нет'): ").lower()
        log(f"Игрок выбрал: {choice}")
        if choice != 'нет':
            index = int(choice) - 1
            if 0 <= index < len(treasures):
                used_item = treasures.pop(index)
                log(f"Вы использовали {used_item[0]} стоимостью {used_item[1]} монет.")

def next_rng(seed):
    new_seed = lcg(seed)
    return new_seed, new_seed

def main():
    inventory = {"зелье": 2, "меч": 1, "факел": 1}
    status = {"здоровье": 100, "энергия": 100}
    treasures = []
    defeated_creatures = {}
    rng_seed = seed

    start_game()

    while status["здоровье"] > 0 and status["энергия"] > 0:
        path = choose_path()

        if path == "налево":
            meet_wise_hermit(inventory)
        elif path == "направо":
            defeated, rng_seed = encounter_creature(inventory, defeated_creatures, rng_seed)
            if not defeated:
                log("Вы не смогли победить существо и теряете здоровье.")
                status["здоровье"] -= 20
        elif path == "прямо":
            sub_path = explore_forest()
            if sub_path == "река":
                log("Вы идете к реке и находите место для отдыха. Вы восстанавливаете энергию.")
                status["энергия"] += 20
                if status["энергия"] > 100:
                    status["энергия"] = 100
            elif sub_path == "пещера":
                log("Вы находите пещеру с древними надписями. Возможно, здесь что-то спрятано.")
                inventory["древний свиток"] = 1
            elif sub_path == "долина":
                log("Вы идете в долину и находите волшебные ягоды. Они восстанавливают здоровье.")
                status["здоровье"] += 20
                if status["здоровье"] > 100:
                    status["здоровье"] = 100
            elif sub_path == "болото":
                log("Вы попадаете в болото и встречаете древнего стража. Вам нужно сразиться с ним.")
                defeated, rng_seed = encounter_creature(inventory, defeated_creatures, rng_seed)
                if defeated:
                    log("Вы победили стража и нашли ценный артефакт!")
                    inventory["древний артефакт"] = 1
                else:
                    log("Вы пострадали в битве и теряете немного здоровья.")
                    status["здоровье"] -= 20
            else:
                log("Вы не нашли ничего полезного.")

        else:
            log("Вы решаете не идти никуда и остаетесь на месте.")
            log("К сожалению, вас настигают лесные духи, и вы теряете свой шанс.")
            return

        rng_seed = search_area(treasures, rng_seed)
        rng_seed = random_event(inventory, status, treasures, defeated_creatures, rng_seed)
        use_treasure(treasures)

        action = find_artifact()

        if action == "да":
            log("Вы берете артефакт и чувствуете прилив силы.")
            status["энергия"] = 100
            path = final_choice()

            if path == "безопасный":
                log("Вы выбираете безопасный путь и благополучно покидаете лес с артефактом.")
                log("Концовка 1: Победа! Вы стали могущественным магом.")
                break
            elif path == "неизвестность":
                log("Вы выбираете путь в неизвестность и исчезаете в тумане.")
                log("Концовка 2: Тайна. Никто не знает, что с вами стало.")
                break
            else:
                log("Вы решаете вернуться в лес, чтобы исследовать его дальше.")
                log("Концовка 3: Исследователь. Ваши приключения продолжаются.")
                continue

        else:
            log("Вы решаете не брать артефакт и покидаете лес.")
            log("Концовка 4: Отказ. Вы вернулись домой ни с чем, но целы и невредимы.")
            break

    if status["здоровье"] <= 0:
        log("Ваше здоровье закончилось. Вы не смогли продолжить путешествие.")
        log("Концовка: Проигрыш. Вы погибли в лесу.")

    log("\nВаш инвентарь:")
    for item, quantity in inventory.items():
        log(f"{item}: {quantity}")

    log("\nНайденные редкие предметы:")
    total_value = 0
    for item, value in treasures:
        log(f"{item}: {value} монет")
        total_value += value

    log(f"\nОбщая стоимость найденных предметов: {total_value} монет")

    log("\nВаши статусы:")
    for stat, value in status.items():
        log(f"{stat}: {value}")

    log("\nПобежденные монстры:")
    for creature, count in defeated_creatures.items():
        log(f"{creature}: {count}")

if __name__ == "__main__":
    main()
