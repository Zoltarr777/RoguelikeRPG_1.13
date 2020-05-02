import tcod as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder
from item_functions import cast_magic
from components.item import Item

def get_constants():
	window_title = "Roguelike RPG"

	screen_width = 80
	screen_height = 50

	bar_width = 20
	panel_height = 7
	panel_y = screen_height - panel_height

	message_x = bar_width + 2
	message_width = screen_width - bar_width - 2
	message_height = panel_height - 1

	map_width = screen_width#80
	map_height = screen_height - panel_height#43

	room_max_size = 10
	room_min_size = 6
	max_rooms = 30

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10

	max_monsters_per_room = 3
	max_items_per_room = 2

	kill_count = 0

	wall_tile = 256
	floor_tile = 257
	player_tile = 258
	orc_tile = 259
	troll_tile = 260
	scroll_tile = 261
	healing_potion_tile = 262
	sword_tile = 263
	shield_tile = 264
	stairs_tile = 265
	dagger_tile = 266
	magic_wand_tile = 267
	greater_healing_potion_tile = 268
	ghost_tile = 269
	slime_tile = 270
	corpse_tile = 271
	goblin_tile = 272
	baby_slime_tile = 273
	skeleton_tile = 274
	slime_corpse_tile = 275
	baby_slime_corpse_tile = 276

	colors = {
			'dark_wall': libtcod.Color(36, 36, 36),
			'dark_ground': libtcod.Color(40, 51, 35),
			'light_wall': libtcod.Color(130, 110, 50),
			'light_ground': libtcod.Color(200, 180, 50)
	}

	constants = {
		'window_title': window_title,
		'screen_width': screen_width,
		'screen_height': screen_height,
		'bar_width': bar_width,
		'panel_height': panel_height,
		'panel_y': panel_y,
		'message_x': message_x,
		'message_width': message_width,
		'message_height': message_height,
		'map_width': map_width,
		'map_height': map_height,
		'room_max_size': room_max_size,
		'room_min_size': room_min_size,
		'max_rooms': max_rooms,
		'fov_algorithm': fov_algorithm,
		'fov_light_walls': fov_light_walls,
		'fov_radius': fov_radius,
		'max_monsters_per_room': max_monsters_per_room,
		'max_items_per_room': max_items_per_room,
		'colors': colors,
		'kill_count': kill_count,
		'wall_tile': wall_tile,
		'floor_tile': floor_tile,
		'player_tile': player_tile,
		'orc_tile': orc_tile,
		'troll_tile': troll_tile,
		'scroll_tile': scroll_tile,
		'healing_potion_tile': healing_potion_tile,
		'sword_tile': sword_tile,
		'shield_tile': shield_tile,
		'stairs_tile': stairs_tile,
		'dagger_tile': dagger_tile,
		'magic_wand_tile': magic_wand_tile,
		'greater_healing_potion_tile': greater_healing_potion_tile,
		'ghost_tile': ghost_tile,
		'slime_tile': slime_tile,
		'corpse_tile': corpse_tile,
		'goblin_tile': goblin_tile,
		'baby_slime_tile': baby_slime_tile,
		'skeleton_tile': skeleton_tile,
		'slime_corpse_tile': slime_corpse_tile,
		'baby_slime_corpse_tile': baby_slime_corpse_tile
	}

	return constants

def get_game_variables(constants):
	fighter_component = Fighter(hp=100, defense=1, power=2, magic=0, magic_defense=1, talismanhp=0, gold=0)
	inventory_component = Inventory(26)
	equipment_inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()
	player = Entity(0, 0, constants['player_tile'], libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, 
		inventory=inventory_component, level=level_component, equipment=equipment_component, equipment_inventory=equipment_inventory_component)
	entities = [player]

	gold_value = 1
	equipment_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=1, gold=gold_value)
	dagger = Entity(0, 0, constants['dagger_tile'], libtcod.white, "Terrium Dagger (+1 atk)", equippable=equipment_component)
	player.equipment_inventory.add_item(dagger)
	player.equipment.toggle_equip(dagger)

	gold_value = 2
	item_component = Item(use_function=cast_magic, damage=2, maximum_range=3, gold=gold_value)
	magic_wand = Entity(0, 0, constants['magic_wand_tile'], libtcod.white, "Magic Wand", item=item_component)
	player.inventory.add_item(magic_wand)

	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], 
		constants['map_height'], player, entities, constants['orc_tile'], constants['healing_potion_tile'], constants['scroll_tile'], 
		constants['troll_tile'], constants['stairs_tile'], constants['sword_tile'], constants['shield_tile'], constants['dagger_tile'], 
		constants['magic_wand_tile'], constants['greater_healing_potion_tile'], constants['ghost_tile'], constants['slime_tile'], 
		constants['corpse_tile'], constants['goblin_tile'], constants['baby_slime_tile'], constants['skeleton_tile'], 
		constants['slime_corpse_tile'], constants['baby_slime_corpse_tile'])

	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

	game_state = GameStates.PLAYERS_TURN

	return player, entities, game_map, message_log, game_state