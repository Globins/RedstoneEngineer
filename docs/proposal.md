---
layout: default
title: Proposal
---

<b> Mimicraft </b>
<b> Summary: </b>
	Our project is an AI that takes in a picture as an input and produces a 3D picture as output. Our goal is to have Mimicraft search for a block of space in our world that will be sufficiently large enough to build the projected image on and then it should go on to produce a group of blocks in Minecraft that essentially mimic (as closely as possible in 3D) the input we’ve given it. To convert our input image into a format that will be usable by our AI, we will use Matplotlib, which can convert our image into a matrix of RBG values for Mimicraft to use. 

<b> AI/ML Algorithms: </b>
    We plan on attempting several different approaches to evaluate which works best. 
    Deep learning - deep neural networks: to produce the image
    K nearest neighbor: to produce the image
    Supervised learning: to find the best space to build our image on
    
<b> Evaluation Plan: </b>
    Quantitative Evaluation:
        For our quantitative evaluation, we plan on measuring the accuracy of the RBG values for each pixel to the RBG values of each corresponding block in Minecraft. If we notice the RBG values are varying greatly, then we will optimize the way in   which our project chooses certain blocks to use in the image. Our baseline goal is to have each RBG value (from the input image) correspond to at least a similar enough RBG value (in the minecraft image). From there, we will try to improve our project to have the lowest RBG value difference possible. 
        https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
        We will use this python technique to compare the two images using Mean Squared Error and Structural Similarity Index
        https://deepai.org/machine-learning-model/image-similarity#:~:text=Image%20Similarity%20compares%20two%20images,of%20'0'%20being%20identical.
        We will also use this image similarity API to compare the two images, we will get a return value that tells us how similar our images are to each other. 
    Qualitative Evaluation:
	    For our qualitative evaluation, we will analyze how close the input image looks compared to the minecraft image. For our sanity cases, we will start off with simpler images such as images of a phone and see if Mimicraft can accurately convert the image into a Minecraft image using the proper blocks. Once we can confirm simple images are being converted accurately, we will start testing out a bit more colorful and complicated images. 
    Moonshot Case: 
        Our moonshot case would be to create our 3d model in a way where if the agent moves around the model, it/the user will be able to tell exactly what the model is an image of from all angles (without having known what the input was).

<b> Appointment with the Instructor: </b>
	We scheduled a second meeting for Friday (01/22/2021) at 4:45 PM.


<title> Proposal #2:  </title> 
<b> Zoomer </b> 
<b> Fast Gliding through obstacles </b> 

<b> Summary: </b>
	Our project is an AI that guides the player through a variety of objects as fast as possible using elytra. Glyder uses OpenCV and reinforcement learning to guide a player in a straight line using elytra without stopping, dying, or touching the floor. We will record the screen the agent is playing on with OpenCV. Then we will analyze the image to identify what is a solid object and what is an air block. After analyzing the image, the agent will move to the optimal gaps to reach the end of the goal using the mechanics of the elytra or firework rockets. 

<b> AI/ML Algorithms: </b>
    Reinforcement Learning to know when it is going too fast (when to stop using fireworks to boost itself). The reward will be based on the time the agent is flying.
<b> Evaluation Plan: </b>
    Quantitative Evaluation: 
	    For our quantitative evaluation, we will record the time period that the agent is able to stay alive for (without dying from kinetic energy or fall damage). Our base case is for the agent to survive for 45 seconds. As we continue to improve our agent, we will expect to see improvements in the time they survive every trial run.
<b> Qualitative Evaluation: </b>
	    For our qualitative evaluation, we will make sure that our AI makes it through the objects of different heights and widths eventually. 
        For our sanity checks, we will make sure that our agent is gliding in the air without touching the ground. We expect the agent to be able to navigate over mountains and through ravines. Eventually, we will try to improve our agent to be able to navigate through forests without crashing. Another sanity check we will use is to see how fast the agent can make it from one side to another. 
<b> Moonshot Case: </b>
        Our agent will be able to navigate through obstacles at low visibility (Light = 3 or lower), this will affect how the agent will see and react to certain obstacles.
	
<b> Appointment with the Instructor: </b>
	We scheduled a second meeting for Friday (01/22/2021) at 4:45 PM.

