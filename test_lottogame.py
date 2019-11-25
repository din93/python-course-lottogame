from modules.lottogame import LottoGame, KegsBag, LottoPlayer, LottoCard 
import os, shutil

def test_kegsbag():
    kegs_bag = KegsBag()
    kegs_initial = kegs_bag.kegs[:]
    pulled_keg = kegs_bag.pull_keg()
    assert pulled_keg == kegs_initial[0]
    assert kegs_bag.kegs == kegs_initial[1:]
    assert kegs_bag.count() == 89
    for _ in range(90):
        kegs_bag.pull_keg()
    assert kegs_bag.pull_keg() == -1
    try:
        KegsBag(kegs_count=10)
    except Exception:
        assert True
    else:
        assert False

def test_lottocard():
    lotto_card = LottoCard()
    keg_numbers_initial = lotto_card.keg_numbers[:]
    lotto_card.cross_out(keg_numbers_initial[0])
    assert lotto_card.keg_numbers == keg_numbers_initial[1:]
    assert lotto_card.has_keg_number(keg_numbers_initial[0]) == False
    assert lotto_card.ROW_LENGTH == 9
    assert not lotto_card.cross_out(142)
    try:
        LottoCard(kegs_count=10)
    except Exception:
        assert True
    else:
        assert False

def test_lottoplayer():
    lotto_card = LottoCard()
    lotto_player = LottoPlayer('TestPlayer', lotto_card, is_bot=True)
    assert lotto_player.name == 'TestPlayer'
    assert lotto_player.lotto_card == lotto_card
    assert lotto_player.is_bot == True

def test_lottogame():
    lotto_game = LottoGame(['player1', 'player2'])

    assert lotto_game.winner == None
    assert lotto_game.stalemate_finishers == None
    assert lotto_game.bot_stalemate_finishers == None
    assert lotto_game.endgame_result_text == None
    assert lotto_game.is_over() == False

    kegs_initial = lotto_game.kegs_bag.kegs[:]
    pulled_keg_number = lotto_game.kegs_bag.pull_keg()
    assert pulled_keg_number == kegs_initial[0]
    assert lotto_game.kegs_bag.kegs == kegs_initial[1:]
    assert lotto_game.kegs_bag.count() == 89

    player1 = lotto_game.players[0]
    assert player1.name == 'player1'
    wrong_choice = 'n' if player1.lotto_card.has_keg_number(pulled_keg_number) else 'y'
    lotto_game.make_move(player1, wrong_choice, pulled_keg_number)
    assert player1 not in lotto_game.players_in_game

    player2 = lotto_game.players[1]
    assert player2.name == 'player2'
    right_choice = 'y' if player2.lotto_card.has_keg_number(pulled_keg_number) else 'n'
    lotto_game.make_move(player2, right_choice, pulled_keg_number)
    assert player2 in lotto_game.players_in_game

    lotto_game.update_game_state(lotto_game.kegs_bag.pull_keg())
    assert lotto_game.winner == player2
    assert lotto_game.endgame_result_text == 'Победил игрок player2!!!'

    lotto_game2 = LottoGame(['bot1', 'bot2'])
    while not lotto_game2.is_over():
        pulled_keg_number = lotto_game2.pull_keg_from_bag()
        lotto_game2.play_round(pulled_keg_number)
    assert lotto_game2.endgame_result_text
