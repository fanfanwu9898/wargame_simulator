from django.shortcuts import render
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context

from .models import User, Game, Round

from game_simulator.game_logic import WarGame, OutOfCardError
from game_simulator.generate_plot import generate_plot


def run_game_simulation(request, version, username_x, username_y, showhistory):
    if request.method == 'GET':
        if version == "v1":
            username_x, username_y = sorted([username_x, username_y])

            card_names = [str(i) for i in range(2, 11)] + ['J', 'Q', 'k', 'A']
            card_patterns = ['black-spades', 'black-clubs', 'red-hearts', 'red-diamonds']

            game = WarGame(username_x, username_y, card_names, card_patterns)

            try:
                winner, rounds, number_of_war_rounds, game_history = game.run_game_simulation()
            except OutOfCardError:
                return HttpResponse("Game Simulation Failed: run out of cards", status=204)

            load_into_database(winner, username_x, username_y, rounds, 
                    number_of_war_rounds, game_history)

            res = {            
                "winner":winner,
                "number_of_rounds":rounds,
                "number_of_war_rounds":number_of_war_rounds,
            }
            
            if showhistory == "showhistory":
                res['game_history'] = game_history

            return JsonResponse(res)

def run_multiple_game_simulations(request, version, username_x, username_y, number_of_games):
    if request.method == 'GET':
        if version == "v1":

            #
            username_x, username_y = sorted([username_x, username_y])

            card_names = [str(i) for i in range(2, 11)] + ['J', 'Q', 'k', 'A']
            card_patterns = ['black-spades', 'black-clubs', 'red-hearts', 'red-diamonds']

            username_x, username_y = sorted([username_x, username_y])

            game_res = []
            while number_of_games > 0:
                game = WarGame(username_x, username_y, card_names, card_patterns)

                try:
                    winner, rounds, number_of_war_rounds, game_history = game.run_game_simulation()
                    number_of_games -= 1

                    res = { "winner":winner,
                            "number_of_rounds":rounds,
                            "number_of_war_rounds":number_of_war_rounds,
                          }
                    game_res.append(res)

                    load_into_database(winner, username_x, username_y, rounds, 
                        number_of_war_rounds, game_history)

                except OutOfCardError:
                    pass

            return JsonResponse(game_res, safe = False)


# initialize GAME_ID every time I restart the server
if Game.objects.all().count() == 0:
    GAME_ID = 0
else:
    GAME_ID = Game.objects.order_by('-game_id')[0].game_id + 1

def load_into_database(winner, username_x, username_y, rounds, 
                number_of_war_rounds, game_history):
    global GAME_ID

    if User.objects.filter(username = winner).exists():
        user = User.objects.get(username = winner)
        user.number_of_wins += 1
        user.save()

    else:
        User(username = winner, 
             number_of_wins = 1
        ).save()
        
    Game(player_name_x = username_x, 
        player_name_y = username_y, 
        winner = winner,
        number_of_rounds = rounds,
        number_of_war_rounds = number_of_war_rounds,
        game_id = GAME_ID
    ).save()

    game_id_recorded = GAME_ID
    GAME_ID += 1

    for round_num, decks in game_history.items():
        Round(game_id = game_id_recorded,
              player_x_deck = decks[username_x],
              player_y_deck = decks[username_y],
              war_round = decks['war_round']
        ).save()


def get_lifetime_wins(request, version, username):
    if request.method == 'GET':
        if User.objects.filter(username = username).exists():
            user = User.objects.get(username = username)
            return JsonResponse({            
                    "username":user.username,
                    "number_of_wins":user.number_of_wins
                })
        else:
            return HttpResponse("Error: User does not exist", status=204)


def visualize_result(request, version, username_x, username_y):

    username_x, username_y = sorted([username_x, username_y])
    games = Game.objects.filter(player_name_x = username_x, player_name_y = username_y)

    number_of_games, stats_table, pie_chart_wins, \
        histogram_number_of_rounds, histogram_number_of_war_rounds, \
        scatter_plot_round = generate_plot(games, username_x, username_y)

    template = Template('''
                        <body>
                        <h2> Analyzing <span style="color:#FF0000"> {{number_of_games}} </span>
                            War Game Results for <span style="color:#FF0000"> {{ username_x }} </span>
                            and <span style="color:#FF0000">{{ username_y }} </span> </h2>
                        <div style="display: flex; justify-content: center">
                            <div>
                                {{ stats_table | safe }}
                            </div>

                            <div>
                                {{ pie_chart_wins | safe }}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: center">
                            <div>
                                {{ histogram_number_of_rounds | safe }}
                            </div>
                            <div>
                                {{ histogram_number_of_war_rounds | safe }}
                            </div>
                        </div>
                        <div style = "display: flex;  justify-content: center">
                            {{ scatter_plot_round | safe }}
                        </div>
                        </body>
                        ''')

    context = Context({
                "number_of_games" : number_of_games,
                "stats_table" : stats_table,
                "pie_chart_wins" : pie_chart_wins,
                "histogram_number_of_rounds" : histogram_number_of_rounds,
                "histogram_number_of_war_rounds" : histogram_number_of_war_rounds,
                "scatter_plot_round" : scatter_plot_round,
                "username_x" : username_x,
                "username_y" : username_y})

    return HttpResponse(template.render(context))





    