# Manga-Downloader
Download manga from mangadex (or other manga websites) to read offline
## Manga Downloader
`Manga Downloader/main.py` is designed to download manga from generic manga websites  
it takes 2-3 arguments
* url of the website
* name of the manga (this argument only changes where the manga is saved)
* reverse - whether to reverse the chapters after scraping them from the given url (changes how the chapters are indexed)

`.env` can also be edited to change the base location, timeout and timeout when met with an error  
It was only tested on one website but the implementation is purposefully generic so there is a decent chance that it will work on most websites
#### Implementation
It scrapes the initial url for a chapter list (takes hrefs from the unindexed list with the most hrefs)  
Then it scrapes the given urls by downloading all images from a div with the most images with srcs of the same domain  
The way it stores these images makes it compatible with the reader inside `Reader`
## How to use the Downloader
Not tested if this still works as Mangadex likes to change their API  
The script `main.py` takes 3 positional command line arguments:
* `mangadex_id` - the id of the manga you want to download from the url (eg. for `https://mangadex.org/title/a77742b1-befd-49a4-bff5-1ad4e6b0ef7b/chainsaw-man` it would be `a77742b1-befd-49a4-bff5-1ad4e6b0ef7b`)
* `name` - creates a new directory inside the root folder where it will save the chapters
* `chapter_range` - both sides inclusive range that specifies what chapters to save and looks like one of these: `a-b`, `a-`, `-b`, `-`  

Inside `.env` you can change the following arguments:
* `location` - the root folder where all manga will be saved
* `langs` - acceptable translation languages seperated by commas
* `timeout` - how much to wait in between requests, if it's less than `0.2` you might get ip banned

It's also worth noting that a chapter will always be redownloaded if it's inside the specified range
## How to use the Reader
You shouldn't. The design is ugly and primitive and the code is horrible but if you don't have any other reader run `src/main.cr` with the following command line arguments
* `name` - the name of the manga you specified while downloading
* `chapter` (optional) - which chapter to open  
This will create and open an html file where you can navigate between pages and chapters with the arrow keys.

You would also need to change the hardcoded directories inside `src/main.cr`.  
You can also set up an alias like this `alias manga='crystal run --release "/SOME/DIRECTORY/src/main.cr" --'`
