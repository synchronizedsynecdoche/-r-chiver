# /r/chiver

## About 
**/r/chiver** is a python program with a Flask frontend that allows a user to fetch, download, and archive Reddit posts and comments from an inputted user. This was designed for people want to have a backup of an account they were about to delete. Note that this program can not resurrect deleted posts, and will simply fetch/write `[removed]`. It uses PRAW to interact with Reddit, so you should be aware of Reddit's API ToS.

## Authentication
/r/chiver requires an key to authenticate to the API. You can learn about how to get an API key [here](https://www.reddit.com/dev/api). The program expects an `archiver.config` file to be in the top level directory, and a sample config file is given. Note that not having a well-formed config file will cause the program to crash, and passing invalid credentials will cause the program to exit once it recieves an error code from PRAW.

## Archival
/r/chiver allows a user to (optionally) archive content using archive.is,  and it is recommended you read through the their terms before using the archival functionality. Archiving will be slow; I put in a 20 second delay every 5 archives to avoid being rate limited, but you can change it at your peril. During this time, the Flask server will appear to hang, but be assured it is still working in the background, and you can see output from the console you're running the server from. 
