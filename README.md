# CharVis
Visualizing sentiment data from Bill O'Reilly's show on Fox News

Note: development framework taken from https://github.com/oschneid/Macaron, including configs.

Input data requires two sets of source files. First is a summary document in the following form, where each array entry is a summary of the data contained in the text:

```json
[
  { "date": "2003/01/03", 
    "summary": "The summary", 
    "title": "The Title", 
    "keywords": ["keyword1", "keyword2"], 
    "speakers": ["speaker1","speaker2"], 
    "concepts": {"concept1": [["sentiment_instance1", #.#],["sentiment_instance2", #.#]], "filename": "the_file.txt", 'concept2' ... }
  }, ...text 2
]
```

Then, each text should be formated as:

```json

{ "paragraphs": [
    {"text":["The","text","split","into","an","array","."]},
     "speaker": "The Speaker", 
     "concepts": [
 	      {"j": ##, 
 	       "concept": "The concept", 
 	       "i": ##, 
 	       "s": ["sentiment", #.#]
 	      },
     ]
}

```

In this way, the system should display any text data formatted like this, i.e., it is not dependant on the corpus presented here.

## Installation Instructions

Simply run:

`npm install`

to download and install all dependencies. Then:

`npm run build`

to compile the JS code into an app. Then:

`npm run dev`

To run the server. If there are any issues, consult the detailed instructions below.

To build the packages for distribution, run:

`npm run deploy`

## Python to build database

This framework also includes a number of python scripts to build up the database used by CharVis. Some were authored by Paul Bucci, some were not. As such, each file contains a tag at the top to identify the author. All front-end appliction development was authored by Paul Bucci, with the exception of the CSS, of which some was taken from a React tutorial base.

All python is in data/python.
