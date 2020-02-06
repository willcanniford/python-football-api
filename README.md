# Python Football API

A project and collection of scripts using a free football API to get data about fixtures, stats, players and events. I have decided to store the responses it in a way that makes analysis repeatable and reusable using `MongoDB`. 


I'm calling the API using these:
* [RapidAPI Details](https://rapidapi.com/api-sports/api/api-football/details)  
* [API-FOOTBALL Documentation](https://www.api-football.com/documentation)

Throughout the project I store my login details `MongoDB` and API keys using conda environments. If you want to know how to do this then you can find out more information from this [article by Brendan Connelly](https://towardsdatascience.com/how-to-hide-your-api-keys-in-python-fb2e1a61b0a0) and this [video from Corey Schafer](https://www.youtube.com/watch?v=IolxqkL7cD8) which I found very helpful when I was working out the best way to do this.  

I am using the free tier of the API so will be writing scripts with that in mind to limit the API calls but maximise the amount of data that I am able to get; this is generally best when designing an application, but especially so when you're short on available calls. 
