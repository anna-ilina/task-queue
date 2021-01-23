Simple message board using redis (Tutorial)

Based on app at http://retwis.redis.io/index.php

Requirements:

- create an account (username and password)
- login, logout
- post messages
- see other user's messages (most recent first)
- follow other users
- stop following other users
- see how many users I am following and how many are following me


Data models:

- Hash to store user's info
	- hashname will be username
	- keys will include:
		- password
		- following (set of usernames I am following)
		- numFollowers (int)

- TBD: HOW TO STORE MESSAGES


Restrictions:

- Username '' is not allowed


Workflow:

- When A creates an account:
	- HSET to create hash given by username, 

- When A follows B:
	- SADD B to A's `following` set
	- INCR B's `numFollowers` by 1

- When A stops following B:
	- SREM B from A's `following` set
	- DECR B's numFollowers by 1

- To see user's message feed:
	- TBD

- To see global latest messages feed:
	- TBD