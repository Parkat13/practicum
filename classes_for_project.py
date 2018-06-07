# -*- coding: utf-8 -*-
import random
flag_buy_fish = 0
flag_buy_forage = 0
clean_queue = []
fish = ['Карп', 'Буффало', 'Сом', 'Угорь', 'Щука', 'Форель']
coefficients_of_fish = {}
coefficients_of_fish['Карп'] = [0.95, 0.85, 0.15]
coefficients_of_fish['Буффало'] = [0.65, 0.65, 0.1]
coefficients_of_fish['Сом'] = [0.9, 0.9, 0.3]
coefficients_of_fish['Угорь'] = [0.8, 0.75, 0.2]
coefficients_of_fish['Щука'] = [0.7, 0.9, 0.1]
coefficients_of_fish['Форель'] = [0.5, 0.8, 0.2]


class game_world:
    def __init__(self, capital, n_pond, ponds, duration, contract_fish, contract_forage, forfeit, cost_fish, cost_forage, percent):
        self.cost_fish, self.cost_forage, self.percent = int(cost_fish), int(cost_forage), int(percent)
        self.owner = owner(capital, n_pond, ponds, duration, contract_fish, contract_forage, forfeit)
        self.win_game, self.end_of_game, self.time, self.factor = 0, 0, 1, 0

    def update(self):
        if self.time == self.owner.duration:
            self.end_of_game = 1
            if self.owner.capital >= 0:
                self.win_game = 1
        else:
            rand = random.randint(0, 100)
            if rand <= self.percent:
                self.factor = 1
            else:
                self.factor = 0
            self.owner.update_contract(self.time, self.factor, self.percent)
            if self.owner.end:
                self.end_of_game = 1
        self.time += 1

    def buy_fish(self, fish):
        global flag_buy_fish
        cost = fish * self.cost_fish
        if self.owner.capital >= cost:
            self.owner.capital -= cost
            flag_buy_fish = 0
            min_fish = 1000
            min_pond = -1
            for i in range(self.owner.n_pond):
                if (self.owner.ponds[i].population_young + self.owner.ponds[i].population_adults) < min_fish and self.owner.ponds[i].status != 'Очистка':
                    min_fish = self.owner.ponds[i].population_young + self.owner.ponds[i].population_adults
                    min_pond = i
            self.owner.ponds[min_pond].population_young += fish
        else:
            flag_buy_fish = 1

    def buy_forage(self, forage):
        global flag_buy_forage
        cost = forage * self.cost_forage
        if self.owner.capital >= cost:
            self.owner.capital -= cost
            flag_buy_forage = 0
            self.owner.forage += forage
        else:
            flag_buy_forage = 1


class pond:
    def __init__(self, status, population):
        self.status, self.population_young, self.population_adults = status, population, 0
        self.clean, self.percent_of_clean = 0, 0

    def update(self, factor, percent):
        global coefficients_of_fish, fish
        rand = random.randint(0, 100)
        if rand <= self.percent_of_clean:
            self.clean = 1
        if self.clean == 1 and self.population_adults ==0 and self.population_young == 0:
            self.status = 'Очистка'
            self.clean = 0
            self.percent_of_clean = 0
        else:
            if self.status == 'Очистка':
                rand = random.randint(0, len(fish) - 1)
                self.status = fish[rand]
            else:
                self.percent_of_clean += 30
                adults = self.population_adults
                young = self.population_young
                self.population_young = (coefficients_of_fish[self.status][0] * adults)//1
                self.population_adults = (coefficients_of_fish[self.status][1] * young + (1 - coefficients_of_fish[self.status][2]) * adults)//1
                if factor:
                    self.population_adults -= (percent * self.population_adults)//100
                    self.population_young -= (percent * self.population_young)//100


class owner:
    def __init__(self, capital, n_pond, ponds, duration, cost_fish, cost_forage, forfeit):
        self.n_pond, self.capital = int(n_pond), int(capital)
        self.ponds = list(pond(ponds[i][0], ponds[i][1]) for i in range(int(n_pond)))
        self.forage = 0.0
        self.duration = int(duration)
        self.end = 0
        self.contract_forage, self.contract_fish, self.forfeit = cost_forage, cost_fish, int(forfeit)

    def update_contract(self, time, factor, percent):
        global clean_queue
        contract_period = (time - 1)//3
        adults_fish = 0
        contract_fish = self.contract_fish[contract_period][0]
        all_fish = 0
        for i in range(self.n_pond):
            adults_fish += self.ponds[i].population_adults
            all_fish += self.ponds[i].population_young + self.ponds[i].population_adults
        if contract_fish > all_fish:
            for i in range(self.n_pond):
                self.ponds[i].population_young = 0
                self.ponds[i].population_adults = 0
            contract_fish -= all_fish
            self.capital += all_fish * self.contract_fish[contract_period][1]
            self.capital -= contract_fish * self.forfeit
            if self.capital < 0:
                self.end = 1
        else:
            while (contract_fish > 0) and (len(clean_queue) > 0):
                if self.ponds[clean_queue[0]].population_adults < contract_fish:
                    contract_fish -= self.ponds[clean_queue[0]].population_adults
                    self.ponds[clean_queue[0]].population_adults = 0
                else:
                    self.ponds[clean_queue[0]].population_adults -= contract_fish
                    contract_fish = 0
                    break
                if self.ponds[clean_queue[0]].population_young < contract_fish:
                    contract_fish -= self.ponds[clean_queue[0]].population_young
                    self.ponds[clean_queue[0]].population_young = 0
                else:
                    self.ponds[clean_queue[0]].population_young -= contract_fish
                    contract_fish = 0
                    break
                clean_queue = clean_queue[1:]
            if contract_fish > 0:
                if adults_fish >= contract_fish:
                    self.update_adults_fish(adults_fish, contract_fish)
                else:
                    contract_fish -= adults_fish
                    self.update_young_fish(contract_fish)
            self.capital += self.contract_fish[contract_period][0] * self.contract_fish[contract_period][1]
        self.capital -= self.contract_forage[contract_period][0] * self.contract_forage[contract_period][1]
        if self.capital < 0:
            self.end = 1
        else:
            self.forage += self.contract_forage[contract_period][0]
        self.update_ponds(factor, percent)

    def update_adults_fish(self, adults_fish, contract_fish):
        max, max_n = 0, 0
        for i in range(self.n_pond):
            if adults_fish == 0:
                now_fish = 0
            else:
                now_fish = ((self.ponds[i].population_adults / adults_fish) * contract_fish) // 1
            self.ponds[i].population_adults -= now_fish
            contract_fish -= now_fish
            if self.ponds[i].population_adults > max:
                max = self.ponds[i].population_adults
                max_n = 0
            elif self.ponds[i].population_adults == max:
                max_n += 1
        if contract_fish > 0:
            ok = 0
            if max_n < contract_fish:
                ok = 1
            for i in range(self.n_pond):
                if self.ponds[i].population_adults == max:
                    if ok:
                        self.ponds[i].population_adults -= 2
                        contract_fish -= 2
                        max_n -= 1
                        if max_n >= contract_fish:
                            ok = 0
                    else:
                        if contract_fish > 0:
                            self.ponds[i].population_adults -= 1
                            contract_fish -= 1
                        else:
                            break

    def update_young_fish(self, contract_fish):
        young_fish = 0
        for i in range(self.n_pond):
            self.ponds[i].population_adults = 0
            young_fish += self.ponds[i].population_young
        max, max_n = 0, 0
        for i in range(self.n_pond):
            if young_fish == 0:
                now_fish = 0
            else:
                now_fish = ((self.ponds[i].population_young / young_fish) * contract_fish) // 1
            self.ponds[i].population_young -= now_fish
            contract_fish -= now_fish
            if self.ponds[i].population_young > max:
                max = self.ponds[i].population_young
                max_n = 0
            elif self.ponds[i].population_young == max:
                max_n += 1
        if contract_fish > 0:
            ok = 0
            if max_n < contract_fish:
                ok = 1
            for i in range(self.n_pond):
                if self.ponds[i].population_young == max:
                    if ok:
                        self.ponds[i].population_young -= 2
                        contract_fish -= 2
                        max_n -= 1
                        if max_n >= contract_fish:
                            ok = 0
                    else:
                        if contract_fish > 0:
                            self.ponds[i].population_young -= 1
                            contract_fish -= 1
                        else:
                            break

    def update_ponds(self, factor, percent):
        global clean_queue
        for i in range(self.n_pond):
            forage_need = self.ponds[i].population_young/2 + self.ponds[i].population_adults
            if float(self.forage) >= forage_need:
                self.forage -= forage_need
            else:
                percent_of_die = self.forage/forage_need
                self.forage = 0
                self.ponds[i].population_adults = (self.ponds[i].population_adults * percent_of_die)//1
                self.ponds[i].population_young = (self.ponds[i].population_young * percent_of_die)//1
            self.ponds[i].update(factor, percent)
            if (self.ponds[i].clean == 1) and not(i in clean_queue):
                clean_queue.append(i)
