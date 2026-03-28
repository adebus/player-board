# POST /sessions
# Inputs: start_time, location, notes?, [players]?
# Returns: GameSesionRead
# Validation: any players provided must exist
# Notes: In future when account feature is live, presume the person creating the session is attending, which will make [players] optional

# GET /sessions
# Inputs: none
# Returns: [GameSessionRead]
# Validation: none

# GET /sessions/{id}
# Inputs: id
# Returns: GameSessionRead
# Validation: none

# POST /sessions/{id}/players
# Inputs: id, [players]
# Returns: [PlayerRead]
# Validation: any players provided must exist

# GET /sessions/{id}/players
# input: id
# Returns: [PlayerRead]
# Validation: none

# POST /sessions/{id}/games
# Input: id, [game_id, start_time?, end_time?, notes?]
# Returns: [GameRead]
# Validation: any games must be in the games table.

# GET /sessions/{id}/games
# Input: id
# Returns: [GameRead]
# Validation: none

# GET /sessions/{id}/games/{game_played_id}
# Input: id, game_played_id
# Returns: [GameRead]
# Validation: none

# POST /sessions/{id}/games/{game_id}/scores
# Input: id, game_id, [player_id, score?, winner?]
# Returns: [GameScoreRead]
# Validation: game must be played in session, players must exist in session

# GET /sessions/{id}/games/{game_id}/scores
# Input: id, game_id
# Returns [GameScoreRead]
# Validation: none

# GET /sessions/{id}/games/{game_id}/scores/{player_id}
# Input: id, game_id, player_id
# Returns: GameScoreRead
# Validation: none
