import pytest


VALID_MOVIE = {
    "id": 550,
    "title": "  Fight Club  ",
    "overview": " An insomniac office worker. ",
    "release_date": "1999-10-15",
    "popularity": 61.416,
    "vote_average": 8.4,
    "vote_count": 26280,
    "original_language": "en",
    "adult": False,
    "genre_ids": [18, 53, 53],
    "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    "backdrop_path": "/hZkgoQYus5vegHoetLkCJzb17zJ.jpg",
}


@pytest.fixture
def sample_movie():
    return dict(VALID_MOVIE)
