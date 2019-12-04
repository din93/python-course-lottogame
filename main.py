from modules.lottogame import LottoGame

IS_MAIN = __name__ == '__main__'

def play_lotto_game(test_players_count=1):
    players_count = int(input('Введите количество игроков: ')) if IS_MAIN else test_players_count
    # players_count = 2

    player_names = []
    if players_count>1:
        for i in range(players_count):
            player_name = input(f'Введите имя для {i+1}-го Игрока (или напишите "Bot" для добавления бота): ').capitalize() if IS_MAIN else f'bot{i}'
            player_names.append(player_name)
    else:
        player_name = input('Введите имя для Игрока (или напишите "Bot" для добавления бота): ').capitalize() if IS_MAIN else f'player'
        player_names.append(player_name)

    game = LottoGame(player_names, kegs_count=90)
    print(game.get_welcome_text())
    input('Введите Enter чтобы продолжить ') if IS_MAIN else None

    while not game.is_over():
        pulled_keg_number = game.pull_keg_from_bag()
        print(game.get_player_cards_text())
        print(f'Новый бочонок: {pulled_keg_number} (осталось {game.kegs_bag.count()})\n')
        for player in game.players_in_game:
            if player.is_bot:
                player_choice = 'y' if player.lotto_card.has_keg_number(pulled_keg_number) else 'n'
                # player_choice = 'y' if random.random()>0.5 else 'n'
            else:
                player_choice = ''
                while player_choice.lower() not in ['y', 'n']:
                    right_choice = 'y' if player.lotto_card.has_keg_number(pulled_keg_number) else 'n'
                    player_choice = input(f'{player.name}, зачеркнуть цифру {pulled_keg_number} из вашей карточки? (y/n): ') if IS_MAIN else right_choice
            result_text = game.make_move(player, player_choice, pulled_keg_number)
            print(result_text)
            print()
        if not game.is_over():
            input('Введите Enter чтобы продолжить ') if IS_MAIN else None
        print()
        game.update_game_state(pulled_keg_number)
        print(game.get_player_cards_text())
    print(game.endgame_result_text)
    print('Игра окончена')

play_lotto_game() if IS_MAIN else None
