# Author: Eric Bartanen
# Description: ShipGame test suite

import unittest
from ShipGame import ShipGame

class TestShipGame(unittest.TestCase):

	"""Unit test for ShipGame"""

	def test_set_ships_out_of_order(self):
		""" Place ships doesnt require taking turns"""
		my_ship = ShipGame()
		my_ship.place_ship('first', 3, "A2", "R")
		my_ship.place_ship('first', 2, "B3", "C")
		my_ship.place_ship('second', 5, "H2", "R")
		my_ship.place_ship('second', 2, "F6", "C")
		first_result = my_ship.get_num_ships_remaining('first')
		second_result = my_ship.get_num_ships_remaining('second')

		self.assertEqual(first_result, 2)
		self.assertEqual(second_result, 2)

	def test_ship_too_short(self):
		""" ship must have at least lenght 2"""
		my_ship = ShipGame()
		my_ship.place_ship('first', 1, "A2", "R")

		first_result = my_ship.get_num_ships_remaining('first')
		self.assertEqual(first_result, 0)
		self.assertFalse(my_ship.place_ship('first', 1, "A2", "R"))

	def test_set_ships_overlap_self(self):
		"""A player cannot place a ship on a square where they already have a ship"""
		my_ship = ShipGame()
		my_ship.place_ship('first', 3, "A2", "R")
		my_ship.place_ship('first', 2, "A2", "C")
		my_ship.place_ship('second', 5, "H2", "R")
		my_ship.place_ship('second', 2, "F6", "C")

		first_result = my_ship.get_num_ships_remaining('first')
		second_result = my_ship.get_num_ships_remaining('second')
		self.assertEqual(first_result, 1)
		self.assertEqual(second_result, 2)
		self.assertFalse(my_ship.place_ship('first', 2, "A2", "C"))

	def test_set_ships_overlap_other_player(self):
		"""players have their own boards so can call the same coordinates"""
		my_ship = ShipGame()
		my_ship.place_ship('first', 3, "A2", "R")
		my_ship.place_ship('first', 2, "H6", "C")
		my_ship.place_ship('second', 3, "A2", "R")
		my_ship.place_ship('second', 2, "H6", "C")

		first_result = my_ship.get_num_ships_remaining('first')
		second_result = my_ship.get_num_ships_remaining('second')
		self.assertEqual(first_result, 2)
		self.assertEqual(second_result, 2)

	def test_set_ships_off_grid_column(self):
		"""Place ship that extends beyond last row"""
		my_ship = ShipGame()
		my_ship.place_ship('first', 3, "A10", "R")
		off_grid = my_ship.get_num_ships_remaining('first')
		self.assertEqual(off_grid, 0)
		self.assertFalse(my_ship.place_ship('first', 3, "A10", "R"))

	def test_set_ships_off_grid_row(self):
		"""Place ship that extends beyond last row"""
		my_ship = ShipGame()
		my_ship.place_ship('first', 3, "J10", "C")
		off_grid = my_ship.get_num_ships_remaining('first')
		self.assertEqual(off_grid, 0)
		self.assertFalse(my_ship.place_ship('first', 3, "J10", "C"))

	def test_player_one_wins(self):
		"""Player one wins. Player two takes a shot after win. """
		my_ship = ShipGame()

		my_ship.place_ship('first', 3, "A2", "R")
		my_ship.place_ship('second', 2, "F6", "R")

		my_ship.fire_torpedo('first', 'F6')
		my_ship.fire_torpedo('second', 'B3')

		my_ship.fire_torpedo('first', 'F7')
		shot_after_win = my_ship.fire_torpedo('second', 'C3')

		first_result = my_ship.get_num_ships_remaining('first')
		second_result = my_ship.get_num_ships_remaining('second')

		self.assertEqual(first_result, 1)
		self.assertEqual(second_result, 0)
		self.assertIs(my_ship.get_current_state(), 'FIRST_WON')
		self.assertFalse(shot_after_win)

	def test_fire_out_of_order(self):
		"""players shoot out of turn"""
		my_ship = ShipGame()

		my_ship.place_ship('first', 3, "A2", "R")
		my_ship.place_ship('second', 2, "F6", "R")

		my_ship.fire_torpedo('first', 'F6')
		out_of_order = my_ship.fire_torpedo('first', 'F7')

		my_ship.fire_torpedo('second', 'B3')
		my_ship.fire_torpedo('second', 'C3')

		first_result = my_ship.get_num_ships_remaining('first')
		second_result = my_ship.get_num_ships_remaining('second')
		self.assertEqual(first_result, 1)
		self.assertEqual(second_result, 1)
		self.assertIs(my_ship.get_current_state(), 'UNFINISHED')
		self.assertFalse(out_of_order)

	def test_fire_in_vain(self):
		"""fire at same coordinate and game play continues"""
		my_ship = ShipGame()

		first_shot = my_ship.place_ship('first', 3, "A2", "R")
		my_ship.place_ship('second', 2, "F6", "R")

		my_ship.fire_torpedo('first', 'F6')
		my_ship.fire_torpedo('second', 'A3')

		my_ship.fire_torpedo('first', 'F6')
		my_ship.fire_torpedo('second', 'A2')

		vain_shot = my_ship.fire_torpedo('first', 'F6')
		my_ship.fire_torpedo('second', 'A4')

		first_result = my_ship.get_num_ships_remaining('first')
		second_result = my_ship.get_num_ships_remaining('second')
		self.assertEqual(first_result, 0)
		self.assertEqual(second_result, 1)
		self.assertIs(my_ship.get_current_state(), 'SECOND_WON')
		self.assertTrue(vain_shot)
		self.assertTrue(first_shot)

if __name__ == '__main__':
	unittest.main()