""" handles the communication with the database """
import logging
import dataclasses
from dataclasses import dataclass
import traceback
import json
from datetime import datetime
import pymssql

import database.GamesGamesModel as GamesGamesModel
import database.TableSentGames as TableSentGames
import database.TeamModel as TeamModel
import database.StreamGamesModel as StreamGamesModel

import DatabaseConnectionSettings

class GDASDB:
    """ handles all the stuff with the database """
    DBDRIVER= '{ODBC Driver 17 for SQL Server}'

    TABLE_CREATE_GAMES="IF OBJECT_ID(N'SentGames', N'U') IS NULL " \
        "CREATE TABLE SentGames(" \
        "gameid INT NOT NULL, " \
        "championship VARCHAR(50), " \
        "stage VARCHAR(20), " \
        "filename VARCHAR(50), " \
        "email VARCHAR(50), " \
        "sent BIT, " \
        "CONSTRAINT PKGAME PRIMARY KEY (gameid))"

    QUERY_GAMES_DELETE = "DELETE FROM SentGames;"
    QUERY_GAMES_EXISTS = "SELECT COUNT(*) FROM SentGames WHERE gameid = %s;"
    QUERY_GAMES_SELECT = "SELECT * FROM SentGames;"
    QUERY_GAMES_INSERT = "INSERT INTO SentGames(gameid, championship, stage, " \
        "filename, email, sent) " \
        "VALUES(%s, %s, %s, %s, %s, %s)"

    TABLE_CREATE_STREAMGAMES = "IF OBJECT_ID(N'stream_games', N'U') IS NULL " \
        "CREATE TABLE stream_games(" \
        "  stream_game_id INT NOT NULL," \
        "  sg_datetime DATETIME)"
    QUERY_STREAMGAMES_INSERT = "INSERT INTO stream_games (stream_game_id, sg_datetime) " \
        "VALUES(%s, %s)"
    QUERY_STREAMGAMES_SELECT = "SELECT * FROM stream_games "
    QUERY_STREAMGAMES_DELETE = "DELETE FROM stream_games WHERE stream_game_id = %s"
    QUERY_STREAMGAMES_UPDATE = "UPDATE stream_games " \
        "SET sg_datetime = '%s' " \
        "WHERE stream_game_id = %s "

    TABLE_CREATE_TEAMS="IF OBJECT_ID(N'teams', N'U') IS NULL " \
        "CREATE TABLE teams( " \
        "teamid INT NOT NULL IDENTITY(1,1), " \
        "name VARCHAR(50), " \
        "sav_echelon VARCHAR(20), " \
        "sav_gender VARCHAR(50), " \
        "sav_serie VARCHAR(50), " \
        "coach VARCHAR(50), " \
        "email VARCHAR(50), " \
        "CONSTRAINT PKTEAM PRIMARY KEY (teamid))"
    QUERY_TEAMS_INSERT = "INSERT INTO teams(name, sav_echelon, " \
        "sav_gender, sav_serie, coach, email) " \
        "VALUES (%s, %s, %s, %s, %s, %s)"
    QUERY_TEAMS_SELECT = "SELECT * " \
        "FROM teams "
    QUERY_TEAMS_DELETE = "DELETE FROM teams WHERE teamid = %s"
    QUERY_TEAMS_UPDATE = "UPDATE teams " \
        "SET name = IsNull(%s, name)," \
        "   sav_echelon = IsNull(%s, sav_echelon)," \
        "   sav_gender = IsNull(%s, sav_gender)," \
        "   sav_serie = IsNull(%s, sav_serie)," \
        "   coach = IsNull(%s, coach)," \
        "   email = IsNull(%s, email) " \
        "WHERE teamid = %s"

    QUERY_GAMES_GAMESMODEL_SELECT = "SELECT * " \
        "FROM games_gamesmodel"
    QUERY_GAMES_GAMESMODEL_UPDATE = "UPDATE games_gamesmodel "

    def set_clause(self, args: dict):
        """ creates the set based on the args """
        result = ""
        for key, value in args.items():
            logging.info("building set clause with key=%s as value=%s", key, value)
            clause = "{pre} {key} = {value} "
            pre = "SET" if len(result) == 0 else ","
            if value is not None:
                result = result + clause.format(pre=pre, key=key,
                    value=value if isinstance(value, int) else f"'{value}'")
        return result

    def where_clause(self, args:dict):
        """ """
        result = ""
        logging.info(args)
        for key, value in args.items():
            logging.info("building where clause with key=%s and value=%s", key, value)
            clause = "{pre} {key} = {value} "
            pre = "WHERE" if len(result) == 0 else "AND"
            if value is not None:
                result = result + clause.format(pre=pre, key=key,
                    value=value if isinstance(value, int) else f"'{value}'")
        return result
    
    def where_clause(self, args:dataclass):
        """ uses the dict to create a where clause """
        return self.where_clause(dataclasses.asdict(args))

    def db(self):
        """ gets the database object """
        return self._db

    def __init__(self, host, database, user, password) -> None:
        conn = DatabaseConnectionSettings(host, database, user, password)
        self.__init__(conn)

    def __init__(self, connection: DatabaseConnectionSettings) -> None:
        """ initializes the connection """
        try:
            # pylint: disable=no-member
            self._db = pymssql.connect(server=connection.host, user=connection.user,
                                      password=connection.password, database=connection.database)
            self._db.autocommit(True)
            cursor = self._db.cursor()
            cursor.execute("SELECT DB_NAME() AS DataBaseName")
            record = cursor.fetchone()
            logging.info("You're connected to database: %s", record)
            self.execute_query(self.TABLE_CREATE_GAMES)
            self.execute_query(self.TABLE_CREATE_TEAMS)
            self.execute_query(self.TABLE_CREATE_STREAMGAMES)
        # pylint: disable=c-extension-no-member
        except pymssql._pymssql.OperationalError as e:
            logging.error("Error while connecting to MySQL: %s", e)

    def execute_query(self, query, params=None):
        """ executes the query """
        cursor = self._db.cursor()
        try:
            cursor.execute(query, params)
        # pylint: disable=no-member
        except pymssql.DatabaseError:
            logging.error("Error while executing query to MySQL: %s", traceback.format_exc())
            return None
        return cursor

    def team_delete(self, teamid):
        """ deletes a team """
        self.execute_query(self.QUERY_TEAMS_DELETE, (teamid,))
    def team_insert(self, team: TeamModel):
        """ inserts a team """
        self.execute_query(self.QUERY_TEAMS_INSERT, (team.name,
                           team.sav_echelon, team.sav_gender,
                           team.sav_serie, team.coach, team.email))
    def team_update(self, team: TeamModel):
        """ updates an existent team """
        self.execute_query(self.QUERY_TEAMS_UPDATE, (team.name,
                           team.sav_echelon, team.sav_gender,
                           team.sav_serie, team.coach, team.email, team.teamid))
    def teams_get(self, team: TeamModel = TeamModel()):
        """ gets all the teams in the database """
        query = self.QUERY_TEAMS_SELECT + self.where_clause(team)
        logging.info("Running query \n%s", query)
        cursor = self.execute_query(query)
        results = []
        for team_cursor in cursor:
            results.append(TeamModel(team_cursor))
        return results

    def streamgames_insert(self, sg: StreamGamesModel):
        """ inserts a new stream game """
        assert sg.stream_game_id is None, "'stream_game_id' is not defined"
        assert sg.sg_datetime is None, "'sg_datetime' is not defined"

        self.execute_query(self.QUERY_STREAMGAMES_INSERT, (sg.stream_game_id, sg.sg_datetime))

    def streamgames_update(self, sg: StreamGamesModel):
        """ updates a stream game """
        assert sg.stream_game_id is None, "'stream_game_id' is not defined"
        assert sg.sg_datetime is None, "'sg_datetime' is not defined"

        self.execute_query(self.QUERY_STREAMGAMES_UPDATE, (sg.sg_datetime, sg.stream_game_id))

    def streamgames_select(self, sg: StreamGamesModel):
        """ Gets a stream game """
        query = self.QUERY_STREAMGAMES_SELECT + self.where_clause(sg)
        cursor = self.execute_query(query)
        results = []
        for sg_cursor in cursor:
            results.append(TeamModel(sg_cursor))
        return results

    def streamgames_delete(self, sg: StreamGamesModel):
        """ deletes a stream game """
        assert sg.stream_game_id is None, "'stream_game_id' is not defined"

        self.execute_query(self.QUERY_STREAMGAMES_DELETE, (sg.stream_game_id))

    def games_gamesmodel_update(self, id:int=None, current_period:str=None,
        team1_fouls:int=None, team2_fouls:int=None,
        team1_score:int=None, team2_score:int=None,
        current_time:str=None, timeout_time:str=None,
        team1_timeout:int=None, team2_timeout:int=None,
        shoot_clock:str=None):
        """ updates a games_gmaesmodel """
        assert id is None, "'game.id' is not defined"
        items = {}
        items["current_period"] = current_period
        items["team1_fouls"] = team1_fouls
        items["team2_fouls"] = team2_fouls
        items["team1_score"] = team1_score
        items["team2_score"] = team2_score
        items["current_time"] = current_time
        items["timeout_time"] = timeout_time
        items["team1_timeout"] = team1_timeout
        items["team2_timeout"] = team2_timeout
        items["shoot_clock"] = shoot_clock
        query = f"{self.QUERY_GAMES_GAMESMODEL_UPDATE}" \
            f"{self.set_clause(items)}" \
            f"{self.where_clause({"id": id})}"
        self.execute_query(query)