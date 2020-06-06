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


class AnimalTestCase(TestCase):

    def test_game_creation(self):
        g = Game.new_game(data)
        for cluster in g.clusters.all():
            print(cluster.points.all())
