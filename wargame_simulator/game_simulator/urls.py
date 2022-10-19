from django.urls import path

from . import views

app_name = "querys"

urlpatterns = [
    path('lifetimewin/<str:version>/username/<str:username>', views.get_lifetime_wins, name = 'get_lifetime_wins'),
    path('simulation/<str:version>/usernamex/<str:username_x>/usernamey/<str:username_y>/<str:showhistory>', views.run_game_simulation, name = 'run_game_simulation'),
    path('simulations/<str:version>/usernamex/<str:username_x>/usernamey/<str:username_y>/<int:number_of_games>', views.run_multiple_game_simulations, name = 'run_multiple_game_simulations'),
    path('visualization/<str:version>/usernamex/<str:username_x>/usernamey/<str:username_y>', views.visualize_result, name = 'visualize_result'),
]