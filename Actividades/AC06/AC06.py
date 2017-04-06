from datetime import datetime as dt


def set_id():
    n = 0
    while True:
        yield "#" + str(n) + "M"
        n += 1


def popular(numero):
    return list((filter(lambda pelicula: pelicula.rating > numero, peliculas)))


def with_genres(numero):
    return list((filter(lambda pelicula: len(pelicula.genres) > numero, peliculas)))


def tops_of_genre(genero):
    a = (filter(lambda pelicula: genero in pelicula.genres, peliculas))
    return sorted(a, key=lambda pelicula: pelicula.rating, reverse=True)[0:10]


def actor_rating(nombre):
    a = (filter(lambda cast: nombre == cast.name, castings))
    b = list((i.movie for i in list(a)))
    c = list((filter(lambda pelicula: pelicula.title in b, peliculas)))
    return sum((i.rating for i in list(c))) / len(c)


def compare_actors(nombre1, nombre2):
    print(nombre1 if actor_rating(nombre1) > actor_rating(nombre2) else nombre2)


def movies_of(nombre):
    a = (filter(lambda cast: nombre == cast.name, castings))
    return list(((i.movie, i.character) for i in list(a)))


def from_year(ano):
    ano = dt.strptime(ano, '%Y-%m-%d')
    return list((filter(lambda pelicula: pelicula.release == ano, peliculas)))


def peliculas():
    return list((Movie(*(line.strip().split(",")[1:])) for line in open('movies.txt', 'r')))


def cast():
    return list((Cast(*(line.strip().split(","))) for line in open('cast.txt', 'r')))


class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = list((genero for genero in args))

    def __repr__(self):
        return self.title


if __name__ == "__main__":
    peliculas = peliculas()
    castings = cast()
    print(popular(60))
    print(with_genres(4))
    print(tops_of_genre("Action"))
    print(actor_rating("Shakira"))
    compare_actors("Shakira", "Kaley Cuoco")
    print(movies_of("Shakira"))
    print(from_year("2017-03-23"))
