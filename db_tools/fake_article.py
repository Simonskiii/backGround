#独立使用django的model
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backGroud.settings")

import django
django.setup()
from articles.models import Article, ArticleCatergory
import faker
from django.forms.models import model_to_dict
import random
fake = faker.Faker()
# for i in range(0, 5):
#     a_instance = ArticleCatergory()
#     name = fake.word()
#     a_instance.name = name
#     li = []
#     for i in name.split(" "):
#         li.append(i[0])
#     a_instance.code = "".join(li)
#     a_instance.save()

# for i in range(0, 5):
u = ArticleCatergory.objects.filter(name__isnull=False)
l = []
for key in u:
    l.append(key)
print(l)
for i in range(0, 20):
    instance = Article()
    name = fake.word()
    instance.name = name
    c = random.randint(0, 13)
    instance.category = l[c]
    instance.aritcle_brief = fake.sentence(nb_words=6, variable_nb_words=True)
    instance.author = fake.name()
    instance.content = fake.text(max_nb_chars=200)
    instance.click_num = random.randint(0, 200)
    instance.fav_num = random.randint(0,200)
    instance.save()




