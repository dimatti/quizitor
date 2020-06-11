from django.test import TestCase

from games.models import Game

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
          "lon": 7.597819,
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
          "question": "Чей это дом?",
          "answer": "Морозова",
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
          "question": "Какая старана представлена этим посольством",
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
