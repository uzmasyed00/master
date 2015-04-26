-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
create database tournament;
'''create table players (player_id serial, player_name varchar);'''
create table matches (match_id integer, player_id integer references playerResults, match_result integer);
create table playerResults(player_id serial PRIMARY KEY, player_name varchar, matches_won integer, matches_played integer);
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


