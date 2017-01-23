PAN Kreator bot
===============
PAN Kreator bot is an internet crawler that digs the resources of the PAN Biblioteka Gdańska and posts interesting results on the Twitter/Facebook.

Bot uses the OAI-PMH API to connect to the pbc.gda.pl and perform a query. Matching record is downloaded, unzipped and converted from djvu to jpg. Finally, the image is posted on the Twitter.

But this is just the part of the bot's abilities. This guy uses machine learning algorithms (Support Vector Machine) to get the idea about the content of the downloaded book. He's able to tell the difference between the text, blank page and image (preferably a figure). Bot goes through all pages of a books and picks only those that are worth posting from his point of view. When a book ends, he chooses the page that seems to contain highest percent of images.

<h4>How does he know what to look for?</h4>

The bot was initially taught to distinguish three categories of pages by a human. We used a set of 368 images that contained different data. 

For example this was marked as a <b>text</b> (which we don't want to publish on Twitter):  

<img src="https://raw.githubusercontent.com/vevurka/pbc/master/image_detector/data/images/page00061..jpg" />

this as a <b>blank page</b> (also not very interesting):

<img src="https://raw.githubusercontent.com/vevurka/pbc/master/image_detector/data/images/3.jpg" />

but this as an <b>image</b>, because it contains something different and possibly worth showing:

<img src="https://raw.githubusercontent.com/vevurka/pbc/master/image_detector/data/images/t-62.jpg" />


The effectiveness of the image recognition is quite hard to predict, but it makes the results of bot's work interesting.


<h4>To check what PAN Kreator have found recently, please visit his Twitter or Facebook page.</h4>

https://twitter.com/PAN_Kreator

https://www.facebook.com/pankreatorbot/

Please follow him if you like this!
