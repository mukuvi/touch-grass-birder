---
title: DRAFT
published: false
tags: devchallenge, hf26challenge, opensource, ai
---

This is a submission for the Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass.

## What I Built

Touch Grass Birder is a bird call identifier that runs on your own device. You
hold your phone up for a few seconds, it tells you which bird is singing, and
then you put the phone away and look for it.

## Demo

Share a deployed link or a video demo.

## Code

Embed the GitHub repo.

## How I Built It

BirdNET, the open acoustic classifier from the Cornell Lab of Ornithology, runs
locally through ONNX Runtime. Gemma 3 1B, an open weight model, runs through
llama.cpp for short field notes.

## Why Does Open Innovation Matter?

The screen is the shortest part of the experience. A closed bird ID API needs a
round trip, and in the backcountry there is no round trip. Running an open
weight model locally means the app works with no signal, and the coordinates of
a rare sighting never leave the device.

## My Agent Session

Optional. Save your session with DevRelay and embed it.

## Prize Categories

- Best Use of Gemma
