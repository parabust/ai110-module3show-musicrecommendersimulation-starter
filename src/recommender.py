from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> float:
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 3.0
        if song.mood == user.favorite_mood:
            score += 2.0
        score += 1.0 * (1 - abs(song.energy - user.target_energy))
        if user.likes_acoustic:
            score += 0.5 * song.acousticness
        else:
            score += 0.5 * (1 - song.acousticness)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = sorted(self.songs, key=lambda s: self.score_song(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"it's a {song.genre} track you might enjoy")
        if song.mood == user.favorite_mood:
            reasons.append(f"it has a {song.mood} vibe")
        if abs(song.energy - user.target_energy) < 0.2:
            reasons.append("the energy level suits your taste")
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("it has a strong acoustic feel")
        elif not user.likes_acoustic and song.acousticness < 0.5:
            reasons.append("it has a produced, non-acoustic sound")
        return ", and ".join(reasons) if reasons else "it's a good overall match for your taste"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    user = UserProfile(
        favorite_genre=user_prefs.get("favorite_genre", ""),
        favorite_mood=user_prefs.get("favorite_mood", ""),
        target_energy=user_prefs.get("target_energy", 0.0),
        likes_acoustic=user_prefs.get("likes_acoustic", False),
    )
    recommender = Recommender([])

    scored = sorted(
        [(song, recommender.score_song(user, Song(**song))) for song in songs],
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        (song, score, recommender.explain_recommendation(user, Song(**song)))
        for song, score in scored[:k]
    ]
