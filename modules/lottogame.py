import random

class KegsBag():
    def __init__(self, kegs_count=90):
        if kegs_count<15:
            raise ValueError('Бочонков должно быть не меньше 15-ти!')
        self.kegs = list(range(1, kegs_count+1))
        random.shuffle(self.kegs)
    
    def pull_keg(self):
        return -1 if len(self.kegs)==0 else self.kegs.pop(0)
    
    def __len__(self):
        return len(self.kegs)

    def __str__(self):
        return f'Bag of {len(self.kegs)} kegs'

    def __eq__(self, other_kegsbag):
        return self.kegs == other_kegsbag.kegs

    def __getitem__(self, index):
        return self.kegs[index]

    def __contains__(self, kegnumber):
        return kegnumber in self.kegs

class LottoCard():
    def __init__(self, kegs_count=90, row_length=9):
        if kegs_count<15:
            raise ValueError('Бочонков должно быть не меньше 15-ти!')
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

    def __len__(self):
        return len(self.keg_numbers)

    def __str__(self):
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

    def __eq__(self, another):
        return self.card_rows == another.card_rows

    def __getitem__(self, index):
        return self.card_rows[index]

    def __contains__(self, kegnumber):
        return kegnumber in self.keg_numbers
    
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

    def __str__(self):
        return f"{'Бот' if self.is_bot else 'Игрок'} {self.name}\n{str(self.lotto_card)}"

    def __eq__(self, another):
        return self.is_bot==another.is_bot and self.name==another.name and self.lotto_card==another.lotto_card

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

    def get_welcome_text(self):
        text = '\n'
        text+='**** Добро пожаловать в Lotto Game! ****\n'
        text+='Правила таковы:\n'
        text+=f"  Есть мешок с бочонками, в них числа (от 1-го до {self.kegs_count})\n"
        text+=f"  У каждого игрока есть карточки с {len(self.players[0].lotto_card.keg_numbers)} числами\n"
        text+="  В каждом раунде достается бочонок с числом, игрокам положено вычеркнуть цифру если она есть в карточке\n"
        text+="  Тот игрок, кто решит вычеркнуть число которого нет в его карточке, выбывает из игры\n"
        text+="  Тот игрок, кто решит не вычеркнуть число которое есть в его карточке, выбывает из игры\n"
        text+="  Тот игрок, кто вычеркнет все числа из карточки первым, либо останется последним в коллективной игре, выигрывает\n"
        return text

    def get_player_cards_text(self):
        text = '\n'
        for player in self.players_in_game:
            text+=f'Карточка игрока {player.name}:\n'
            text+=str(player.lotto_card)+'\n'
        return text

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
            if pulled_keg_number in player.lotto_card:
                result_text = f'{player.name} не вычеркнул число {pulled_keg_number}, записанное в карточке!\nИгра окончена для {player.name}.'
                self.players_in_game = list(filter(lambda x: x is not player, self.players_in_game))
            else:
                result_text = f'{player.name} не вычеркнул число {pulled_keg_number}, которого и не было в карточке.'
        else:
            raise ValueError('Некорректный ответ')

        return result_text
    
    def __str__(self):
        title_text = f"Игра Лото на {self.kegs_count} бочонков ({len(self.kegs_bag)} осталось)"
        players_text = f"{len(self.players)} игроков: {', '.join([player.name for player in self.players])}"
        gamestate_text = f"В игре сейчас {len(self.players_in_game)} игроков: {', '.join([player.name for player in self.players_in_game])}"
        if self.endgame_result_text:
            gamestate_text = self.endgame_result_text
        return f"{title_text}\n{players_text}\n{gamestate_text}"

    def __eq__(self, another):
        return self.players==another.players and self.players_in_game==another.players_in_game and self.kegs_count==another.kegs_count and self.kegs_bag==another.kegs_bag
