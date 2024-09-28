# Weather data

This repo contains some boilerplate code and instructions for three subtasks we would like you to complete as a part of evaluating you for the Data Engineer position at Trustly. We expect this to take a few hours at most and we don't expect the code to be "perfect". What we want to understand is how you think when you build software.

## Scenario
Your first day as a Data Engineer at Trustly you are asked to look at a Jira card with the title "Integrate SMHI". There is no description but you manage to get hold of the stakeholder who wrote this card and the following conversation ensues:

__You__: I saw this Jira card about integrating SMHI. What is that and why do you need it?

__Stakeholder__: We want to download weather data from the Swedish Meteorological and Hydrological Institute to try out some hypotheses we have.

__You__: What data do you want?

__Stakeholder__: Ehh.. Everything I guess.

__You__: I can have a look but if it's a lot of data I may come back to you and maybe we can work out together what you really need, ok?

__Stakeholder__: Sure, that sounds great!

## Exercise 1

_You do some googling and find that SMHI has an [Open Data API](https://opendata.smhi.se/apidocs/metobs/index.html) that you can use. Sweet! After having integrated a lot of data sources over the years you know that doing everything up-front on such a loose request is probably not a good idea so you decide to first write a small script that extracts and presents the different kinds of data you can export. There is some boilerplate code available in the file [smhi.py](smhi/smhi.py) in this repo. You should modify it to enable this behaviour_:

````
$ python3 -m smhi.smhi --parameters
1, Lufttemperatur (momentanvärde, 1 gång/tim)
2, Lufttemperatur (medelvärde 1 dygn, 1 gång/dygn, kl 00)
3, Vindriktning (medelvärde 10 min, 1 gång/tim)
[...]
````

__Tip__: _If you haven't already done so, it may be a good idea to create a virtual environment for this project and then install the script with_:
````
$ make install
````

Once finished with the modification, you go back to the stakeholder:

__You__: I extracted a list of the data points that are available over the API. Do you really think we need all of those?

__Stakeholder__: No no, when I see all this, I realise that what I want is just he average temperature during the day so "2, Lufttemperatur (medelvärde 1 dygn, 1 gång/dygn, kl 00)" should be enough. When can we have it available?

__You__: It shouldn't be that hard. Is there any particular geographical location for which we should retrieve this data?

__Stakeholder__: Well, actually, what we need to know is just the stations with the highest and lowest temperatures. Can you extract that?

__You__: I'll have a look.

## Exercise 2

_Without removing any functionality, add this behaviour to the script:_

````
$ python3 -m smhi.smhi --temperatures
Highest temperature: Falsterbo, 2.0 degrees
Lowest temperature: Karesuando, -30.6 degrees
````

_Note: the highest/lowest temperatures will of course vary all the time, what's important is that your logic works._

Happy with your latest change, you go back to the stakeholder again:

__You__: Let me show you, now we can instantly retrieve the average temperature for all Swedish meteorological observation points and print the highest and lowest values.

__Stakeholder__: This looks really good. Great work! I would ask you to deploy it right away but something else has come up that we need to focus on so let's put this on hold for a while.


## Exercise 3

_Well, this happens all the time, right? You have to switch context and work with something else for an indefinite amount of time. Knowing that you will have forgotten everything about this script once it's time to revive it you decide to write an automated test (unless you haven't already done so) to make your life easier down the road. Is there any test you can add to [test_smhi.py](tests/test_smhi.py) that would help improve the quality of this small repo? It's an open question and we are not expecting any particular answer. We're just curious to understand how you are reasoning about testing your code and would like to see an example of that. It's usually a bit complex to add "pure" unit tests to logic that is tightly coupled to an external API so feel free to consider this an "integration test" if you want. You can verify that the test runs with:_

````
$ make test
pytest tests
[...]
==================== 2 passed in 0.32s ====================
````

Once you are done, make a zip file of the repo and send it back to us via email or, if you have created your own fork, share it with us. Please do not push any code back to our git repo!
