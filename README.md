# pokerendpoint
Flask demo project api



Calculate poker cards wining combination rank, higher - better and higher card

    Accepts cards in format
    'XY' , where X is suit
         'Y' stands for card value, could be any in
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "D", "K", "A"

    For given request:


    POST 127.0.0.1:5005/api/v1.0/hands
    {
        "hand": ["DK", "CA", "D7", "D7", "CK"]
    }

    returns:
    {
      "hand": {
        "max_card": "K",
        "rank": 2,
        "second_value": "7"
      }
    }

    where rank 1 stands for 'pair of'
    and A for ACE

    where rank 1 stands for 'pair of' 7th
    
    Also 
    GET 127.0.0.1:5005/api/v1.0/calculate/DA,CA,D7,D6,D3
    
    calculates:
    {
      "max_card": "A",
      "rank": 1
    }
