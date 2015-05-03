# cse30332_final_project
Final Programming Paradigms Project (Creature Battler)

(Very) Rough Outline:

Creature Class:
  Variables:
    Health
    MP (number of points for an attack in order to limit the use of the ultimate attack)
    Attack Power
    Defense
    images for animation, etc. 
  Methods:
    Movement function
    primary attack function
    ultimate attack function
    general function used to update stats, state, etc.
    
Player Class:
  Variables:
    Player Creature
    Enemy Creature
    information used for making the connection to the game server
  Methods:
    method for interpretting user input and feeding that input to the creature
    method for sending information across the connection
    method for receiving and interpretting information from the connection
    
Server:
  Similar to the Twisted Primer in that there are multiple classes for handling the different connections and a deferred queue to bridge the connections.
  Connections:
    Player 1 to server
    Player 2 to server
  
High Level Overview:
  Players will initialize their game clients, choose their creature, then wait until the server connects them with another player.  Each player's client then initialize an enemy creature whose movements will be controlled by the other player via the bridged connection.  
  
Creature Types:
  Fire:
    Very Fast (can move two spaces instead of 1)
    Primary Attack = Fireball (moderate amount of damage)
    Ultimate Attack = Pyroblast (Very high amount of damage, but completely drains MP)
    Least amount of health among the 3 creatures
    
  Water:
    Highest defense
    Primary Attack = Ice Lance (low amount of damage)
    Ultimate Attack = Frost Nova (freezes the enemy creature for 3 rounds, drains .5 of MP)
  
  Grass:
    Highest Health, lowest defense
    Primary Attack = Vine whip (average amount of damage, slightly leses than fireball)
    Ultimate Attack = Giga Drain (does a low amount of damage initially, but then drains the enemies health and restores your health for 3 turns)
    
    
    
