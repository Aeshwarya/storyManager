# storyManager

APIs:
1.	Create Story:
a.	Url: http://3.22.208.149/story
b.	METHOD: POST
c.	Data
i.	Content-type: multipart/form-data
ii.	file:  (FileStream) (Video/Image) (Optional)
iii.	user_name: <Any String>
iv.	name: <Any String>
v.	description: <Any String>
vi.	type: IMAGE|VIDEO|TEXT
vii.	latititude: <Any string>
viii.	longitude: <Any string>
ix.	text: <Any string> (Optional)
 

2.	fetch all stories
a.	Url: http://3.22.208.149/stories
b.	METHOD: GET
3.	Fetch resized
a.	Url: http://3.22.208.149/resize?story_id=<ID>
b.	METHOD: GET

HOW TO RUN:
1.	Install python3 on your machine
a.	sudo apt-get install python3
2.	Install pip on your machine
a.	sudo apt install python3-pip
3.	Install virtualenvironment on your machine
a.	python3 -m pip install  virtualenv
4.	Install redis-server on your machine
a.	https://redis.io/topics/quickstart
5.	Run redis-server
a.	redis-erver
Move  to new terminal
6.	Clone source code
a.	git clone https://github.com/Aeshwarya/storyManager
7.	Create a virtual environment
a.	cd storyManager
b.	python3 -m venv env
8.	Activate the virtual environment
a.	source env/bin/activate
9.	Install requirements.txt
a.	pip3 install -r requirements.txt
10.	Run python server
a.	python3 run.py
Move to new terminal and activate the virtual environment
11.	Run Celery worker
a.	celery worker -A worker.celery --loglevel=info

Test with the above url, replace ip with localhost and port 5000 😊 
