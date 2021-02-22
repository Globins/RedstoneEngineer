from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

from builtins import range
import MalmoPython
import os
import random
import sys
import time
import json
import random
import errno
import malmoutils
import gym, ray
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint
from gym.spaces import Discrete, Box
from ray.rllib.agents import ppo
from sys import platform


malmoutils.fix_print()
class Zoomer(gym.Env):
    def __init__(self, env_config):  
        # Static Parameters
        self.size = 50
        self.reward_density = .1
        self.penalty_density = .02
        self.obs_size = 5
        self.max_episode_steps = 100
        self.log_frequency = 10
        
        self.action_dict = {
            0: 'move 1',  # Move one block forward
            1: 'turn 1',  # Turn 90 degrees to the right
            2: 'turn -1',  # Turn 90 degrees to the left
            3: 'attack 1'  # Destroy block
        }

        # Rllib Parameters
        self.action_space = Box(-.05,.05, shape = (3,), dtype = np.float32)
        self.observation_space = Box(0, 1, shape=(2 * self.obs_size * self.obs_size, ), dtype=np.float32)

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

        # DiamondCollector Parameters
        self.obs = None
        self.allow_move_action = False
        self.episode_step = 0
        self.episode_return = 0
        self.returns = []
        self.steps = []
        malmoutils.parse_command_line(self.agent_host)
        self.recordingsDirectory = malmoutils.get_recordings_directory(self.agent_host)
        self.video_requirements = '<VideoProducer><Width>860</Width><Height>480</Height></VideoProducer>' if self.agent_host.receivedArgument("record_video") else ''

    def reset(self):
        """
        Resets the environment for the next episode.

        Returns
            observation: <np.array> flattened initial obseravtion
        """
        # Reset Malmo
        world_state = self.init_malmo()

        # Reset Variables
        self.returns.append(self.episode_return)
        current_step = self.steps[-1] if len(self.steps) > 0 else 0
        self.steps.append(current_step + self.episode_step)
        self.episode_return = 0
        self.episode_step = 0

        # Log
        if len(self.returns) > self.log_frequency + 1 and \
            len(self.returns) % self.log_frequency == 0:
            self.log_returns()

        # Get Observation
        self.obs, self.allow_move_action = self.get_observation(world_state)
        
        return self.obs

    def step(self, action):
        """
        Take an action in the environment and return the results.

        Args
            action: <int> index of the action to take

        Returns
            observation: <np.array> flattened array of obseravtion
            reward: <int> reward from taking action
            done: <bool> indicates terminal state
            info: <dict> dictionary of extra information
        """
        # Get Action 

        if self.allow_move_action or action[2] < 0:
            self.agent_host.sendCommand('pitch {}'.format(action[0]))
            self.agent_host.sendCommand('turn {}'.format(action[1]))
            time.sleep(.2)
        else:
            self.boost()
        self.episode_step +=1
        

        # Get Observation
        world_state = self.agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
        self.obs, self.allow_move_action = self.get_observation(world_state) 
        # Get Done
        done = not world_state.is_mission_running 

        # Get Reward
        reward = 0
        for r in world_state.rewards:
            reward += r.getValue()
        self.episode_return += reward
        print("REWARD" 
            + str(reward))
        return self.obs, reward, done, dict()

    
    def GenCuboid(self, x1, y1, z1, x2, y2, z2, blocktype,color):
        if color == "":
            return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'
        else:
            return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '" colour="'+color+'"/>'
        
    def GenBlock(self, x1, y1, z1, blocktype):
        return '<DrawBlock x="' + str(x1) + '" y="' + str(y1) + '" z="' + str(z1) + '" type="' + blocktype + '"/>'
    
    def line(self, x0, y0, x1, y1):
        #"Bresenham's line algorithm"
        points_in_line = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                points_in_line.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                points_in_line.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points_in_line.append((x, y))
        return points_in_line

#-----------------------------------------------------------------------------------------------------
    def GetMissionXML(self, summary):
        ''' Build an XML mission string.'''
        courseHalfWidth = 16

        obstSpawnMinY = 6
        obstSpawnMaxY = 49

        minObstacleAmount = 5
        maxObstacleAmount = 15
        horizChance = 70
        diagChance = 15
        obstacleCourseLength = 300

        obstacleGap = 10
        obstacleStart = 10
        playerStart = 0
        loopCount = obstacleStart

        obsString = ""
        checkptReward = ""
        while(loopCount < obstacleCourseLength):
            for _ in range(random.randint(minObstacleAmount,maxObstacleAmount)):
                xA = random.randint(-courseHalfWidth,courseHalfWidth)
                xB = random.randint(-courseHalfWidth,courseHalfWidth)
                yA = random.randint(obstSpawnMinY,obstSpawnMaxY)
                yB = random.randint(obstSpawnMinY,obstSpawnMaxY)
                roll = random.randint(0,99)
                if(roll <  diagChance):
                    resultLine = self.line(xA, yA, xB, yB)
                    for x,y in resultLine:
                        obsString += "<DrawBlock x = '{}' y = '{}' z = '{}' type='wool' colour='BLUE'/>".format(x, y, loopCount)
                elif(roll < horizChance):
                    obsString += "<DrawCuboid x1 = '{}' y1 = '{}' z1 = '{}' x2 = '{}' y2 = '{}' z2 = '{}' type='wool' colour='BLUE'/>".format(xA, yA, loopCount, xB, yA, loopCount)
                else:
                    obsString += "<DrawCuboid x1 = '{}' y1 = '{}' z1 = '{}' x2 = '{}' y2 = '{}' z2 = '{}' type='wool' colour='BLUE'/>".format(xA, yA, loopCount, xA, yB, loopCount)

            for x in range(-courseHalfWidth, courseHalfWidth):
                for y in range(obstSpawnMaxY):
                    checkptReward += "<Marker x='{}' y='{}' z='{}' reward='{}' tolerance='{}' />".format(x, y, loopCount+1, 1, 0)
            loopCount += obstacleGap
        obstacleCourseXML = ""
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='4' z1='{}' x2='{}' y2='50' z2='{}' type='air'/>".format(-obstacleCourseLength, -obstacleCourseLength, obstacleCourseLength, obstacleCourseLength)
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='{}' z1='{}' x2='{}' y2='{}' z2='{}' type='obsidian'/>".format(-courseHalfWidth-1, 1, playerStart-5, courseHalfWidth, obstSpawnMaxY+1, playerStart-5) #Backwall
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='{}' z1='{}' x2='{}' y2='{}' z2='{}' type='obsidian'/>".format(courseHalfWidth, 4, playerStart-5, courseHalfWidth, obstSpawnMaxY+1, obstacleCourseLength) #left wall
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='{}' z1='{}' x2='{}' y2='{}' z2='{}' type='obsidian'/>".format(-courseHalfWidth-1, 4, playerStart-5, -courseHalfWidth-1, obstSpawnMaxY+1, obstacleCourseLength) #right wall
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='{}' z1='{}' x2='{}' y2='{}' z2='{}' type='glass'/>".format(-courseHalfWidth-1, obstSpawnMaxY+1, playerStart-5, courseHalfWidth, obstSpawnMaxY+1, obstacleCourseLength) #ceiling
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='{}' z1='{}' x2='{}' y2='{}' z2='{}' type='lava'/>".format(-courseHalfWidth-1, 1, playerStart-5, courseHalfWidth, 3, obstacleCourseLength) #floor
        obstacleCourseXML += "<DrawCuboid x1='{}' y1='{}' z1='{}' x2='{}' y2='{}' z2='{}' type='redstone_block'/>".format(-courseHalfWidth-1, 4, obstacleCourseLength, courseHalfWidth, obstSpawnMaxY+1, obstacleCourseLength) #end wall
        obstacleCourseXML += "<DrawBlock x='{}'  y='14' z='{}' type='emerald_block'/>".format(playerStart, playerStart)
        
        playerSpawn = "<Placement x='{}' y='15.0' z='{}'/>".format(playerStart+.5, playerStart+.9)
        return '''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>''' + summary + '''</Summary>
            </About>

            <ServerSection>
                <ServerInitialConditions>
                  <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                  </Time>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;7,2*3,2;1;" />
                    <DrawingDecorator>
                    ''' + obstacleCourseXML + obsString + '''
                        <DrawEntity x="0" y="5" z="0" type="Cow" yaw="0"/>
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="150000"/>
                    <ServerQuitWhenAnyAgentFinishes />
                </ServerHandlers>
            </ServerSection>

            <AgentSection mode="Creative">
                <Name>Wright</Name>
                <AgentStart>
                    '''+ playerSpawn + '''
                    <Inventory>
                    <InventoryItem slot='38' type='elytra'/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                    <ContinuousMovementCommands turnSpeedDegs="480"/>
                    <ChatCommands/>
                    <ObservationFromFullStats/>
                    <ObservationFromRay/>
                    <ObservationFromGrid>
                        <Grid name="floorAll">
                            <min x="-'''+str(int(self.obs_size/2))+'''" y="-1" z="-'''+str(int(self.obs_size/2))+'''"/>
                            <max x="'''+str(int(self.obs_size/2))+'''" y="0" z="'''+str(int(self.obs_size/2))+'''"/>
                        </Grid>
                    </ObservationFromGrid>
                    <ObservationFromFullInventory/>
                    ''' + self.video_requirements + '''
                    <RewardForTouchingBlockType>
                        <Block type="lava" reward="-50" />
                        <Block type="redstone_block" reward="1000" />
                        <Block type="obsidian" reward="-50" />
                        <Block type="wool" reward="-10" />
                        <Block type="glass" reward="-50" />
                    </RewardForTouchingBlockType>
                    <RewardForReachingPosition>
                        ''' + checkptReward + '''
                    </RewardForReachingPosition>
                    <AgentQuitFromTouchingBlockType>
                        <Block type="redstone_block"/>
                    </AgentQuitFromTouchingBlockType>
                </AgentHandlers>
            </AgentSection>

        </Mission>'''
    #ELYTRA------------------------------------------------------------------------------------------------
    def initialize_inventory(self):
        self.agent_host.sendCommand("chat /gamemode 0")
        self.agent_host.sendCommand("chat /give @p diamond_helmet 1 0 {ench:[{id:0,lvl:4},{id:34,lvl:3}]}")
        self.agent_host.sendCommand("use 1")
        time.sleep(.2)
        self.agent_host.sendCommand("chat /give @p diamond_leggings 1 0 {ench:[{id:0,lvl:4},{id:34,lvl:3}]}")
        self.agent_host.sendCommand("use 1")
        time.sleep(.2)
        self.agent_host.sendCommand("chat /give @p diamond_boots 1 0 {ench:[{id:0,lvl:4},{id:34,lvl:3}]}")
        self.agent_host.sendCommand("use 1")
        time.sleep(.2)
        for i in range(0, 36):
            self.agent_host.sendCommand("chat /give @p fireworks 64 0 {Fireworks:{Flight:1}}")


    def boost(self):
        self.agent_host.sendCommand("use 1")
        self.agent_host.sendCommand("use 0")

    def checkRocketPosition(self, obs):
        '''Make sure our rockets, if we have any, is in slot 0.'''
        for i in range(1,39):
            key = 'InventorySlot_'+str(i)+'_item'
            if key in obs:
                item = obs[key]
                print(item == 'fireworks')
                if item == 'fireworks':
                    self.agent_host.sendCommand("swapInventoryItems 0 " + str(i))
                    return

    def launch(self):
        if (platform == "linux" or platform == "macOS"):
            pass
        elif(platform == "win32"):
            import pyautogui
            import pygetwindow as gw
            minecraftWin = gw.getWindowsWithTitle('Minecraft 1.11.2')[0]
            minecraftWin.activate()
            self.agent_host.sendCommand("jump 1")
            self.agent_host.sendCommand("move 1")
            time.sleep(.5)
            pyautogui.press('enter')
            pyautogui.keyDown('space')
            time.sleep(.15)
            pyautogui.keyUp('space')
            pyautogui.press('enter')


    def printInventory(self, obs):
        for i in range(0,9):
            key = 'InventorySlot_'+str(i)+'_item'
            var_key = 'InventorySlot_'+str(i)+'_variant'
            col_key = 'InventorySlot_'+str(i)+'_colour'
            if key in obs:
                item = obs[key]
                print(str(i) + " ------ " + item, end=' ')
            else:
                print(str(i) + " -- ", end=' ')
            if var_key in obs:
                print(obs[var_key], end=' ')
            if col_key in obs:
                print(obs[col_key], end=' ')
            print()
    
    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        validate = True
        my_client_pool = MalmoPython.ClientPool()
        my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
        my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))
        my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10002))
        my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10003))

        if self.agent_host.receivedArgument("test"):
            num_reps = 1
        else:
            num_reps = 1

        my_mission = MalmoPython.MissionSpec(self.GetMissionXML("Flight #1"),validate)
        my_mission_record = MalmoPython.MissionRecordSpec() # Records nothing by default
        if self.recordingsDirectory:
            my_mission_record.recordRewards()
            my_mission_record.recordObservations()
            my_mission_record.recordCommands()
            if self.agent_host.receivedArgument("record_video"):
                my_mission_record.recordMP4(24,2000000)
            my_mission_record.setDestination(self.recordingsDirectory + "//" + "Mission_2.tgz")
        
        max_retries = 3
        for retry in range(max_retries):
            try:
                # Attempt to start the mission:
                self.agent_host.startMission( my_mission, my_client_pool, my_mission_record, 0, "Zoomer" )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission",e)
                    print("Is the game running?")
                    exit(1)
                else:
                    time.sleep(2)
            
        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:",error.text)


        # main loop:
        print("Starting Flight")
        self.initialize_inventory()
        self.launch()
            
        # mission has ended.
        
        
        time.sleep(0.5) # Give the mod a little time to prepare for the next mission.
        
        return world_state

    def get_observation(self, world_state):
        obs = np.zeros((2 * self.obs_size * self.obs_size, ))
        allow_move_action = False
        while world_state.is_mission_running:
            time.sleep(0.3)
            world_state = self.agent_host.getWorldState()
            if len(world_state.errors) > 0:
                raise AssertionError('Could not load grid.')
            
            if world_state.number_of_observations_since_last_state > 0:
                msg = world_state.observations[-1].text
                
                observations = json.loads(msg)
                grid = observations['floorAll']
           
                for i, x in enumerate(grid):
                    obs[i] = x == "wool" or x == "lava"
                obs = obs.reshape((2, self.obs_size, self.obs_size))
                
                # yaw = observations['Yaw']
                # if yaw >= 225 and yaw < 315:
                #     obs = np.rot90(obs, k=1, axes=(1, 2))
                # elif yaw >= 315 or yaw < 45:
                #     obs = np.rot90(obs, k=2, axes=(1, 2))
                # elif yaw >= 45 and yaw < 135:
                #     obs = np.rot90(obs, k=3, axes=(1, 2))
                obs = obs.flatten()
                if('LineOfSight' in observations):
                    allow_move_action = observations['LineOfSight']['type'] == "wool" or observations['LineOfSight']['type'] == "lava"
                self.checkRocketPosition(observations)
                break

        return obs, allow_move_action


    def log_returns(self):
        """
        Log the current returns as a graph and text file

        Args:
            steps (list): list of global steps after each episode
            returns (list): list of total return of each episode
        """
        box = np.ones(self.log_frequency) / self.log_frequency
        returns_smooth = np.convolve(self.returns[1:], box, mode='same')
        plt.clf()
        plt.plot(self.steps[1:], returns_smooth)
        plt.title('Zoomer')
        plt.ylabel('Return')
        plt.xlabel('Steps')
        plt.savefig('returns.png')

        with open('returns.txt', 'w') as f:
            for step, value in zip(self.steps[1:], self.returns[1:]):
                f.write("{}\t{}\n".format(step, value)) 

if __name__ == '__main__':
    ray.init()
    trainer = ppo.PPOTrainer(env=Zoomer, config={
        'env_config': {},           # No environment parameters to configure
        'framework': 'torch',       # Use pyotrch instead of tensorflow
        'num_gpus': 0,              # We aren't using GPUs
        'num_workers': 0            # We aren't using parallelism
    })
    
    https://github.com/ray-project/ray/issues/7983
    #insert path that the training gets saved to
    # trainer.restore(path)

    i = 0
    while True:
        result = trainer.train()
        if i%10 == 0: #save every 10th training iteration
            checkpoint_path = trainer.save()
            print(checkpoint_path)
        i+=1