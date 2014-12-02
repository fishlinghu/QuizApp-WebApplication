# -*- coding: utf-8 -*-

from views import Handler
from setting import checkPlayerName
from users import checkPlayer

class FriendHandler(Handler):
    def render_homepage(self, **kw):
        self.render("friend.html", **kw)

    def get(self):
        user = self.session.get('QUIZAPP_USER')
        if user:
            # Get the player
        	q = Player.all()
        	q.filter('player_ID = ', user)
        	player = q.fetch(1)

        	# Get the list of friends' names
        	q = Player.all()
        	friend_name_list = []
        	for friend_ID in player.friend_list:
        		q = Player.all()
        		q.filter('player_ID = ', friend_ID)
        		friend = q.fetch(1)
        		friend_name_list.append(friend.name)

        	 template_values = {
            	'friend_name_list': friend_name_list
              	}

            self.render("friend.html", **template_values)
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.render_homepage()

    def post(self):
    	# Used to add new friends
    	# Maybe we can implement the features like both users have to agree on the friendship
    	# Then the adding will be successful for both users
    	# But here I just try to implement a simple version
    	# You can just add other user to your friends list by entering their name or id
    	user = self.session.get('QUIZAPP_USER')
        if user:
            # Get the player
        	q = Player.all()
        	q.filter('player_ID = ', user)
        	player = q.fetch(1)

        	# Add the player as friend by name
        	friend_name = self.request.get('friend_name')
        	friend = checkPlayerName(friend_name)
        	if friend:
        		# There is such player
        		player.friend_list.append(friend.player_ID)
        	else:
        		self.write_plain("Sorry, no such player")

        	# Add the player as friend by id
        	friend_ID = self.request.get('friend_ID')
        	friend = checkPlayer(friend_ID)
        	if friend:
        		player.friend_list.append(friend_ID)
        	else:
        		self.write_plain("Sorry, no such player")

        	# Unfriend the player by name
        	friend_name_del = self.request.get('friend_name_del')
        	friend = checkPlayerName(friend_name_del)
        	if friend:
        		# There is such player
        		if friend.player_ID in player.friend_list:
        			# okay he is your friend
        			player.friend_list.remove(friend.player_ID)
        		else
        			self.write_plain("This player is not your friend!")
        	else:
        		self.write_plain("Sorry, no such player")

        	# Unfriend the player by id
        	friend_ID_del = self.request.get('friend_ID_del')
        	friend = checkPlayer(friend_ID_del)
        	if friend:
        		if friend_ID_del in player.friend_list:
        			# Okay he is your friend
        			player.friend_list.remove(friend_ID_del)
        		else:
        			self.write_plain("This player is not your friend!")
        	else:
        		self.write_plain("Sorry, no such player")

        	player.put()
			self.redirect('/friend')

        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.render_homepage()