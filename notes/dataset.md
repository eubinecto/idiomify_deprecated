## 25th of March 2021

> What would be your target idioms?

The SLIDE idioms. They are the 5000 most frequently used idioms. So worth
extraction collocations, and implementing a reverse dictionary search.

Target idioms would be around 3000 idioms. (include only those that are long enough.)


> where can I get definitions * POS for the idioms?

The more definitions we have, the better the quality of the 
model would be.

- Any API's I could use?
  - WordNik API (this includes Wiktionary, so no need for directly scraping them)
  - Phrases API
  

- any useful website I could scrape?
  - [free dictionary](https://idioms.thefreedictio nary.com/and+be+done+with+it)
    - not sure if they have an api, but I can parse them out.
  


quora - https://www.quora.com/What-are-the-popular-free-dictionary-APIs-available-today


so we have:
- wiktionary (guaranteed to have at least one. )
- phrases.com
- wordnik (also involves more formal dictionaries)
- the free dictionary - this is also pretty rich. 
- the urban dictionary - this one is rich. Let's take this one first. You can use RapidAPI for this.


Okay. If you look for them, you'll be able to find them. That's good.

## 26th of March 2021

urban dictionary - I can't use them for dataset. They are jokingly biased towards a specific topic.
e.g. 
```
#### idiom:wouldn't you know
["refers to the story told by [Jim Cornette] when a local wrestling [promoter] ,
 faced with declining attendance ,
 [rigged] a lottery to give a way a pony so his son won it
  , so we did not lose money on the deal . As a result anything is is obviously rigged is referred to as wouldn't you know who won the pony ."]

```

other api's I could use?
