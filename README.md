# Mangadex-Downloader
Download manga from mangadex to read offline (their servers are really unreliable)
## How to use the Downloader
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
