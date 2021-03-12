---
layout: default
title:  Status
---
<h1>Video</h1>
<video width="700" height="300" controls>
  <source src="CS 175 Project Zoomer - Small.mov" type="video/mp4">
</video>

<h2>Project Summary:</h2>
Flying any object at a low altitude is one of the most challenging tasks in both real life and in Minecraft. There’s less time to react, can’t move or see as far and there’s a higher chance of crashing. For this reason, an AI is required to navigate low-flying agents by using object recognition and movement.

Our Zoomer Project is an AI that uses Reinforcement Learning to guide a Minecraft Agent through a randomly generated course using the flight mechanics of the Elytra. The goal of the project is to have our agent fly through the obstacle course in the fastest and safest manner possible. Using the Proximal Policy Optimization (PPO) algorithm from RLlib and Malmo, we take a 31x31x31 observation space, the line of sight, and the agent’s y and z position as input. The agent then returns a pitch, turn and use command as an action. The agent’s reward is based on the progress it makes through the course, the number of obstacles it hits and whether it makes it to the end or not. As a result, our Agent learns when to boost itself, what objects to avoid, and what objects to aim for during flight.



<h2>Approach:</h2>
In our project, the primary reinforcement learning algorithm we use is Proximal Policy Optimization preimplemented by the RLlib using the pytorch framework. For our input, we created an observation space capturing every block within the nearest 5x2x5 region and a line of sight. Using the observation space, we then send what type of blocks are in the immediate line of sight so that our agent can learn to avoid these obstacles instead of crashing. Using the line of sight, we make sure our agent will move immediately if there is lava, obsidian (the wall), glass (the ceiling), or wool (the obstacle) nearby. 

We decided to use continuous movement for our agent in order to give the agent more maneuverability and fluidity to avoid obstacles. With continuous movement, our action space includes “pitch”, “turn”, and “use”. By including “pitch” as one of the actions, our agent will be able to immediately move down or up if there is an obstacle in front of it. Similarly, by including “turn” in our actions, our agent will be able to turn away from the obstacle (most of the time, these obstacles include the walls), and not crash. Lastly, we include “use” as one of our actions so our agent can decide when to use the fireworks and boost itself forward over obstacles. However, to make ensure that "use" was working properly, we modified the minecraft client by swapping the "use" and "attack" buttons so that the agent is able to use the rockets. We also gave our agent diamond armor with protection IV and unbreaking III to prevent the agent from immediately dying when it reaches the redstone goal blocks or any obstacle/edge.

Finally, it is important to add rewards to discourage or encourage the agent from certain behaviors. First, we decided to add a negative reward of -50 for touching lava, obsidian, glass, and -10 for touching wool. Since lava causes the agent to immediately die, we added a high negative reward for it so the agent learns not to touch it. Meanwhile, we added a high negative reward for obsidian (the walls) and glass (the ceilings) so the agent will not “hug” these blocks in order to get across the obstacle course, as seen during some of the earlier training sessions. We want our agent to steadily be in the center of the course with occasional movements to the side, up, and down for maximum maneuverability. As a result, we added a lower negative reward for touching wool (the obstacle block), so the agent would learn to avoid it but not go all the way to the edge or top. We also added a cuboid of reward checkpoints immediately behind the obstacles to encourage the agent to move forward. However, since each individual block in the cuboid gives a reward, to prevent the agent from abusing the checkpoints for rewards we gave it a +1 reward. This is why the other rewards are extremely high. Since the obstacle course is 100 blocks long, the negative rewards can add up quickly. In response we added a very large positive reward of +1000 for reaching the end of the course. This reward will outweigh the negative rewards and teach the agent that reaching the end of the course is beneficial.


<h2>Evaluation:</h2>
<h4>Quantitative Evaluation:</h4>
For our quantitative evaluation, we decided to use the reward counter that would give us an overview of how the agent was performing over a certain period of time, including using saved reinforcement learning data from previous runs (See Figure Z-2 that uses the learned data from Figure Z-1 to resume running). 
Here you can see that the agent is in fact learning (it is not acheiving the same amount of negative reward as it had been in the beginning).
The data is not trending as upwards as we hoped it would into the positives but because we are using continuous action that is somewhat expected. Nonetheless, there is an undeniable upward trend in terms of less negative reward being achieved later on in the graph, and we see a little less volatility towards the extreme negative values. Based off of the current upwards trend, we predict that if we run it for an even longer amount of time, we would see better upward trending results. 

<img src="FinalReturns2.png" width="500" height="500"/>
<caption>Figure Z-1</caption>

<img src="FinalReturns1.png" width="500" height="500"/>
<caption>Figure Z-2</caption>


<h4>Qualitative Evaluation:</h4>
For our qualitative evaluation, we are analyzing the response time the agent has to see an object and perform an action. Based on this, we are able to determine if the agent is reacting to objects the way we want it to. In Video ZV-1 you can see that the agent is still learning through reinforcement learning, it doesn't quite make it to the goal but it now has more data that it can use to determine what it should do next time. In Videos ZV-2 and ZV-3, you can get an idea of what our agent's baseline performance is like after it has learned with the PPO algorithm a little more and is starting to make less mistakes but still either hits obstacles or struggles to reach the goal. In Video ZV-4, the agent reaches the goal redstone wall with relatively no errors and and through our observation, we know it received a higher reward value than usual. Although sometimes the rewards aren't as high as we would like them, the video results prove to us that the agent is in fact learning and achieving it's goal a lot more often towards the end. 


![](https://media.giphy.com/media/orG59r33iqSQQvFaC2/giphy.gif)
<caption>Video ZV-1</caption>


<h4>Baseline Performance:</h4>

![](https://media.giphy.com/media/Pmol78fyEMXNjbW6iP/giphy.gif)
<caption>Video ZV-2</caption>

![](https://media.giphy.com/media/QJJL9EhKjjqc7NpiUi/giphy.gif)
<caption>Video ZV-3</caption>


<h4>Best Performance:</h4>

![](https://media.giphy.com/media/wVxSe23Q0WoJdty5UZ/giphy.gif)
<caption>Video ZV-4</caption>



<h2>References/Resources Used:</h2>
We based our initial reinforcement learning approach/implementation on that provided to us in Assignment #2 (which uses the library “rllib”), which we modified to work with our project. We used the XML Schema and Project Malmo code documentation to help with writing our code. 

Additionally, we used the “pyautogui” and “pygetwindow” libraries to activate the elytra as Malmo could not send the jump output long enough for the wings to activate.

[pyautogui](https://pyautogui.readthedocs.io/en/latest/)
[pygetwindow](https://pypi.org/project/PyGetWindow/)


