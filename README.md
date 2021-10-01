# Mangadex-Downloader
Download manga from mangadex to read offline (their servers are really unreliable)
# How to use the Downloader
the script `main.py` takes 3 positional command line arguments:
* `mangadex_id` - the id of the specified manga from the url (eg. for `https://mangadex.org/title/a77742b1-befd-49a4-bff5-1ad4e6b0ef7b/chainsaw-man` it would be `a77742b1-befd-49a4-bff5-1ad4e6b0ef7b`)
* `name` - creates a new directory inside the root folder where it will save the chapters
* `chapter_range` - both sides inclusive range that specifies what folders to save and looks like one of these: `a-b`, `a-`, `-b`, `-` where a and b are floats
inside `.env` you can change the following arguments:
* `location` - the root folder where all manga will be saved
* `langs` - acceptable translation languages seperated by commas
* `timeout` - how much to wait in between requests, if its less than `0.2` you might get ip banned
# How to use the Reader
you shouldn't the design is ugly and the code is horrible but if you've got nothing better run `src/main.cr` with the following command line arguments
* `name` - the name of the manga you specified while downloading
* `chapter` - which chapter to open  
you would also need to change the hardcoded directories inside `src/main.cr`
