import asyncio
import unittest
from unittest.mock import Mock, patch
from aiogram.types import Message, URLInputFile, BotCommandScopeDefault
from aiogram import Bot
from Bot import set_commands, user_filters, user_films
from filter_country_keyboard import keyboard_builder3, country_map
from filter_genre_keyboard import keyboard_builder4, genre_map
from filter_rating_keyboard import keyboard_builder2, rating_from_map, rating_before_map, keyboard_builder
from filter_year_keyboard import keyboard_builder5, keyboard_builder6
from find_movie import get_movie_url, get_random_movie, get_new_movie, get_popular_movie, by_filter_get, get_movie_info, show_info_about_movie
from keyboard_for_filter import UserFilter



class TestBot(unittest.TestCase):
    @patch('aiogram.Bot')
    def test_start(self, mock_bot):
        # Создаем мок сообщения
        message = Mock(spec=Message)
        message.from_user.full_name = "Test User"

        # Вызываем функцию start
        with patch('Bot.start') as mock_start:
            asyncio.run(mock_start(message))

        # Проверяем, что отправлено сообщение с ожидаемым текстом
        mock_start.assert_called_once()
        expected_text = "Привет, Test User!\n\nЯ - бот для подборки фильмов, мультфильмов и сериалов.\nДля получения списка команд и работы введите /menu."
        message.answer.assert_called_once_with(text=expected_text)

    @patch('aiogram.Bot')
    def test_menu(self, mock_bot):
        # Создаем мок сообщения
        message = Mock(spec=Message)

        # Вызываем функцию menu
        with patch('Bot.menu') as mock_menu:
            asyncio.run(mock_menu(message))

        # Проверяем, что отправлено сообщение с кнопками
        mock_menu.assert_called_once()
        message.answer.assert_called_once()  # проверяем, что был вызван метод answer

    @patch('aiogram.Bot')
    def test_info_about_us(self, mock_bot):
        # Создаем мок callback
        callback = Mock()
        callback.message = Mock()

        # Вызываем функцию info_about_us
        with patch('Bot.info_about_us') as mock_info_about_us:
            asyncio.run(mock_info_about_us(callback))

        # Проверяем, что отправлено сообщение с ожидаемым текстом
        expected_text = ("Всем привет 👋 \n"
                         "Мы студенты 2 курса ОП «Прикладная математика и информатика». \n"
                         "Данный бот - результат нашего проекта по Python 🎉 \n")
        callback.message.answer.assert_called_once_with(text=expected_text)

    @patch('sqlite3.connect')
    @patch('aiogram.Bot')
    def test_info_about_favourite(self, mock_bot, mock_db):
        # Создаем мок callback и базы данных
        callback = Mock()
        callback.message = Mock()
        callback.from_user.id = 123  # Пример идентификатора пользователя
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Сценарий, когда в базе данных есть фильмы
        mock_cursor.fetchall.return_value = [('Movie1',), ('Movie2',)]
        with patch('name.info_about_favourite') as mock_info_about_favourite:
            asyncio.run(mock_info_about_favourite(callback))
        expected_text = "Ваши фильмы：\nMovie1\nMovie2"
        callback.message.answer.assert_called_with(expected_text)

        # Сценарий, когда в базе данных нет фильмов
        mock_cursor.fetchall.return_value = []
        with patch('name.info_about_favourite') as mock_info_about_favourite:
            asyncio.run(mock_info_about_favourite(callback))
        callback.message.answer.assert_called_with("Не найдены")

    @patch('aiogram.Bot')
    def test_filter(self, mock_bot, your_module_name=None):
        # Создаем мок callback
        callback = Mock()
        callback.message = Mock()
        callback.from_user.id = 123  # Пример идентификатора пользователя

        # Создаем мок кнопок
        mock_buttons = Mock()
        with patch('Bot.buttons', mock_buttons):
            # Случай 1: Все фильтры не установлены
            user_filters[123] = UserFilter()
            with patch('name.filter') as mock_filter:
                asyncio.run(mock_filter(callback))

            expected_text = "✔️ Выбрано : \n➡️ Рейтинг : \n➡️ Год : \n➡️ Жанр : \n➡️ Страна : "
            callback.message.answer.assert_called_with(text=expected_text, reply_markup=mock_buttons.as_markup())

            # Случай 2: Установлены некоторые фильтры
            user_filters[123].set_rating_from(5)
            user_filters[123].set_rating_before(8)
            user_filters[123].set_year_from(2000)
            user_filters[123].set_year_to(2010)
            user_filters[123].set_type("Комедия")
            user_filters[123].set_country("США")

            with patch('name.filter') as mock_filter:
                asyncio.run(mock_filter(callback))

            expected_text = "✔️ Выбрано : \n➡️ Рейтинг : 5 - 8\n➡️ Год : 2000 - 2010\n➡️ Жанр : Комедия\n➡️ Страна : США"
            callback.message.answer.assert_called_with(text=expected_text, reply_markup=mock_buttons.as_markup())

        @patch('aiogram.Bot')
        def test_rating_before(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.rating_before') as mock_rating_before:
                asyncio.run(mock_rating_before(callback))

            callback.message.answer.assert_called_with('Выберите число:', reply_markup=keyboard_builder2.as_markup())

        @patch('aiogram.Bot')
        def test_rating_from(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.rating_from') as mock_rating_from:
                asyncio.run(mock_rating_from(callback))

            callback.message.answer.assert_called_with('Выберите число:', reply_markup=keyboard_builder.as_markup())

        @patch('aiogram.Bot')
        def test_country(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.country') as mock_country:
                asyncio.run(mock_country(callback))

            callback.message.answer.assert_called_with('Выберите страну:', reply_markup=keyboard_builder3.as_markup())

        @patch('aiogram.Bot')
        def test_genre(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.genre') as mock_genre:
                asyncio.run(mock_genre(callback))

            callback.message.answer.assert_called_with('Выберите жанр:', reply_markup=keyboard_builder4.as_markup())

        @patch('aiogram.Bot')
        def test_process_rating_from(self, mock_bot):
            callback = Mock()
            callback.data = 'some_data_key'
            callback.from_user.id = 123
            user_filters[123] = UserFilter()

            with patch('name.process_rating_from') as mock_process_rating_from:
                asyncio.run(mock_process_rating_from(callback))

            self.assertEqual(user_filters[123].get_rating_from(), rating_from_map['some_data_key'])
            mock_process_rating_from.assert_called_with(callback)

        @patch('aiogram.Bot')
        def test_process_rating_before(self, mock_bot):
            callback = Mock()
            callback.data = 'some_data_key'
            callback.from_user.id = 123
            user_filters[123] = UserFilter()

            with patch('name.process_rating_before') as mock_process_rating_before:
                asyncio.run(mock_process_rating_before(callback))

            self.assertEqual(user_filters[123].get_rating_before(), rating_before_map['some_data_key'])
            mock_process_rating_before.assert_called_with(callback)

        @patch('aiogram.Bot')
        def test_process_country(self, mock_bot):
            callback = Mock()
            callback.data = 'country_key'
            callback.from_user.id = 123
            user_filters[123] = UserFilter()

            with patch('name.process_country') as mock_process_country:
                asyncio.run(mock_process_country(callback))

            self.assertEqual(user_filters[123].get_country(), country_map['country_key'])
            mock_process_country.assert_called_with(callback)

        @patch('aiogram.Bot')
        def test_process_genre(self, mock_bot):
            callback = Mock()
            callback.data = 'genre_key'
            callback.from_user.id = 123
            user_filters[123] = UserFilter()

            with patch('name.process_genre') as mock_process_genre:
                asyncio.run(mock_process_genre(callback))

            self.assertEqual(user_filters[123].get_type(), genre_map['genre_key'])
            mock_process_genre.assert_called_with(callback)

        @patch('aiogram.Bot')
        def test_cancel_all(self, mock_bot):
            callback = Mock()
            callback.message = Mock()
            callback.from_user.id = 123
            user_filters[123] = UserFilter()
            user_filters[123].set_rating_from("5")
            user_filters[123].set_rating_before("8")
            user_filters[123].set_year_from("2000")
            user_filters[123].set_year_to("2010")
            user_filters[123].set_type("Комедия")
            user_filters[123].set_country("США")

            with patch('name.cancel_all') as mock_cancel_all:
                asyncio.run(mock_cancel_all(callback))

            self.assertEqual(user_filters[123].get_rating_from(), "")
            self.assertEqual(user_filters[123].get_rating_before(), "")
            self.assertEqual(user_filters[123].get_year_from(), "")
            self.assertEqual(user_filters[123].get_year_to(), "")
            self.assertEqual(user_filters[123].get_type(), "")
            self.assertEqual(user_filters[123].get_country(), "")
            mock_cancel_all.assert_called_with(callback)
            callback.message.answer.assert_called_with('Фильтр сброшен')

        @patch('aiogram.Bot')
        def test_year_from(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.year_from') as mock_year_from:
                asyncio.run(mock_year_from(callback))

            callback.message.answer.assert_called_with('Выберите год:', reply_markup=keyboard_builder5.as_markup())

        @patch('aiogram.Bot')
        def test_filter_by_year_from(self, mock_bot):
            callback = Mock()
            callback.data = "s2020"
            callback.from_user.id = 123
            user_filters[123] = UserFilter()

            with patch('name.filter_by_year_from') as mock_filter_by_year_from:
                asyncio.run(mock_filter_by_year_from(callback))

            self.assertEqual(user_filters[123].get_year_from(), 2020)
            mock_filter_by_year_from.assert_called_with(callback)

        @patch('aiogram.Bot')
        def test_year_to(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.year_to') as mock_year_to:
                asyncio.run(mock_year_to(callback))

            callback.message.answer.assert_called_with('Выберите год:', reply_markup=keyboard_builder6.as_markup())

        @patch('aiogram.Bot')
        def test_filter_by_year_to(self, mock_bot):
            callback = Mock()
            callback.data = "f2020"
            callback.from_user.id = 123
            user_filters[123] = UserFilter()

            with patch('name.filter_by_year_to') as mock_filter_by_year_to:
                asyncio.run(mock_filter_by_year_to(callback))

            self.assertEqual(user_filters[123].get_year_to(), 2020)
            mock_filter_by_year_to.assert_called_with(callback)

        @patch('aiogram.Bot')
        @patch('name.get_random_movie')
        def test_find_random(self, mock_get_random_movie, mock_bot):
            callback = Mock()
            callback.message = Mock()
            mock_get_random_movie.return_value = {'nameRu': 'Random Movie', 'posterUrl': 'url_to_poster'}

            with patch('name.find_random') as mock_find_random:
                asyncio.run(mock_find_random(callback))

            callback.message.answer.assert_called_with(text="Выполняется поиск ...")
            callback.message.answer_photo.assert_called()

        @patch('aiogram.Bot')
        @patch('name.get_new_movie')
        def test_find_new(self, mock_get_new_movie, mock_bot):
            callback = Mock()
            callback.message = Mock()
            mock_get_new_movie.return_value = {'nameRu': 'New Movie', 'posterUrl': 'url_to_poster'}

            with patch('name.find_new') as mock_find_new:
                asyncio.run(mock_find_new(callback))

            callback.message.answer.assert_called_with(text="Выполняется поиск ...")
            callback.message.answer_photo.assert_called()

        @patch('aiogram.Bot')
        @patch('name.get_popular_movie')
        def test_find_popular(self, mock_get_popular_movie, mock_bot):
            callback = Mock()
            callback.message = Mock()
            mock_get_popular_movie.return_value = {'nameRu': 'Popular Movie', 'posterUrl': 'url_to_poster'}

            with patch('name.find_popular') as mock_find_popular:
                asyncio.run(mock_find_popular(callback))

            callback.message.answer.assert_called_with(text="Выполняется поиск ...")
            callback.message.answer_photo.assert_called()

        @patch('aiogram.Bot')
        @patch('name.by_filter_get')
        def test_confirm(self, mock_by_filter_get, mock_bot):
            callback = Mock()
            callback.message = Mock()
            callback.from_user.id = 123
            user_filters[123] = UserFilter()
            mock_film = {'nameRu': 'Test Movie', 'posterUrl': 'url_to_poster'}
            mock_by_filter_get.return_value = mock_film

            with patch('name.confirm') as mock_confirm:
                asyncio.run(mock_confirm(callback))

            callback.message.answer.assert_called_with('Поиск запущен')
            callback.message.answer_photo.assert_called_with(URLInputFile(mock_film['posterUrl']), caption="Постер")

        @patch('aiogram.Bot')
        def test_find_random(self, mock_bot):
            callback = Mock()
            callback.message = Mock()

            with patch('name.find_random') as mock_find_random:
                asyncio.run(mock_find_random(callback))

            callback.message.answer.assert_called_with("Введите название фильма")

        @patch('aiogram.Bot')
        @patch('name.get_movie_info')
        def test_handle_user_input(self, mock_get_movie_info, mock_bot):
            message = Mock()
            message.text = "Test Movie"
            message.from_user.id = 123
            mock_get_movie_info.return_value = {'nameRu': 'Test Movie', 'posterUrl': 'url_to_poster'}

            with patch('name.handle_user_input') as mock_handle_user_input:
                asyncio.run(mock_handle_user_input(message))

            message.answer.assert_called_with(f"Ищу Test Movie...")
            message.answer_photo.assert_called()

        @patch('aiogram.Bot')
        @patch('sqlite3.connect')
        def test_add_favourite(self, mock_db, mock_bot):
            callback = Mock()
            callback.message = Mock()
            callback.from_user.id = 123
            user_films[123] = 'Test Movie'
            mock_conn = mock_db.return_value
            mock_cursor = mock_conn.cursor.return_value

            with patch('name.add_favourite') as mock_add_favourite:
                asyncio.run(mock_add_favourite(callback))

            mock_cursor.execute.assert_called_with("INSERT INTO movies (user_id, movie) VALUES (?, ?)",
                                                   (123, 'Test Movie'))
            mock_conn.commit.assert_called_once()
            callback.message.answer.assert_called_with(text="Добавлено")

        class TestBotCommands(unittest.TestCase):
            @patch('aiogram.Bot')
            def test_set_commands(self, mock_bot):
                # Создаем мок для объекта Bot
                bot = Mock(spec=Bot)

                # Вызываем функцию set_commands
                asyncio.run(set_commands(bot))

                # Проверяем, что метод set_my_commands был вызван с правильными аргументами
                expected_commands = [
                    {'command': 'start', 'description': 'Начало работы'},
                    {'command': 'menu', 'description': 'Меню'}
                ]
                bot.set_my_commands.assert_called_once_with(expected_commands, BotCommandScopeDefault())

        class TestGetMovieUrl(unittest.TestCase):
            def test_get_movie_url(self):
                movie_name = "Test Movie"
                urls = get_movie_url(movie_name)

                expected_urls = [
                    "https://www.kinopoisk.ru/index.php?kp_query=Test%20Movie",
                    "https://premier.one/search?query=Test%20Movie",
                    "https://okko.tv/search?q=Test%20Movie",
                    "https://www.ivi.tv/search?q=Test%20Movie",
                    "https://doramy.club/?s=Test%20Movie"
                ]

                self.assertEqual(len(urls), 5)
                for url in expected_urls:
                    self.assertIn(url, urls)

            @patch('requests.get')
            @patch('random.randint')
            def test_get_movie(self, mock_randint, mock_get):
                mock_randint.return_value = 0
                mock_get.return_value.json.return_value = {'items': [{'kinopoiskId': 123}]}
                movie = get_random_movie()
                self.assertIn('kinopoiskId', movie)

            def test_get_new_movie(self, mock_get):
                mock_get.return_value.json.return_value = {'films': [{'filmId': 123}]}
                movie = get_new_movie()
                self.assertIn('filmId', movie)

            def test_get_popular_movie(self, mock_get):
                mock_get.return_value.json.return_value = {'items': [{'kinopoiskId': 123}]}
                movie = get_popular_movie()
                self.assertIn('kinopoiskId', movie)

            @patch('requests.get')
            @patch('random.randint')
            def test_by_filter_get(self, mock_randint, mock_get):
                mock_randint.return_value = 0
                mock_get.return_value.json.return_value = {'items': [{'kinopoisk_id': 123}]}
                movie = by_filter_get("", "", "", "", "", "")
                self.assertIn('kinopoisk_id', movie)

            from unittest.mock import patch
            import unittest

        class TestMovieFunctions(unittest.TestCase):
            @patch('requests.get')
            def test_get_movie_info(self, mock_get):
                # Настройка мока для имитации ответа API
                mock_get.return_value.json.return_value = {
                    'films': [{'filmId': 123, 'nameRu': 'Test Movie', 'year': '2020'}]
                    }

                movie_name = "Test Movie"
                movie_info = get_movie_info(movie_name)

                self.assertEqual(movie_info['filmId'], 123)
                self.assertEqual(movie_info['nameRu'], 'Test Movie')
                self.assertEqual(movie_info['year'], '2020')



        class TestShowInfoAboutMovie(unittest.TestCase):
            @patch('name.get_movie_url')
            def test_show_info_about_movie(self, mock_get_movie_url):
                # Настройка мока для get_movie_url
                mock_get_movie_url.return_value = [
                    "url1", "url2", "url3", "url4", "url5"
                ]

                movie = {
                    'nameRu': 'Test Movie',
                    'year': '2020',
                    'genres': [{'genre': 'Action'}, {'genre': 'Drama'}],
                    'countries': [{'country': 'USA'}, {'country': 'Canada'}],
                    'description': 'Test Description',
                    'ratingImdb': '8.0'
                }

                movie_info_text = show_info_about_movie(movie)

                self.assertIn('Test Movie', movie_info_text)
                self.assertIn('2020', movie_info_text)
                self.assertIn('Action, Drama', movie_info_text)
                self.assertIn('USA, Canada', movie_info_text)
                self.assertIn('Test Description', movie_info_text)
                self.assertIn('8.0', movie_info_text)
                # Проверяем наличие URL в тексте
                for url in mock_get_movie_url.return_value:
                    self.assertIn(url, movie_info_text)