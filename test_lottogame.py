from modules.lottogame import LottoGame, KegsBag, LottoPlayer, LottoCard 
import unittest, pytest
from main import play_lotto_game

class TestKegsBag(unittest.TestCase):
    def setUp(self):
        self.kegs_bag = KegsBag()
        self.kegs_initial = self.kegs_bag.kegs[:]
    
    def test_pulling_keg(self):
        pulled_keg = self.kegs_bag.pull_keg()
        self.assertEqual(pulled_keg, self.kegs_initial[0], msg='Получен некорректный номер бочонка')
        self.assertListEqual(self.kegs_bag.kegs, self.kegs_initial[1:], msg='Некорректное изменение содержимого мешка')
        self.assertEqual(len(self.kegs_bag), 89, msg='Некорректное изменение количества элементов в мешке')

    def test_empty_bag(self):
        for _ in range(91):
            self.kegs_bag.pull_keg()
        self.assertEqual(self.kegs_bag.pull_keg(), -1)

    def test_low_kegs_exception(self):
        with self.assertRaises(ValueError):
            KegsBag(kegs_count=10)

    def test_len(self):
        self.assertEqual(len(self.kegs_bag), len(self.kegs_bag.kegs))

    def test_str(self):
        self.assertEqual(str(self.kegs_bag), 'Bag of 90 kegs')
        self.kegs_bag.pull_keg()
        self.assertEqual(str(self.kegs_bag), 'Bag of 89 kegs')

    def test_eq(self):
        another_kegs_bag = KegsBag()
        self.assertNotEqual(self.kegs_bag, another_kegs_bag)
        another_kegs_bag.kegs = self.kegs_bag.kegs
        self.assertEqual(self.kegs_bag, another_kegs_bag)

    def test_getitem(self):
        self.assertEqual(self.kegs_bag[0], self.kegs_bag.kegs[0])
        self.assertEqual(self.kegs_bag[1], self.kegs_bag.kegs[1])
        self.assertEqual(self.kegs_bag[-1], self.kegs_bag.kegs[-1])
        with self.assertRaises(IndexError):
            self.kegs_bag[200]

    def test_contains(self):
        self.assertIn(self.kegs_bag.kegs[0], self.kegs_bag)
        self.assertNotIn(200, self.kegs_bag)

class TestLottoCard():
    def setup(self):
        self.lotto_card = LottoCard()
        self.keg_numbers_initial = self.lotto_card.keg_numbers[:]

    def test_show_card(self):
        card_display_text = str(self.lotto_card)
        assert card_display_text.startswith('----')
        assert card_display_text.endswith('----')

    def test_has_keg_number(self):
        assert 100 not in self.lotto_card
        keg_number_from_card = self.lotto_card.keg_numbers[0]
        assert keg_number_from_card in self.lotto_card

    def test_crossing_out(self):
        self.lotto_card.cross_out(self.keg_numbers_initial[0])
        assert self.lotto_card.keg_numbers == self.keg_numbers_initial[1:]
        assert self.keg_numbers_initial[0] not in self.lotto_card
        assert not self.lotto_card.cross_out(142)

    def test_low_kegs_exception(self):
        with pytest.raises(ValueError):
            LottoCard(kegs_count=10)

    def test_len(self):
        assert len(self.lotto_card) == len(self.lotto_card.keg_numbers)

    def test_str(self):
        assert str(self.lotto_card).startswith('-------')
        assert str(self.lotto_card).endswith('-------')

    def test_eq(self):
        another_lotto_card = LottoCard()
        assert self.lotto_card != another_lotto_card
        another_lotto_card.card_rows = self.lotto_card.card_rows
        assert self.lotto_card == another_lotto_card

    def test_getitem(self):
        assert self.lotto_card[0][0] == self.lotto_card.card_rows[0][0]
        assert self.lotto_card[1][1] == self.lotto_card.card_rows[1][1]
        assert self.lotto_card[-1][-1] == self.lotto_card.card_rows[-1][-1]

    def test_contains(self):
        assert self.lotto_card.keg_numbers[0] in self.lotto_card
        assert self.lotto_card.keg_numbers[-1] in self.lotto_card
        assert 0 not in self.lotto_card
        assert 120 not in self.lotto_card

class TestLottoPlayer(unittest.TestCase):
    def setUp(self):
        self.lotto_card = LottoCard()

    def tearDown(self):
        del(self.lotto_card)

    def test_bot(self):
        lotto_player = LottoPlayer('TestBot', self.lotto_card, is_bot=True)
        self.assertEqual(lotto_player.name, 'TestBot')
        self.assertEqual(lotto_player.lotto_card, self.lotto_card)
        self.assertTrue(lotto_player.is_bot)
    
    def test_player(self):
        lotto_player = LottoPlayer('TestPlayer', self.lotto_card, is_bot=False)
        self.assertEqual(lotto_player.name, 'TestPlayer')
        self.assertEqual(lotto_player.lotto_card, self.lotto_card)
        self.assertFalse(lotto_player.is_bot)

    def test_str(self):
        lotto_bot = LottoPlayer('TestBot', LottoCard(), is_bot=True)
        self.assertTrue(str(lotto_bot).startswith('Бот TestBot\n------------'))
        lotto_player = LottoPlayer('TestPlayer', LottoCard(), is_bot=False)
        self.assertTrue(str(lotto_player).startswith('Игрок TestPlayer\n------------'))

    def test_eq(self):
        lotto_player1 = LottoPlayer('TestPlayer1', LottoCard(), is_bot=False)
        copyof_lotto_player1 = LottoPlayer('TestPlayer1', lotto_player1.lotto_card, is_bot=False)
        self.assertEqual(lotto_player1, copyof_lotto_player1)
        lotto_player2 = LottoPlayer('TestPlayer2', LottoCard(), is_bot=False)
        self.assertNotEqual(lotto_player1, lotto_player2)
        lotto_bot1 = LottoPlayer('TestBot1', LottoCard(), is_bot=True)
        self.assertNotEqual(lotto_player1, lotto_bot1)

class TestLottoGame():
    def setup(self):
        self.lotto_game = LottoGame(['player1', 'player2'])
        self.no_kegs_code_number = -1

    def teardown(self):
        del(self.lotto_game)

    def test_init_game(self):
        assert self.lotto_game.winner == None
        assert self.lotto_game.stalemate_finishers == None
        assert self.lotto_game.bot_stalemate_finishers == None
        assert self.lotto_game.endgame_result_text == None
        assert self.lotto_game.is_over() == False

    def test_str(self):
        assert str(self.lotto_game) == 'Игра Лото на 90 бочонков (90 осталось)\n2 игроков: player1, player2\nВ игре сейчас 2 игроков: player1, player2'
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()
        assert str(self.lotto_game) == 'Игра Лото на 90 бочонков (89 осталось)\n2 игроков: player1, player2\nВ игре сейчас 2 игроков: player1, player2'
        player1 = self.lotto_game.players[0]
        assert player1.name == 'player1', 'Порядок списка игроков не соответствует ожидаемому'
        wrong_choice = 'n' if pulled_keg_number in player1.lotto_card else 'y'
        self.lotto_game.make_move(player1, wrong_choice, pulled_keg_number)
        self.lotto_game.update_game_state(pulled_keg_number)
        assert str(self.lotto_game) == 'Игра Лото на 90 бочонков (89 осталось)\n2 игроков: player1, player2\nПобедил игрок player2!!!'

    def test_eq(self):
        another_lotto_game = LottoGame(['player1', 'player2'])
        assert self.lotto_game != another_lotto_game
        another_lotto_game.kegs_bag = self.lotto_game.kegs_bag
        another_lotto_game.players = self.lotto_game.players
        another_lotto_game.players_in_game = self.lotto_game.players_in_game
        assert self.lotto_game == another_lotto_game

    def test_pulling_keg(self):
        kegs_initial = self.lotto_game.kegs_bag.kegs[:]
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()
        assert pulled_keg_number == kegs_initial[0], 'Некорректно извлечен бочонок'
        assert len(self.lotto_game.kegs_bag) == 89, 'Количество бочонков в мешке не изменилось после извлечения'
        assert self.lotto_game.kegs_bag.kegs == kegs_initial[1:]

    def test_print_game_info(self):
        assert self.lotto_game.get_welcome_text().startswith('\n**** Добро пожаловать в Lotto Game! ****')
        assert self.lotto_game.get_player_cards_text().startswith('\nКарточка игрока ')

    def test_losing_player(self):
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()
        player1 = self.lotto_game.players[0]
        assert player1.name == 'player1', 'Порядок списка игроков не соответствует ожидаемому'
        wrong_choice = 'n' if pulled_keg_number in player1.lotto_card else 'y'
        self.lotto_game.make_move(player1, wrong_choice, pulled_keg_number)
        assert player1 not in self.lotto_game.players_in_game

    def test_wrong_answer(self):
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()
        player1 = self.lotto_game.players[0]
        assert player1.name == 'player1', 'Порядок списка игроков не соответствует ожидаемому'
        wrong_answer = 'abcd'
        with pytest.raises(ValueError):
            self.lotto_game.make_move(player1, wrong_answer, pulled_keg_number)

    def test_keeping_player(self):
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()
        player2 = self.lotto_game.players[1]
        assert player2.name == 'player2', 'Порядок списка игроков не соответствует ожидаемому'
        right_choice = 'y' if pulled_keg_number in player2.lotto_card else 'n'
        self.lotto_game.make_move(player2, right_choice, pulled_keg_number)
        assert player2 in self.lotto_game.players_in_game

    def test_winning_game(self):
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()

        player1 = self.lotto_game.players[0]
        wrong_choice = 'n' if pulled_keg_number in player1.lotto_card else 'y'
        self.lotto_game.make_move(player1, wrong_choice, pulled_keg_number)
        player2 = self.lotto_game.players[1]
        right_choice = 'y' if pulled_keg_number in player2.lotto_card else 'n'
        self.lotto_game.make_move(player2, right_choice, pulled_keg_number)

        self.lotto_game.update_game_state(self.no_kegs_code_number)
        assert self.lotto_game.winner == player2
        assert self.lotto_game.endgame_result_text == 'Победил игрок player2!!!'
        assert self.lotto_game.is_over() == True

    def test_no_winners(self):
        lotto_game = LottoGame(['player1', 'player2'], kegs_count=15)
        pulled_keg_number = lotto_game.pull_keg_from_bag()
        for player in lotto_game.players:
            wrong_choice = 'n' if pulled_keg_number in player.lotto_card else 'y'
            lotto_game.make_move(player, wrong_choice, pulled_keg_number)
        lotto_game.update_game_state(lotto_game.pull_keg_from_bag())
        assert lotto_game.winner == None
        assert lotto_game.endgame_result_text == 'Нет победивших'
        assert lotto_game.is_over() == True

    def test_playing_bots(self):
        lotto_game_bots = LottoGame(['bot1', 'bot2'])
        bot1 = lotto_game_bots.players[0]
        bot2 = lotto_game_bots.players[1]
        while not lotto_game_bots.is_over():
            pulled_keg_number = lotto_game_bots.pull_keg_from_bag()
            lotto_game_bots.make_move(bot1, 'y' if pulled_keg_number in bot1.lotto_card else 'n', pulled_keg_number)
            lotto_game_bots.make_move(bot2, 'y' if pulled_keg_number in bot2.lotto_card else 'n', pulled_keg_number)
            lotto_game_bots.update_game_state(pulled_keg_number)
        assert lotto_game_bots.endgame_result_text

    def test_stalemate_empty_finishers(self):
        player1 = self.lotto_game.players[0]
        player1.lotto_card.keg_numbers = []
        player2 = self.lotto_game.players[1]
        player2.lotto_card.keg_numbers = []
        pulled_keg_number = self.lotto_game.pull_keg_from_bag()
        self.lotto_game.update_game_state(pulled_keg_number)
        assert self.lotto_game.stalemate_finishers

    def test_stalemate_no_kegs_bots(self):
        lotto_game_bots = LottoGame(['bot1', 'bot2', 'bot3'])
        lotto_game_bots.update_game_state(self.no_kegs_code_number)
        assert lotto_game_bots.winner == None
        assert lotto_game_bots.bot_stalemate_finishers == lotto_game_bots.players
        assert lotto_game_bots.is_over() == True

    def test_stalemate_no_kegs_players(self):
        self.lotto_game.update_game_state(self.no_kegs_code_number)
        assert self.lotto_game.winner == None
        assert self.lotto_game.stalemate_finishers == self.lotto_game.players
        assert self.lotto_game.is_over() == True  

    def test_one_player(self):
        lotto_game = LottoGame(['player'])
        player = lotto_game.players[0]
        while not lotto_game.is_over():
            pulled_keg_number = lotto_game.pull_keg_from_bag()
            right_choice = 'y' if pulled_keg_number in player.lotto_card else 'n'
            lotto_game.make_move(player, right_choice, pulled_keg_number)
            lotto_game.update_game_state(pulled_keg_number)
        assert lotto_game.winner == player

    def test_no_kegs_one_bot(self):
        lotto_game = LottoGame(['bot1'])
        bot1 = lotto_game.players[0]
        lotto_game.update_game_state(self.no_kegs_code_number)
        assert lotto_game.winner == bot1
        assert lotto_game.is_over() == True

def test_play_lotto_game():
    play_lotto_game(test_players_count=1)
    play_lotto_game(test_players_count=2)
