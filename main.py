from modules.lottogame import LottoGame

def play_lotto_game():
    players_count = int(input('Введите количество игроков: '))
    # players_count = 2

    player_names = []
    if players_count>1:
        for i in range(players_count):
            player_name = input(f'Введите имя для {i+1}-го Игрока (или напишите "Bot" для добавления бота): ').capitalize()
            player_names.append(player_name)
    else:
        player_name = input('Введите имя для Игрока (или напишите "Bot" для добавления бота): ').capitalize()
        player_names.append(player_name)

    game = LottoGame(player_names, kegs_count=90)
    game.print_welcome()
    input('Введите Enter чтобы продолжить ')

    while not game.is_over():
        pulled_keg_number = game.pull_keg_from_bag()
        game.print_player_cards()
        game.play_round(pulled_keg_number)
        if not game.is_over():
            input('Введите Enter чтобы продолжить ')
        print()
    print(game.endgame_result_text)
    print('Игра окончена')

if __name__ == '__main__':
    play_lotto_game()
