## PESA PULSE - Where are Our Customers?
Pesa Pulse has signed a partner who shares its customer directory through an API. Before marketing plans regional campaigns, they need the basics: how many customers there are, where they are, and what the data looks like. This project pulls the data, explores it, extracts the attributes that matter answering the question first with plain Python and then with pandas, ending with visuals.

### Data Source : 
"https://jsonplaceholder.typicode.com/users"

### PREREQUISITES
We need to have these dependencies installed inside our virtual enviroment. 
```powershell
uv add pandas matplotlib requests
```
**NOTE:** The above syntax on how to add dependecies applies if you initiated your project folder using UV

### Project Layout
```
Analysis.py 
Outputs/:
        customers.csv              #a flat dictionary with individual attributes eg 'id','name', 'email' etc 
        cities.csv                 # a dictinary; city name as key, customers as value {<str>:<int>}
        domains.csv                #a dictionary with email domain as key and customers as value{<str>:<int>}
        customer_distribution.png  #no. of customers per city 
        domain_distribution.png    #no. of customers per email domain
README.md
```    
### My Approach 
I approached the project in 8 steps each step in its own function , from retrieving data to visualising and generating distribution plots.

#### Step 1:Retrieving data with requests
`get_customers(url)` calls `requests.get(url, timeout=10)`, then `raise_for_status()`, then returns `response.json()`.

**Timeout:** without one, a stalled server would hang the script forever. Ten seconds is generous for a small payload.
**Status check:** `raise_for_status()` turns a 404 or 500 into an exception instead of letting an error page be parsed as data.
**Errors:** I catch `Timeout`(if the API takes too long to respond), `ConnectionError`(if a conection cant be established for example due to network problems), `HTTPError`(The setrver returns an unsuccessfull HTTPS status).

#### Step 2: Explore the nested dictionaries
Our Jason file comprises of a nested dictionary, meaning it has dictionaries inside the main dictinary, and this arreangement has levels to it.
The function `explore(record, indent)` is recursive: meaning for each dictinary it prints each key with its value type and calls itself again on the value whenever the value itself is a dictinary on it's own. In each level it goes , it adds an indentation `indent + 1`.
So in our JSON file we have these 3 keys whose values are dictinaries by themselves:
|Key               |Type        |Value                                  | 
|------------------|------------|---------------------------------------|
|`address`         |dict        |street, suite, city, zipcode, geo      |
|`address.geo`     |nested dict |lat, long                              |
|`company`         |dict        |name, CatchPhrase, bs                  |


