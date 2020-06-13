import time

from django.test import TestCase
from datetime import datetime
from games.models import Game, CurrentGame

data = {
  "name": "Test Game",
  "clusters": [
    {
      "start": [12.1, 12.2],
      "finish": [12.3, 12.2],
      "points": [
        {
          "lat": 12.11,
          "lon": 12.55,
          "question": "How are you?",
          "answer": "fine",
          "tip": "wtf"
        },
        {
          "lat": 12.11,
          "lon": 12.55,
          "question": "How are you?",
          "answer": "fine",
          "tip": "wtf"
        },
        {
          "lat": 12.11,
          "lon": 12.55,
          "question": "How are you?",
          "answer": "fine",
          "tip": "wtf"
        }
      ]
    },
    {
      "start": [12.1, 12.2],
      "finish": [12.3, 12.2],
      "points": [
        {
          "lat": 12.11,
          "lon": 12.55,
          "question": "How are you?",
          "answer": "fine",
          "tip": "wtf"
        },
        {
          "lat": 12.11,
          "lon": 12.55,
          "question": "How are you?",
          "answer": "fine",
          "tip": "wtf"
        },
        {
          "lat": 12.11,
          "lon": 12.55,
          "question": "How are you?",
          "answer": "fine",
          "tip": "wtf"
        }
      ]
    }
  ]
}

data2 = {
  "name": "GAME NUMBER ONE",
  "clusters": [
    {
      "start": [55.765284, 37.605429],
      "finish": [55.757024, 37.601879],
      "points": [
        {
          "lat": 55.761752,
          "lon": 37.602939,
          "question": "Сокращенное название театра?",
          "answer": "МХАТ",
          "tip": "заметьте, это не МХТ"
        },
        {
          "lat": 55.760424,
          "lon": 37.597819,
          "question": "Назовите страну, дом титульной нации которой расположен тут?",
          "answer": "Израиль",
          "tip": "ой-вэй"
        },
        {
          "lat": 55.760424,
          "lon": 37.597819,
          "question": "Назовите фамилию писателя, который жил здесь",
          "answer": "Горький",
          "tip": "На дне"
        }
      ]
    },
    {
      "start": [55.757024, 37.601879],
      "finish": [55.748086, 37.600356],
      "points": [
        {
          "lat": 55.755553,
          "lon": 37.606747,
          "question": "Назовите тип организации, которая тут расположена",
          "answer": "Биржа",
          "tip": "Акции и торги"
        },
        {
          "lat": 55.752955,
          "lon": 37.603355,
          "question": "Назовите фамилию владельца этого дома?",
          "answer": "Морозов",
          "tip": "Савва"
        },
        {
          "lat": 55.750809,
          "lon": 37.600463,
          "question": "Назовите фамилию 'героя' этого памятника",
          "answer": "Гоголь",
          "tip": "Про души"
        }
      ]
    },
{
      "start": [55.748086, 37.600356],
      "finish": [55.743600, 37.608128],
      "points": [
        {
          "lat": 55.743893,
          "lon": 37.596727,
          "question": "Какая страна представлена этим посольством",
          "answer": "Люксенбург",
          "tip": "Роза"
        },
        {
          "lat": 55.743893,
          "lon": 37.596727,
          "question": "Фамилия того, чья галерея",
          "answer": "Глазунова",
          "tip": "( . ) ( . )"
        },
        {
          "lat": 55.749716,
          "lon": 37.592110,
          "question": "Фамилия человека, в честь котрого назван тестр",
          "answer": "Вахтангов",
          "tip": "Кикабидзе"
        }
      ]
    }
  ]
}

class AnimalTestCase(TestCase):

    def test_game_creation(self):
        g = Game.new_game(data)
        self.assertEqual(len(g.clusters.all()), 2)
        for cluster in g.clusters.all():
            self.assertEqual(len(cluster.points.all()), 3)

    def test_current_game(self):
        g = Game.new_game(data2)
        cg = CurrentGame(source_game=g, time_start=datetime.now())
        cg.save()
        c = cg.next_cluster()
        c1 = cg.current_cluster()

        print("FIRST POINT") #10
        print(c1.check_point(0, 55.761752, 37.602939))
        print(c1.get_question(0))
        print(c1.get_tip(0))
        print(c1.check_answer(0, "МХАТ"))
        print(c1.get_status()[0])

        print("SECOND POINT") #0
        print(c1.check_point(1, 55.760424, 37.597819))
        print(c1.get_question(1))
        print(c1.check_answer(1, "МХАТ"))
        print(c1.get_status()[1])

        print("THIRD POINT")
        lat, lon = c1.get_help(2) #10
        print(c1.check_point(2, lat, lon))
        print(c1.get_question(2))
        print(c1.check_answer(2, "Горький"))
        print(c1.get_status()[2])

        time.sleep(5)
        print(c1.close_cluster())

        print("2 - SECOND POINT")  # 0
        c2 = cg.next_cluster()
        lat, lon = c2.get_help(1)
        print(c2.check_point(1, lat, lon))
        print(c2.get_question(1))
        print(c2.check_answer(1, "моРозов"))
        print(c2.get_status()[1])

        print("2 - THIRD POINT")  # 0
        lat, lon = c2.get_help(2)
        print(c2.check_point(2, lat, lon))
        print(c2.get_question(2))
        print(c2.check_answer(2, "моРозов"))
        print(c2.get_status()[2])

        time.sleep(10)
        print(c2.close_cluster())
        print(c2.close_cluster(forced=True))