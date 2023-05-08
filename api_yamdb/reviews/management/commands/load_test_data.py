from csv import DictReader
from django.core.management.base import BaseCommand

from reviews.models import User, Title, Review, Genre, Comment, Category


class Command(BaseCommand):
    help = "Загрузить данные из static/data"

    def handle(self, *args, **options):

        print("Загрузка данных из csv в базу:")

        model = User

        print(f"Загружаю {model.__name__}")
        for row in DictReader(open("static/data/users.csv", encoding="utf8")
                              ):
            model.objects.create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],)

        model = Category

        print(f"Загружаю {model.__name__}")
        for row in DictReader(
            open("static/data/category.csv", encoding="utf8")
        ):
            model.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )

        model = Genre

        print(f"Загружаю {model.__name__}")
        for row in DictReader(open('static/data/genre.csv', encoding='utf8')):
            model.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )

        model = Title

        print(f"Загружаю {model.__name__}")
        for row in DictReader(open('static/data/titles.csv', encoding='utf8')):
            model.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']),
            )

        model = Title.genre.through

        print(f"Загружаю {model.__name__}")
        for row in DictReader(
            open('static/data/genre_title.csv', encoding='utf8')
        ):
            model.objects.create(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )

        model = Review

        print(f"Загружаю {model.__name__}")
        for row in DictReader(open('static/data/review.csv', encoding='utf8')):
            model.objects.create(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date'],
            )

        model = Comment

        print(f"Загружаю {model.__name__}")
        for row in DictReader(open('static/data/comments.csv', encoding='utf8')
                              ):
            model.objects.create(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date'],
            )
