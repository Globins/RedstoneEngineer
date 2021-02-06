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
import pyautogui
import pygetwindow as gw

malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)
recordingsDirectory = malmoutils.get_recordings_directory(agent_host)
video_requirements = '<VideoProducer><Width>860</Width><Height>480</Height></VideoProducer>' if agent_host.receivedArgument("record_video") else ''
observation_size = 10

items=["red_flower white_tulip", "coal", "planks spruce", "planks birch", "planks dark_oak", "rabbit", "carrot", "potato", "brown_mushroom"]

def buildPositionList(items):
    positions=[]
    for item in items:
        positions.append((random.randint(-10,10), random.randint(-10,10)))
    return positions
def getSubgoalPositions(positions):
    goals=""
    for p in positions:
        goals += '<Point x="' + str(p[0]) + '" y="227" z="' + str(p[1]) + '" tolerance="1" description="Checkpoint" />'
    return goals



def initialize_inventory(agent_host):
  for i in range(0, 36):
    agent_host.sendCommand("chat /give @p fireworks 64 0 {Fireworks:{Flight:1}}")
  agent_host.sendCommand("chat /gamemode 0")
#
def boost(obs, agent_host):
  checkRocketPosition(obs, agent_host)
  agent_host.sendCommand("use 1")

def checkRocketPosition(obs, agent_host):
    '''Make sure our rockets, if we have any, is in slot 0.'''
    for i in range(1,39):
        key = 'InventorySlot_'+str(i)+'_item'
        if key in obs:
            item = obs[key]
=
            if item == 'fireworks':
                agent_host.sendCommand("swapInventoryItems 0 " + str(i))
                return
def launch(agent_host):
  minecraftWin = gw.getWindowsWithTitle('Minecraft 1.11.2')[0]
  minecraftWin.activate()
  agent_host.sendCommand("jump 1")
  agent_host.sendCommand("move 1")
  time.sleep(.5)
  pyautogui.press('enter')
  pyautogui.keyDown('space')
  time.sleep(.15)
  pyautogui.keyUp('space')
  pyautogui.press('enter')


def printInventory(obs):
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

def GetMissionXML(summary):
    ''' Build an XML mission string that uses the RewardForCollectingItem mission handler.'''
    
    positions = buildPositionList(items)
    
    return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + summary + '''</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,2*3,2;1;" />
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="4" z1="-50" x2="50" y2="3" z2="50" type="air" />   <!-- to clear old items-->
                    <DrawBlock x='0'  y='50' z='0' type='diamond_ore' />
                    <DrawEntity x="0" y="4" z="0" type="Cow" yaw="0"/>
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="150000"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Creative">
            <Name>Wright</Name>
            <AgentStart>
                <Placement x="0.5" y="52.0" z="0.5"/>
                <Inventory>
                  <InventoryItem slot='38' type='elytra'/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <ChatCommands/>
                <ObservationFromSubgoalPositionList>''' + getSubgoalPositions(positions) + '''
                </ObservationFromSubgoalPositionList>
                <ObservationFromFullInventory/>
                ''' + video_requirements + '''
            </AgentHandlers>
        </AgentSection>

    </Mission>'''



# Create a pool of Minecraft Mod clients.
# By default, mods will choose consecutive mission control ports, starting at 10000,
# so running four mods locally should produce the following pool by default (assuming nothing else
# is using these ports):
validate = True
my_client_pool = MalmoPython.ClientPool()
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10001))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10002))
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10003))

if agent_host.receivedArgument("test"):
    num_reps = 1
else:
    num_reps = 1

for iRepeat in range(num_reps):
    my_mission = MalmoPython.MissionSpec(GetMissionXML("Flight #" + str(iRepeat)),validate)
    my_mission_record = MalmoPython.MissionRecordSpec() # Records nothing by default
    if recordingsDirectory:
        my_mission_record.recordRewards()
        my_mission_record.recordObservations()
        my_mission_record.recordCommands()
        if agent_host.receivedArgument("record_video"):
            my_mission_record.recordMP4(24,2000000)
        my_mission_record.setDestination(recordingsDirectory + "//" + "Mission_" + str(iRepeat + 1) + ".tgz")

    max_retries = 3
    for retry in range(max_retries):
        try:
            # Attempt to start the mission:
            agent_host.startMission( my_mission, my_client_pool, my_mission_record, 0, "Elytra Test" )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission",e)
                print("Is the game running?")
                exit(1)
            else:
                time.sleep(2)

    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()

    total_reward = 0
    # main loop:
    print("Starting Flight")
    initialize_inventory(agent_host)
    launch(agent_host)
    while world_state.is_mission_running:
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            boost(ob, agent_host)
        world_state = agent_host.getWorldState()
        
    # mission has ended.
    for error in world_state.errors:
        print("Error:",error.text)
    # if world_state.number_of_rewards_since_last_state > 0:
    #     reward = world_state.rewards[-1].getValue()
    #     print("Final reward: " + str(reward))
    #     total_reward += reward
    # print("Total Reward: " + str(total_reward))
    # if total_reward < expected_reward:  # reward may be greater than expected due to items not getting cleared between runs
    #     print("Total reward did not match up to expected reward - did the crafting work?")
    time.sleep(0.5) # Give the mod a little time to prepare for the next mission.
