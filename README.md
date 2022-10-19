# Aspen Capital Interview Project
## 
##
##
## RESTful Endpoints
### Endpoint for run simulation of the card game
Both endpoint are accessible using "GET" method
```sh
http://54.201.247.15/simulation/v1/usernamex/<str:player name>/usernamey/<str:player name>/noshowhistory
#or get result with the game history
http://54.201.247.15/simulation/v1/usernamex/<str:player name>/usernamey/<str:player name>/showhistory
```
Example without history (you can click it to experiment): http://54.201.247.15/simulation/v1/usernamex/Alex/usernamey/Iris/noshowhistory
Return:
```sh
{"winner": "Alex", "number_of_rounds": 117, "number_of_war_rounds": 7}
```
Example with history (you can click it to run): http://54.201.247.15/simulation/v1/usernamex/Alex/usernamey/Iris/showhistory
Return:
```sh
#since it show the full history of the game, it is very long output, here I only show the top several lines.
{"winner": "Alex", "number_of_rounds": 735, "number_of_war_rounds": 41, "game_history": {"0": {"round_num": 0, "Alex": "black-clubs_5->black-clubs_2->black-clubs_A....", "Iris": "black-clubs_4->black-clubs_6->red-hearts_4->black-spades_8->red-diamonds_J->black-spades_k->red-hearts_k->red-diamonds ...}
```

Example without history: http://54.201.247.15/simulation/v1/usernamex/Alex/usernamey/Iris/showhistory
Return:
```sh
{"winner": "Alex", "number_of_rounds": 117, "number_of_war_rounds": 7}
```

### Endpoint to get lifetime wins for each player
```sh
http://54.201.247.15/lifetimewin/v1/username/<str:player name>
```
Example: http://54.201.247.15/lifetimewin/v1/username/Iris
Example Return:
```sh
{"username": "Iris", "number_of_wins": 1136}
```

## Additional APIs that I implemented
### Endpoint to run multiple game simulations
```sh
http://54.201.247.15/simulations/v1/usernamex/<str:player name>/usernamey/<str:player name>/<int:number of simulation to run>
```
Example: http://54.201.247.15:8000/simulations/v1/usernamex/Alex/usernamey/Iris/10
Example Return:
```sh
[{"winner": "Alex", "number_of_rounds": 147, "number_of_war_rounds": 11}, {"winner": "Iris", "number_of_rounds": 127, "number_of_war_rounds": 5}, {"winner": "Alex", "number_of_rounds": 494, "number_of_war_rounds": 28}, {"winner": "Alex", "number_of_rounds": 363, "number_of_war_rounds": 23}, {"winner": "Iris", "number_of_rounds": 174, "number_of_war_rounds": 12}, {"winner": "Iris", "number_of_rounds": 798, "number_of_war_rounds": 52}, {"winner": "Iris", "number_of_rounds": 1265, "number_of_war_rounds": 79}, {"winner": "Alex", "number_of_rounds": 186, "number_of_war_rounds": 22} ...]
```

Note: Since I am using a single core server and currently no autoscaling is configured, if you give it a large number, it may take very long time to run and cause time out. 

### Endpoint to visualize the simulation result between two players
Imagine you want to do some analysis on the simulations result for two players, this API provide basic plotting and tables. It is updated based on the database, and if you run new simulation, refreshing the page will give you updated result.
```sh
http://54.201.247.15:8000/visualization/v1/usernamex/<str:player name>/usernamey/<str:player name>
```
Example: http://54.201.247.15:8000/visualization/v1/usernamex/Alex/usernamey/Iris
Example Return: a page with interactive plots and chart
Picture

## Error Handling

## Run the Framework locally
Currently, the service is already deployed at the AWS Lightsail and you can test using above links without install locally
For running locally, following these steps:
```sh
pip install pandas statsmodel
pip install plotly==5.10.0
python -m pip install Django

git clone https://github.com/fanfanwu9898/wargame_simulator
cd wargame_simulator 
python manage.py makemigration game_simulator
python manage.py migrate game_simulator
python manage.py runserver
```
## Current Design and Future Improvement (that I wish that I have time to make)
Due to time/budget limitation, I choose to deploy my service using AWS Lightsail, which is a great tool for quick prototyping and deployment, but not meant for scalable production. 

If time allows, I will implement a production-level autoscalling-enabled cloud service, which will use EC2 instances from AWS.

Other Improvements could be made:
- I can have better database design for storing game history
 Currently the history of each simulation is recorded by using long strings to represent the card deck of each player. This obviously violate the third normal form of database design. There is much better way to design the table for shorter query time and less space consumption.
- I can implement interactive UI that integrate existing Plotly visualization using React framework
- At this moment, the service is using the Django development server. For production ready, I will configure Nginx server. 

# NOT MY CONTENT
Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

# 

Dillinger uses a number of open source projects to work properly:

- [AngularJS] - HTML enhanced for web apps!
- [Ace Editor] - awesome web-based text editor
- [markdown-it] - Markdown parser done right. Fast and easy to extend.
- [Twitter Bootstrap] - great UI boilerplate for modern web apps
- [node.js] - evented I/O for the backend
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML
to Markdown converter
- [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```

This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>

