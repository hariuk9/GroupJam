DB schema:

table: user_auths

user_id: int
access_token: string
token_type: string
scope: string
expires_in: int
refresh_token: string

table: top_songs

user_id: int
id: string
danceability: float
energy: float 
key: float
loudness: float
mode: float
speechiness: float
acousticness: float
instrumentalness: float
liveness: float
valence: float
tempo: float
type: string
uri: string
track_href: string
analysis_url: string
duration_ms: int
time_signature: int

__table__ = Table('user_auths', Base.metadata,
        Column('user_id', Integer, primary_key=True),
        Column('access_token', String(50)),
        Column('token_type', String(50)),
        Column('scope', String(50)),
        Column('expires_in', Integer),
        Column('refresh_token', String(50))
    )

__table__ = Table('top_songs', Base.metadata,
        Column('user_id', Integer, primary_key=True),
        Column('id', Float)
        Column('id', Float)
        Column('id', Float)
        Column('id', Float)
        Column('id', Float)
        Column('id', Float)
        Column('id', Float)

    )
