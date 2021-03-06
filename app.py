from datetime import timedelta
from flask import Flask, jsonify, make_response, request, current_app
from functools import update_wrapper

import requests
import sys
import MySQLdb
import feedparser
from bson import json_util
import json

sys.path.insert(0, './backend')
import nba_api

app = Flask(__name__)
#database connection
con = MySQLdb.connect('localhost', 'root', '', 'nba')
nba_api.initialize_id_map()

PLAYER_TYPE = 1
TEAM_TYPE = 2

# For Cors
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def doRequest(endpointUrl, params):
    """
    General purpose function which takes the endpoint URL and a list of different
    parameter fields which we will be using in the request. The parameter values
    will be obtained from the 'requests' module.

    @type endpointUrl: string
    @param endpointUrl: URL endpoint of the request
    @type params: List[string]
    @param params: List of parameters which will be passed to the request

    @rtype: jsonObject
    @return: the JSON object resulting from the request
    """
    finalUrl = endpointUrl
    for param in params:
        finalUrl = finalUrl + param + "=" + str(request.args.get(param)) + "&"
    finalUrl = finalUrl[:-1]
    print "<<<<<<OUTGOING REQUEST:>>>>>>>"
    print finalUrl
    requestJson = requests.get(finalUrl)
    return jsonify(requestJson.json())

@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'test_json_data': test_json_data})

# a players career stats
@app.route('/playercareerstats', methods=['GET'])
@crossdomain(origin='*')
def get_player_stats():
    endpointUrl = "http://stats.nba.com/stats/playercareerstats?"
    perMode = request.args.get("PerMode") or "PerGame"
    leagueID = request.args.get("LeagueID") or "00"
    player = request.args.get("Player")
    return jsonify(nba_api.get_player_career_stats(player, leagueID, perMode))

# shot chart info
@app.route('/shotchartdetail', methods=['GET'])
@crossdomain(origin='*')
def get_player_shot_chart():
    player = request.args.get("Player")
    season = request.args.get("Season")
    # filters
    shottype = request.args.get("ShotType")
    shotzone = request.args.get("ShotZone")
    shotarea = request.args.get("ShotArea")
    shotdist = request.args.get("ShotDist")
    return jsonify(nba_api.get_shotchart(player, season, shottype, shotzone, shotarea, shotdist))

# player radar
@app.route('/playerradar', methods=['GET'])
@crossdomain(origin='*')
def get_player_radar():
    player = request.args.get("Player")
    season = request.args.get("Season")
    return jsonify(nba_api.get_playerradar(player, season))

# returns all players ever played in the nba
@app.route('/commonallplayers', methods=['GET'])
@crossdomain(origin='*')
def get_all_players():
    return jsonify(nba_api.get_allplayers())

# return general info about player: height, weight, etc
@app.route('/commonplayerinfo', methods=['GET'])
@crossdomain(origin='*')
def get_player_info():
    player = request.args.get("Player")
    return jsonify(nba_api.get_playerinfo(player))

# returns general info about team: WL pct, team stats for each category (per game)
@app.route('/teaminfocommon', methods=['GET'])
@crossdomain(origin='*')
def get_team_info():
    season = request.args.get("Season")
    team = request.args.get("Team")
    seasontype = request.args.get("SeasonType") or "Regular Season"
    return jsonify(nba_api.get_teaminfo(season, team, seasontype))

# return team roster for a season
@app.route('/commonteamroster', methods=['GET'])
@crossdomain(origin='*')
def get_team_roster():
    season = request.args.get("Season")
    team = request.args.get("Team")
    team_roster = nba_api.get_teamroster(season, team)
    team_roster_withpics = nba_api.supplement_teamroster(team_roster)
    return jsonify(team_roster_withpics)


# return all players for a season
@app.route('/playersseason', methods=['GET'])
@crossdomain(origin='*')
def get_players_season():
    season = request.args.get("Season") or "2016-17"
    return jsonify(nba_api.get_playersseason(season))

@app.route('/follow_new_entity', methods=['GET'])
@crossdomain(origin='*')
def follow_new_entity():
    follow_type = request.args.get("type")
    follow_name = request.args.get("name")
    
    cursor = con.cursor()
    query = "INSERT INTO followings ( type, name) \
            VALUES ('%d', '%s')" % \
            (int(follow_type), follow_name)

    print query 
    try:
        cursor.execute(query)
        con.commit()
        return "success"
    except:
        con.rollback()
        print "Error inserting new following into database"
    return "fail"

@app.route('/get_followings', methods=['GET'])
@crossdomain(origin='*')
def get_followings():
    cursor = con.cursor()
    query = "SELECT * FROM followings"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print results
        return jsonify(results)
    except:
        print "Error querying the followings data"
        return jsonify("{status: failed}")

@app.route('/get_user_news', methods=['GET'])
@crossdomain(origin='*')
def get_user_news():
    cursor = con.cursor()
    query = "SELECT * FROM followings"
    news = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except:
        print "Error querying"
        return jsonify("{status: failed}")
    for follow in results:
      if follow[0] == PLAYER_TYPE:
        follow_news = get_player_news_helper(follow[1])["news"]
        print get_player_news_helper(follow[1])
      if follow[0] == TEAM_TYPE:
        follow_news = get_team_news_helper(follow[1])["news"]
      news = news + follow_news
    return jsonify({"news":news})

@app.route('/get_team_news', methods=['GET'])
@crossdomain(origin='*')
def get_team_news():
    team = request.args.get('Team')
    return jsonify(get_team_news_helper(team))

def get_team_news_helper(team):
    rss_link = 'http://www.nba.com/' + team.lower() + '/rss.xml'
    team_news = feedparser.parse(rss_link)
    newslist = []
    for newsitem in team_news["entries"]:
      print newsitem
      news = {}
      news["title"] = newsitem["title"]
      news["link"] = newsitem["link"]
      if 'summary' in newsitem:
        news["summary"] = newsitem["summary"]
      else:
        news["summary"] = ""
      newslist.append(news)
    return {"news":newslist}

@app.route('/get_player_news', methods=['GET'])
@crossdomain(origin='*')
def get_player_news():
    return jsonify(get_player_news_helper(request.args.get('Player')))

def get_player_news_helper(m_player):
    rss_link = "http://www.rotoworld.com/rss/feed.aspx?sport=nba&ftype=news&count=500&format=rss"
    all_news = feedparser.parse(rss_link)
    player_news = []
    if m_player:
        player = m_player.lower().replace("_", " ")
        for item in all_news["items"]:
            print item
            if player in str(item["title"]).lower():
                player_news.append({
                "title": item["title"],
                "summary": item["summary"],
                "link": item["link"]
                })
    else:
        for item in all_news["items"]:
            print item
            player_news.append({
                "title": item["title"],
                "summary": item["summary"],
                "link": item["link"]
            })
            
    return {"news": player_news}


@app.route('/playerpic', methods=['GET'])
@crossdomain(origin='*')
def get_player_pic():
    player = request.args.get("Player")
    return jsonify({"url":nba_api.get_playerpic(player)})

@app.route('/teampic', methods=['GET'])
@crossdomain(origin='*')
def get_team_pic():
    team = request.args.get("Team") or None
    return jsonify({"url":nba_api.get_teampic(team)})

@app.route('/leagueshotavg', methods=['GET'])
@crossdomain(origin='*')
def get_league_shotavg():
    season = request.args.get("Season") or None
    return jsonify(nba_api.get_league_shotavg(season))


@app.route('/getboxscore', methods=['GET'])
@crossdomain(origin='*')
def get_box_score():
    date = request.args.get("Date") or None
    teamOne = request.args.get("TeamOne") or None
    teamTwo = request.args.get("TeamTwo") or None
    return jsonify(nba_api.get_boxscore_summary(date, teamOne, teamTwo))

@app.route('/getgamesforday', methods=['GET'])
@crossdomain(origin='*')
def get_games_for_day():
    date = request.args.get("Date") or None
    return jsonify(nba_api.get_games_for_day(date))

@app.route('/leaderstiles', methods=['GET'])
@crossdomain(origin='*')
def get_leaders():
    season = request.args.get("Season") or "2016-17"
    stat = request.args.get("Stat")
    seasontype = request.args.get("SeasonType") or "Regular Season"
    playerscope = request.args.get("PlayerScope") or "All Players"
    playerorteam = request.args.get("PlayerOrTeam") or "Player"
    permode = request.args.get("PerMode") or "PerGame"

    return jsonify(nba_api.get_stats_leaders(season, seasontype, stat, playerscope, playerorteam, permode))

@app.route('/allleaders', methods=['GET'])
@crossdomain(origin='*')
def get_all_leaders():
    season = request.args.get("Season") or "2016-17"
    seasontype = request.args.get("SeasonType") or "Regular Season"
    playerscope = request.args.get("PlayerScope") or "All Players"
    playerorteam = request.args.get("PlayerOrTeam") or "Player"
    permode = request.args.get("PerMode") or "PerGame"

    return jsonify(nba_api.get_all_leaders(season, seasontype, playerscope, playerorteam, permode))


if __name__ == '__main__':
    app.run(debug=True)
