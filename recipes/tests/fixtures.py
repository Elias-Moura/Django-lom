from recipes.models import Category, Recipe, User


def make_category(name='Category'):
    return Category.objects.create(name=name)

def make_author(
    first_name='user',
    last_name='name',
    username='username',
    password='123456',
    email='username@email.com',
):
    return User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=password,
        email=email,
    )

def make_recipe(
    category_data=None,
    author_data=None,
    title='Recipe Title',
    description='Recipe Description',
    slug='recipe-slug',
    preparation_time=10,
    preparation_time_unit='Minutos',
    servings=5,
    servings_unit='Porções',
    preparation_steps='Recipe Preparation Steps',
    preparation_steps_is_html=False,
    is_published=True,
):
    if category_data is None:
        category_data = {}

    if author_data is None:
        author_data = {}

    return Recipe.objects.create(
        category=make_category(**category_data),
        author=make_author(**author_data),
        title=title,
        description=description,
        slug=slug,
        preparation_time=preparation_time,
        preparation_time_unit=preparation_time_unit,
        servings=servings,
        servings_unit=servings_unit,
        preparation_steps=preparation_steps,
        preparation_steps_is_html=preparation_steps_is_html,
        is_published=is_published,
    )
