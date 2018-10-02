#!/usr/bin/python3
# Head to head lockboard challenge script
# Writen by: Graph-X 
 
import pifacedigitalio as pfd


board_one = [0,1,2]
board_two = [3,4,5]
player_one = 0
player_two = 0
pf = pfd.PiFaceDigital()

	
def reset(event):
	global board_one
	global board_two
	global player_one
	global player_two
	player_one = 0
	player_two = 0
	board_one = [0,1,2]
	board_two = [3,4,5]
	#turn off all the leds
	for i in range(0,7):
		pfd.leds[i].turn_off()
		
#when a player wins turn on the correct LED	
def player_win(player):
	if player == 1:
		#turn on led 6
		pfd.leds[6].turn_on()
	if player == 2:
		pfd.leds[7].turn_on()
		

def lock_open(event):
	global board_one
	global board_two
	global player_one
	global player_two
	
	pfd.leds[event.pin_num].turn_on()
	if event.pin_num in board_one:
		player_one += 1
		board_one.remove(event.pin_num)
		if player_one == 3:
			player_win(1)
	if event.pin_num in board_two:
		player_two += 1
		board_two.remove(even.pin_num)
		if player_two == 3:
			player_win(2)


# registers that a lock has been closed.
def lock_closed(event):
	global board_one
	global board_two
	global player_one
	global player_two
	
	pfd.leds[event.pin_num].turn_off()
	if event.pin_num in [0,1]:
		board_one.add(event.pin_num)
		player_one -= 1
		print("Player one has closed a lock.")
	if event.pin_num in [3,4]:
		board_two.add(event.pin_num)
		player_two -= 1
		print("Player two has closed a lock.")

# basically the main function but I called it listen. 
def listen():
	#setup the listeners
	listener = pfd.InputEventListener(chip=pf)
	for i in [0,1,3,4]:
		listener.register(i, pfd.IODIR_RISING_EDGE, lock_open)
		listener.register(i, pfd.IODIR_FALLING_EDGE, lock_closed)
	for i in [2,5]:
		listener.register(i, pfd.IODIR_FALLING_EDGE, lock_open)
		
	#reset button listener
	listener.register(6, pfd.IODIR_FALLING_EDGE, reset)
	listener.activate()
	
	
if __name__ == "__main__":
	listen()
	
