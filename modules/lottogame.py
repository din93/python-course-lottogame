import random

class KegsBag():
    def __init__(self, kegs_count=90):
        if kegs_count<15:
            raise Exception('Бочонков должно быть не меньше 15-ти!')
        self.kegs = list(range(1, kegs_count+1))
        random.shuffle(self.kegs)
    
    def pull_keg(self):
        return -1 if len(self.kegs)==0 else self.kegs.pop(0)
    
    def count(self):
        return len(self.kegs)

class LottoCard():
    def __init__(self, kegs_count=90, row_length=9):
        if kegs_count<15:
            raise Exception('Бочонков должно быть не меньше 15-ти!')
        self.ROW_LENGTH = row_length
        keg_numbers = []
        while len(set(keg_numbers))<15:
            number = random.randint(1, kegs_count)
            keg_numbers.append(number) if number not in keg_numbers else None
        self.keg_numbers = keg_numbers
        card_rows = [
            keg_numbers[0:5],
            keg_numbers[5:10],
            keg_numbers[10:15]
        ]
        # Сортировка строк карточки и добавление пустых полей
        for row in card_rows:
            row.sort()
            while len(row)<row_length:
                insert_index = random.randint(0, len(row))
                row.insert(insert_index, ' ')
        self.card_rows = card_rows

    def show_card(self):
        ROW_LENGTH = self.ROW_LENGTH
        divider = '-'*(ROW_LENGTH*2 + ROW_LENGTH-1)
        card_result = divider+'\n'
        for row in self.card_rows:
            for field in row:
                if str(field).isnumeric():
                    card_result += f' {field} ' if field<10 else f'{field} '
                else:
                    card_result += f' {field} '
            card_result += '\n'
        card_result += divider
        return card_result

    def has_keg_number(self, keg_number):
        for row in self.card_rows:
            if keg_number in row:
                return True
        return False
    
    def cross_out(self, keg_number):
        for rindex, row in enumerate(self.card_rows):
            if keg_number in row:
                self.card_rows[rindex] = ['-' if field==keg_number else field for field in row]
                self.keg_numbers.remove(keg_number)
                return True
        return False

class LottoPlayer():
    def __init__(self, name, lotto_card, is_bot):
        self.name = name
        self.lotto_card = lotto_card
        self.is_bot = is_bot

class LottoGame():
    def __init__(self, player_names, kegs_count=90):
        self.kegs_count = kegs_count
        self.kegs_bag = KegsBag(kegs_count=kegs_count)
        self.players = [
            LottoPlayer(player_name, LottoCard(kegs_count=self.kegs_count), player_name.lower().startswith('bot'))
            for player_name in player_names
        ]
        self.players_in_game = self.players[:]
        self.winner = None
        self.stalemate_finishers = None
        self.bot_stalemate_finishers = None
        self.endgame_result_text = None

    def is_over(self):
        return any([self.winner, self.stalemate_finishers, self.bot_stalemate_finishers, self.endgame_result_text])

    def print_welcome(self):
        print()
        print('**** Добро пожаловать в Lotto Game! ****')
        print('Правила таковы:')
        print(f"  Есть мешок с бочонками, в них числа (от 1-го до {self.kegs_count})")
        print(f"  У каждого игрока есть карточки с {len(self.players[0].lotto_card.keg_numbers)} числами")
        print("  В каждом раунде достается бочонок с числом, игрокам положено вычеркнуть цифру если она есть в карточке")
        print("  Тот игрок, кто решит вычеркнуть число которого нет в его карточке, выбывает из игры")
        print("  Тот игрок, кто решит не вычеркнуть число которое есть в его карточке, выбывает из игры")
        print("  Тот игрок, кто вычеркнет все числа из карточки первым, либо останется последним в коллективной игре, выигрывает")
        print()

    def print_player_cards(self):
        for player in self.players_in_game:
            print(f'Карточка игрока {player.name}:')
            print(player.lotto_card.show_card())

    def pull_keg_from_bag(self):
        return self.kegs_bag.pull_keg()

    def update_game_state(self, pulled_keg_number):
        if len(self.players_in_game)==0:
            self.endgame_result_text = 'Нет победивших'
        if len(self.players)>1 and len(self.players_in_game)==1:
            self.winner = self.players_in_game[0]
        empty_players = [player for player in self.players_in_game if not len(player.lotto_card.keg_numbers)]
        if len(empty_players)==1:
            self.winner = empty_players[0]
        elif len(empty_players)>1:
            self.stalemate_finishers = empty_players
        if pulled_keg_number==-1:
            real_players_in_game = list(filter(lambda player: not player.is_bot, self.players_in_game))
            bots_in_game = list(filter(lambda player: player.is_bot, self.players_in_game))
            if len(real_players_in_game)==1:
                self.winner = real_players_in_game[0]
            elif len(real_players_in_game)>1:
                self.stalemate_finishers = real_players_in_game
            elif len(bots_in_game)==1:
                self.winner = bots_in_game[0]
            elif len(bots_in_game)>1:
                self.bot_stalemate_finishers = self.players_in_game
        if self.winner:
            self.endgame_result_text = f"Победил игрок {self.winner.name}!!!"
        elif self.stalemate_finishers:
            self.endgame_result_text = f'Ничья между {", ".join([player.name for player in self.stalemate_finishers])}'
        elif self.bot_stalemate_finishers:
            self.endgame_result_text = f'Ничья между ботами {", ".join([player.name for player in self.bot_stalemate_finishers])}'

    def make_move(self, player, player_choice, pulled_keg_number):
        result_text = ''
        if player_choice.lower() == 'y':
            if not player.lotto_card.cross_out(pulled_keg_number):
                result_text = f'{player.name} попытался зачеркнуть число {pulled_keg_number}, которого нет в карточке!\nИгра окончена для {player.name}.'
                self.players_in_game = list(filter(lambda x: x is not player, self.players_in_game))
            else:
                result_text = f'{player.name} вычеркнул число {pulled_keg_number} из своей карточки.'
        elif player_choice.lower() == 'n':
            if player.lotto_card.has_keg_number(pulled_keg_number):
                result_text = f'{player.name} не вычеркнул число {pulled_keg_number}, записанное в карточке!\nИгра окончена для {player.name}.'
                self.players_in_game = list(filter(lambda x: x is not player, self.players_in_game))
            else:
                result_text = f'{player.name} не вычеркнул число {pulled_keg_number}, которого и не было в карточке.'
        else:
            raise Exception('Некорректный ответ')

        return result_text

    def play_round(self, pulled_keg_number):
        self.update_game_state(pulled_keg_number)
        if self.is_over():
            return

        print(f'Новый бочонок: {pulled_keg_number} (осталось {self.kegs_bag.count()})\n')

        for player in self.players_in_game:
            if player.is_bot:
                player_choice = 'y' if player.lotto_card.has_keg_number(pulled_keg_number) else 'n'
                # player_choice = 'y' if random.random()>0.5 else 'n'
            else:
                player_choice =''
                while player_choice.lower() not in ['y', 'n']:
                    player_choice = input(f'{player.name}, зачеркнуть цифру {pulled_keg_number} из вашей карточки? (y/n): ')
            result_text = self.make_move(player, player_choice, pulled_keg_number)
            print(result_text)
            print()
