
import logging

import constants
import requests

from cogs.points.chat_points import get_chatpoints_leaderboard


logging.info('Uploading ChatPoints leaderboard to Firebase')
leader_board = get_chatpoints_leaderboard()[10:]
requests.put(f'https://{constants.firebase_url}/discordstats/chatpoints.json', \
    json=leader_board, headers={"Content-Type": "application/json"})