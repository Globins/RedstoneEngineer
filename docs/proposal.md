---
layout: default
title: Proposal
---

Proposal - Redstone:

Summary: 
    In Minecraft, you can create contraptions that will perform automated tasks for you using specialized redstone or related blocks. These can range from piston doors, auto-farmers, elevators or even flying vehicles. For many builders, these designs can be clunky and take up an unnecessary amount of space, making overall builds cramped and requiring excess material. The goal of RedstoneEngineer is to take a redstone design with its inputs and outputs, and optimize the circuitry behind it to reduce space while maintaining the original intended timings of the mechanism (i.e finding the shortest and most optimal path for the circuit). We can apply this AI to a multitude of applications that deal with Redstone circuits to make builds look nicer and to reduce excess material used in a design.


AI/ML Algorithms: 
We plan on using Reinforcement Learning on the agent’s ability to navigate through the redstone circuit quicker.
 

Evaluation Plan: 
    We will take several quantitative measurements to evaluate the performance of our AI. We will measure and keep track of the amount of time it takes the agent to complete the maze given a certain original redstone design/blueprint. We will also keep track of how much resources the AI uses in its design while maintaining the desired output. We will monitor both of these values to ensure that our agent is learning and improving their time and overall circuit  creation each time around (for the most part). As a part of our manual evaluation plan, we will complete the maze ourselves in order to find the most optimal solution for it and check that the agent is achieving the same result (or similarly optimal) in the end. 
    In order to ensure our Agent is working properly, we will begin by seeing whether the Agent ignores traps or opens unnecessary doors. From there, we will test whether the Agent starts fixing traps and ignoring certain doors to reach the end of the maze quicker. As part of a sanity check, we will record the changes the Agent makes every round it is run, and see if it is improving overall. We will know our Agent is working properly when it knows which doors to open and which traps to fix in order to get to the end in the quickest time possible.


Backup Proposal: CombatAI


Summary: 
	In Minecraft, you face off different kinds of enemies and players, and you can only fight given what’s in your inventory. For our AI, we will use different techniques and weaponry in response to different combat cues such as type of mob, if a player is using a shield, what kind of weapon the agent has, and what the player has in its hand. We will give the agent various weapons and spawn several close combat and long range creatures in front of the AI. We will then examine how long the AI survives, how many creatures it kills, and the experience level it has gained from the battles.

AI/ML Algorithms: 
We plan on using Reinforcement Learning on the agent’s ability to know when to use which weapon and when to retreat.
 
Evaluation Plan: 
	We will take several quantitative measurements to evaluate the performance of our AI. We plan on keeping track of how often our agent picks the correct weapon in battle against his opponent vs. how often it does not. We will also monitor the amount of health the agent has vs. his enemy in battle each round. Another measurement we will use is the amount of experience the AI has gotten (based off of the level bar near the health); the greater the experience, the better the AI performed. The fourth and final value we will keep track of is the length of time our agent survives each round. These numbers will give us an idea of how much the agent is learning and improving in each round. 
	In order to ensure that our agent is on the right track we will check to make sure that it is actually attempting to fight in the battle with their opponent and that the agent has picked a weapon (any weapon - first at random and then with more knowledge). As a part of the sanity check we will record the weapons the agent picks each time to ensure that if they are not working in its previous battles, then the agent is attempting new ones in the later battles. Our end goal would be for our AI to beat the Ender Dragon. 

Appointment Time: January 20th 3:30 PM