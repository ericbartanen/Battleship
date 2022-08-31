# Author: Eric Bartanen
# Description: Battleship Game with 2 players on a 10x10 grid.

class ShipGame:
	"""
	Represents the two-player Ship Game (similar to Battleship). This game is played on a 10x10	grid. Players can
	create as many ships as they like as long as they are at least 2 squares long and entirely within the bounds
	of the grid. Ships can be placed in any order. However, the game begins with firing torpedoes and player one
	goes first, then players alternate game play. Players fire torpedoes attempting to sink their opponents ships.
	The winner is declared once all of a player’s ships are sunk.
	"""

	def __init__(self):
		"""
		ShipGame takes no parameters. Initialize data members:
		1) List (empty) of player one ships
		2) List (empty) of player two ships
		3) Player turn = "first"
		4) Game state = "UNFINISHED"
		"""

		self._player_one_ships = []
		self._player_two_ships = []
		self._player_turn = "first"
		self._game_state = "UNFINISHED"

	def place_ship(self, player, ship_length, coordinates, orientation):
		"""
		When a player places a ship, a new ship object is created in Ship class. The place_ship parameters, excluding
		player, are passed to the create_ship method, which checks that the ship being created follows the rules of
		the board (min. size, all coordinates within [A1:J10]).

		place_ship then checks that the new ship does not overlap any of player's existing ships. If this new ship
		does not overlap then it is added to the player's list of ships.

		:param player:
		:param ship_length:
		:param coordinates:
		:param orientation:
		:return:
		"""
		new_ship = Ship()
		new_ship.create_ship(ship_length, coordinates, orientation)
		ship_dimensions = new_ship.get_ship()

		if player == 'first':
			if ship_dimensions is None:
				return False

			if len(self._player_one_ships) == 0:
				self._player_one_ships.append(new_ship)
				return True

			# Compare each new coordinate with every existing coordinate in player's ships
			else:
				for coordinate in ship_dimensions:
					for ship in self._player_one_ships:
						if coordinate in ship.get_ship():
							return False
					else:
						continue
				self._player_one_ships.append(new_ship)
				return True

		if player == 'second':
			if ship_dimensions is None:
				return False

			if len(self._player_two_ships) == 0:
				self._player_two_ships.append(new_ship)
				return True

			# Compare each new coordinate with every existing coordinate in player's ships
			else:
				for coordinate in ship_dimensions:
					for ship in self._player_two_ships:
						if coordinate in ship.get_ship():
							return False
					else:
						continue
				self._player_two_ships.append(new_ship)
				return True

	def get_current_state(self):
		"""Returns current game state. Three options: 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'."""
		return self._game_state

	def fire_torpedo(self, player, coordinates):
		"""
		Allows a player to fire a torpedo at a coordinate, hoping that an enemy's ship is at that location.

		If player fires out of turn, return False.

		If game is finished, return False.

		Check enemy's list of ships to see if torpedo hit an occupied coordinate. If so, remove that coordinate from
		the ship's list of coordinates. Then, check if enemy still has ships, if not, update game state. Change player's
		turn and return True.

		:param player:
		:param coordinates:
		:return:
		"""
		if player is not self._player_turn:
			return False

		if self._game_state != 'UNFINISHED':
			return False

		else:
			if player == 'first':
				for ship in self._player_two_ships:

					# if torpedo hits ship, remove that coordinate from ship
					if coordinates in ship.get_ship():
						ship.ship_hit(coordinates)

					# if a ship's coordinates have all been removed, remove the ship from player's list of ships
					if len(ship.get_ship()) == 0:
						self._player_two_ships.remove(ship)

					# if enemy's ships are all gone, declare winner
					if len(self._player_two_ships) == 0:
						self._game_state = "FIRST_WON"

				# Change player's turn
				self._player_turn = 'second'
				return True

			if player == 'second':
				for ship in self._player_one_ships:

					# if torpedo hits ship, remove that coordinate from ship
					if coordinates in ship.get_ship():
						ship.ship_hit(coordinates)

					# if a ship's coordinates have all been removed, remove the ship from player's list of ships
					if len(ship.get_ship()) == 0:
						self._player_one_ships.remove(ship)

					# if enemy's ships are all gone, declare winner
					if len(self._player_one_ships) == 0:
						self._game_state = "SECOND_WON"

				# Change player's turn
				self._player_turn = 'first'
				return True

	def get_num_ships_remaining(self, player):
		"""Returns current number of ships 'player' has on their board"""
		if player == "first":
			return len(self._player_one_ships)
		if player == "second":
			return len(self._player_two_ships)


class Ship:
	"""
	This class represents a Ship to be used in the Ship game. Methods allow the creation of	ships, indicate damage
	from torpedoes, and share the full coordinates of each ship.
	"""

	def __init__(self):
		"""
		Initializes column and row headers, which together make the entire game board available as coordinates for
		a ship.

		Initializes ship to None. The create_ship method will turn this data member into a list of coordinates
		as long as the coordinated conform to the board rules.
		"""
		self._columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
		self._rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
		self._ship = None

	def create_ship(self, ship_length, coordinates, orientation):
		"""
		Creates a new ship object using ship_length, coordinates, and orientation.

		Controls that ship is minimum length and on the board but does not check if ship overlaps
		with an existing ship.
		"""
		if ship_length < 2:
			return False

		if coordinates[0] not in self._rows:
			return False

		if coordinates[1] not in self._columns:
			return False

		else:

			# Create new ship with vertical orientation
			if orientation == 'C':

				# Convert row letter to ASCII value, add ship length, then convert back to a letter
				end_row = chr(ord(coordinates[0]) + (ship_length - 1))

				if end_row not in self._rows:
					return False

				else:
					self._ship = []
					for i in range(ship_length):
						row = chr(ord(coordinates[0]) + i)
						self._ship.append(str(row + coordinates[1]))
					return True

			# Create new ship with horizontal orientation
			if orientation == 'R':

				# Find last column value by adding column coordinate and ship length as integers

				# Find end column for columns 0-9
				if len(coordinates) == 2:
					end_column = int(coordinates[1]) + int((ship_length - 1))

					if str(end_column) not in self._columns:
						return False

					else:
						self._ship = []
						for i in range(ship_length):
							column = int(coordinates[1]) + i
							self._ship.append(str(coordinates[0]) + str(column))
						return True

				# Find end column for column 10 (need to adjust for 2 digits in 10)
				if len(coordinates) == 3:
					end_column = 10 + int((ship_length - 1))

					if str(end_column) not in self._columns:
						return False

					else:
						self._ship = []
						for i in range(ship_length):
							column = int(coordinates[1]) + i
							self._ship.append(str(coordinates[0]) + str(column))
						return True

	def ship_hit(self, coordinates):
		"""
		Removes a coordinate from a ship's list of coordinates. To be used by the fire_torpedo method in ShipGame class.
		"""
		self._ship.remove(coordinates)

	def get_ship(self):
		"""
		Returns the ship's list of coordinates.
		"""
		return self._ship


def main():
	my_ship = ShipGame()

	my_ship.place_ship('first', 2, "A2", "C")

	my_ship.place_ship('second', 2, "H2", "R")

	print(my_ship.get_num_ships_remaining('first'))
	print(my_ship.get_num_ships_remaining('second'))

	my_ship.fire_torpedo('first', 'F6')
	my_ship.fire_torpedo('second', 'A2')

	my_ship.fire_torpedo('first', 'G6')
	my_ship.fire_torpedo('second', 'B2')

	print(my_ship.get_current_state())


if __name__ == "__main__":
	main()
