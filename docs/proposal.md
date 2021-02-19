---
layout: default
title: Proposal
---

<b> Zoomer </b>
<b> Fast Gliding Through Obstacles </b> 

<b> Summary: </b>
	Our project is an AI that guides the player through a variety of objects as fast as possible using elytra. Glyder will use reinforcement learning to guide a player in a straight line using elytra without stopping, dying, or touching the floor. Glyder will be placed in a tube at the start of the game where it will need to navigate the randomly generated obstacles placed in front of it until it reaches the redstone and completes the level. 
    We will observe the space around our agent using the script agent_visibility.py. Then we will analyze the image to identify what is a solid object and what is an air block, i.e, where Glyder can pass through and what they will have to avoid (all blocks other than redstone). After analyzing the image of the world around and in front of him, the agent will move to the optimal gaps to reach the end of the goal using the mechanics of the elytra or firework rockets. If Glyder touches the bottom, top or sides of the tube, it will die just as it would if it touches any of the obstacles it needs to navigate. 


<b> AI/ML Algorithms: </b>
    Reinforcement Learning to know when it is going too fast (when to stop using fireworks to boost itself). The positive reward will be based on the time the agent has spent flying. The negative reward will be on whether the agent hits a block and dies.
<b> Evaluation Plan: </b>
    Quantitative Evaluation: 
	    For our quantitative evaluation, we will record the time period that the agent is able to stay alive for (without dying from kinetic energy or fall damage). Our base case is for the agent to survive for 45 seconds. As we continue to improve our agent, we will expect to see improvements in the time they survive every trial run.
<b> Qualitative Evaluation: </b>
	    For our qualitative evaluation, we will make sure that our AI makes it through the objects of different heights and widths eventually. 
        For our sanity checks, we will make sure that our agent is gliding in the air without touching the ground and hitting blocks. We expect the agent to be able to navigate through 4x4 squares. Eventually, we will try to improve our agent to be able to navigate through different shapes, sizes, and heights as well without crashing. Another sanity check we will use is to see how fast the agent can make it from one side to another. 


<b> Moonshot Case: </b>
        Our agent will be able to navigate through obstacles at low visibility (Light = 3 or lower), this will affect how the agent will see and react to certain obstacles.

<b> Weekly Meeting Time: </b>
    We plan on meeting at least once a week at this scheduled time: Fridays at 3:30pm PST + any additional appointments we may need to set up with each other in order to complete the project. 

<b> Status Report Update </b>
    By the time the status report is due, we plan on having our agent capable of flying through an empty, pre-created world and hit a redstone block/hoop at the end. This will show us that our agent is both capable of flying/gliding and it is capable of reaching the game’s end goal. 
	
<b> Appointment with the Instructor: </b>
	We scheduled a second meeting for Friday (01/22/2021) at 4:45 PM.

