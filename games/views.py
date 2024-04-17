from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from games.models import Game

CLICK_TIMES = 500
MIN_CLICKS_STRING = "00000000"
MAX_CLICKS = 99999999
EARN_GOLD_REWARD = 1000
COUNT_PER_CLICK = 100


@login_required
def earn_gold_by_clicking_game(request):
    context = {}

    user_character = request.user.character

    game = Game.objects.get(gold_to_gain=EARN_GOLD_REWARD)
    if game:
        game_message = f'Click on the button {CLICK_TIMES} times to earn {EARN_GOLD_REWARD} gold.'
        context['game_message'] = game_message

    if request.method == "GET":
        user_character.current_clicks = 0
        user_character.save()
    elif request.method == "POST":
        if game:
            if user_character.current_clicks + COUNT_PER_CLICK >= MAX_CLICKS:
                user_character.current_clicks = 0
            user_character.current_clicks += COUNT_PER_CLICK
            if user_character.current_clicks % CLICK_TIMES == 0:
                user_character.gold += EARN_GOLD_REWARD
                success_message = f'You earned {EARN_GOLD_REWARD} gold!'
                context['success_message'] = success_message

            user_character.save()

    clicks_to_string = MIN_CLICKS_STRING[:len(MIN_CLICKS_STRING) - len(str(user_character.current_clicks))] + str(
        user_character.current_clicks)
    context['clicks_to_string'] = clicks_to_string

    return render(request, 'games/earn_gold_by_clicking_game.html', context)
