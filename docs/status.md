---
layout: default
title:  Status
---

<h2>Project Summary:</h2>
Our Zoomer project is an AI that guides our agent through a course of randomly generated obstacles spawned at set locations. The twist is it will be using elytra to glide/fly through these obstacles to reach its goal rather than walk. The agent is placed at the beginning of an obstacle course approximately 100 blocks long. It has a 5 by 5 observation space/line of sight of the world around it and moves away from any obstacles that come within that using a random pitch. Our agent is also using reinforcement learning to know when to use elytra, when to boost itself, which objects to avoid (glass ceiling, obsidian side walls, lava enveloping the ground, and blue wool obstacles scattered throughout the course), and which objects to aim for (redstone goal blocks). The goal of our project is to have our agent fly through the obstacle course in the straightest and fastest manner possible without touching the edges (walls/ceilings) of the course. 


<h2>Approach:</h2>
In our project, the primary machine learning/artificial intelligence algorithm we use is reinforcement learning. Using the “rllib” library, we give it the pytorch framework as a primary way to learn. In order for reinforcement learning to work properly, we created an observation space capturing every block within the nearest 5x2x5 region. Using the observation space, we then send what type of blocks are in the immediate line of sight so that our agent can learn to avoid these obstacles instead of crashing. Using the line of sight, we make sure our agent will move immediately if there is lava, obsidian (the wall), glass (the ceiling), or wool (the obstacle) nearby. 

We decided to use continuous movement for our agent in order to give the agent more maneuverability and fluidity to avoid obstacles. With continuous movement, our action space includes “pitch”, “turn”, and “use”. By including “pitch” as one of the actions, our agent will be able to immediately move down or up if there is an obstacle in front of it. Similarly, by including “turn” in our actions, our agent will be able to turn away from the obstacle (most of the time, these obstacles include the walls), and not crash. Lastly, we include “use” as one of our actions so our agent can decide when to use the fireworks and boost itself forward over obstacles. 

Finally, it is important to add negative rewards if the agent doesn’t perform properly in order to discourage further similar actions. So, we decided to add a negative reward of -50 for touching lava, obsidian, glass, and -10 for touching wool. Since lava causes the agent to immediately die, we added a high negative reward for it so the agent learns not to touch it. Meanwhile, we added a high negative reward for obsidian (the walls) and glass (the ceilings) so the agent will not “hug” these blocks in order to get across the obstacle course. We want our agent to steadily be in the center of the course with occasional movements to the side, up, and down. As a result, we added a lower negative reward for touching wool (the obstacle block), so the agent would learn to avoid it but not go all the way to the edge or top. Since the obstacle course is 100 blocks long and negative rewards can add up quickly, we decided to add a positive reward of +1000 for reaching the end of the course. This reward will outweigh the negative rewards and teach the agent that reaching the end of the course is beneficial. Additionally, we added a reward of +1 for reaching six checkpoints located at different distances across the 100 block range. This reward should teach the agent that getting further in the course will also be beneficial.


<h2>Evaluation:</h2>
For our quantitative evaluation, we decided to use the reward counter since that would give us an overview of how the agent was performing over a certain period of time. Currently, we have a working agent that gets to the end of the obstacle course occasionally, but dies other times. Below, you can see two graphs highlighting the reward improvement over the course of 1000 steps and over the course of 2500 steps. While the agent tends to have negative rewards sometimes, we can already see an upward trend leading towards the positive side. Once we start training the agent for longer periods of time, we can expect to see a more stable positive reward.

![Figure 1](zoomer_graph_1.jpg)
![Figure 2](zoomer_graph_2.jpg)

For our qualitative evaluation, we are analyzing the response time the agent has to see an object and perform an action. Based on this, we are able to determine if the agent is reacting to objects the way we want it to. In the first video below, you can see the agent crashing immediately into the lava. In the second video, after changing the pitch, our agent was able to react more positively to the obstacles by avoiding them.

![](https://media.giphy.com/media/CNWDGkhmbiGpNUWV5Y/giphy.gif)
![](https://media.giphy.com/media/boW7I8waJeu4RQDeM8/giphy.gif)

<h2>Remaining Goals and Challenges:</h2>

<h4>Remaining Goals:</h4>
Because our AI is not improving/learning at the rate we would like it to, one of our primary goals for the final report is to improve the rate of the reinforcement learning of Zoomer to ensure it is always (or almost always) improving as it goes through the course whether it reaches its goal or dies. 
For at least part of the next few weeks we would like to experiment with different methods and techniques that might allow us to improve our player’s reinforcement learning. One of these would be to test out possibly using a video recording to recognize objects and allow the agent to dodge them in mid-air. 
And of course, over the next few weeks we would like to have our player run for longer periods of time in order to sufficiently evaluate our methods and determine the best reinforcement learning techniques for our project before final presentations. 



<h4>Challenges:</h4>
From our experience so far, we have had some trouble ensuring that the agent stays alive when it reaches the redstone wall. Too often, it smacks the redstone wall at too high a velocity that it dies on impact which means that despite reaching the end goal, it fails (it does, however, receive the reward for reaching the redstone wall, so it’s not necessarily crippling to the project but it does not return end screen we would like it to). We have tried solving the issue using more armor to protect the agent but that has done to help. Moving forward we might try expanding the observation space/input (possibly video recording) to check if there is a wall before allowing the agent to boost itself. 
By stacking our checkpoints, the agent is sometimes motivated to move upwards away from them as opposed to across them to reach the end goal. This problem doesn’t seem to be as much of an issue after spending some time considering/testing different reward values. We will continue to test different reward values to determine the best for us or possibly consider an approach without checkpoints. 

<h2>Resources Used:</h2>
We based our initial reinforcement learning approach/implementation on that provided to us in Assignment #2 (which uses the library “rllib”), which we modified to work with our project. We used the XML Schema and Project Malmo code documentation to help with writing our code. Additionally, we used the “Pyautogui” and “pygetwindow” libraries to activate the elytra as Malmo could not send the jump output long enough for the wings to activate.



