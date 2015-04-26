#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

match_id= 0;
matchesPlayedByWinner = 0;
matchesPlayedByLoser = 0;


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE from matches;")
    conn.commit()
    cur.close()
    conn.close()
    
def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE from playerResults;")
    conn.commit()
    cur.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("select count(player_id) from playerResults;")
    no_players = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return no_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO playerResults(player_name, matches_won, matches_played) VALUES (%s, %s, %s);", (name, 0 , 0))
    conn.commit()
    cur.close()
    conn.close()
    

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("select * from playerResults order by matches_won desc;")
    standings = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    
    global match_id    
    #Insert the match_id in the database and record the win/loss for each player.
    match_won =0;
    conn = connect()
    cur = conn.cursor()
    match_id += 1
    cur.execute("Insert into matches (match_id, player_id, match_result) VALUES (%s, %s, %s);",(match_id,winner,1))    
    cur.execute("Insert into matches (match_id, player_id, match_result) VALUES (%s, %s, %s);",(match_id,loser,0))

    #Read matches_played by winner from the database and add 1 to that value since a match is reported.
    cur.execute("SELECT * FROM playerResults WHERE player_id = %s;",(winner,))
    matchesPlayedByWinner = cur.fetchone()[3]    
    matchesPlayedByWinner = int(matchesPlayedByWinner) +1;
    #update matches_played by winner in database
    updateTotalMatchesPlayed(winner, matchesPlayedByWinner);

    #Read matches_won by winner from the database and add 1 to that value.
    cur.execute("SELECT * FROM playerResults WHERE player_id = %s;",(winner,))
    matchesWonByWinner = cur.fetchone()[2]
    matchesWonByWinner = int(matchesWonByWinner) +1;
    #update matches_won by winner in database
    updateTotalWins(winner,matchesWonByWinner)
    
    #Read matches_played by loser from the database and add 1 to that value.
    cur.execute("SELECT * FROM playerResults WHERE player_id = %s;",(loser,))
    matchesPlayedByLoser = cur.fetchone()[3]
    matchesPlayedByLoser = int(matchesPlayedByLoser) +1;
    #update matches_played by loser in database
    updateTotalMatchesPlayed(loser, matchesPlayedByLoser);

    conn.commit()
    cur.close()
    conn.close()
       
def updateTotalMatchesPlayed(playerId, matchesPlayed):

    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE playerResults SET matches_played = %s where player_id = %s;", (matchesPlayed, playerId,))
    conn.commit()
    cur.close()
    conn.close()

def updateTotalWins(playerId, matchesWon):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE playerResults SET matches_won = %s  where player_id = %s;", (matchesWon, playerId,))
    conn.commit()
    cur.close()
    conn.close()
    
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
   
    """
    conn = connect()
    cur = conn.cursor()
    pairings = []
    no_of_pairs = (countPlayers()/2)
    #pair 2 players at a time
    limit = 2
    offset = 0
    for index in range(no_of_pairs):
         # Sort playerResults by matches_won so that players with equal to or nearly-equal win-record are paired together
         cur.execute("select player_id from playerResults order by matches_won desc LIMIT  %s OFFSET %s;", (limit,offset,))
         players_who_should_be_paired = cur.fetchall()
         first_player = players_who_should_be_paired[0][0]
         second_player = players_who_should_be_paired[1][0]
         cur.execute("select player_id, player_name from playerResults where player_id =%s;",(first_player,))
         first_player_record = cur.fetchone()
         cur.execute("select player_id, player_name from playerResults where player_id =%s;",(second_player,))
         second_player_record = cur.fetchone()
         pairings.extend([(first_player_record[0],first_player_record[1],second_player_record[0],second_player_record[1])])
         limit +=2
         # set offset = 2 so that next pair in sorted playerResults can be computed
         offset +=2
    conn.commit()
    cur.close()
    conn.close()
    return pairings

