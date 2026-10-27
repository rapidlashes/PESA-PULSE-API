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

All other fields `(id, name, username, email, phone, website)` are flat.
The deepest attribute is three levels down (record → address → geo → lat/lng) and is reached by chaining keys:

```python
'latitude' = c['address']['geo']['lat']
'longitude = c['address']['geo']['long']
```

#### Step 3: Extract customer attributes
`extract_attributes(customers)` returns one flat dictionary per customer with attributes: **id, name, username, email, email_domain, phone, city, zipcode, latitude, longitude, company, website.**

Nested values are reached with the key chains found in step 2 (for example `c["address"]["city"]`, `c["company"]["name"]`).
email_domain is derived with `email.split("@")[-1].lower()`. the `[-1]` tells python to take the most last part of our email after splitting and the `.lower()` converts it into lower casing. For instance **ahmedsalim@gmail.com** , the domain name will be `gmail.com`.
`latitude` and `longitude` are wrapped in float(), as the brief requires.
Flat dictionaries were the goal because they map directly to table rows, which makes the pandas step trivial.

#### Step 4: Finding unique cities
`unique_cities(customers)` is a set comprehension: `{c["address"]["city"] for c in customers}`. A set stores each value only once, so its length is the number of distinct cities.

I then compare that number with the number of customers which is equal

**MEANING :** every customer is in a different city, so there are no city-level clusters and marketing cannot target campaigns by city.

**INTERPRETATION** Fewer cities than customers --> customers cluster, Cities with several customers are the natural first targets for local campaigns.

#### Step 5: Counting customers with dictinary comprehension
This step counts th number of customers in each city, and bearing each domain name giving back the result inform of a dictionary with this format `{<str> : <int>}`
The brief bans **collections.Counter** and **pandas** here, so the counting is explicitly done by for loops and adding a count whenever the function loops in individual customers:
syntax:
```python
def city_counts(customers):
    customer = {}
    for c in customers:
        city_name = c['address']['city']

        if city_name in customer:
            customer[city_name] += 1
        else:
            customer[city_name] = 1

    return customer
```

Now lets return a dictionary of domain names and count of customers:
syntax:
```python
def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    customer = {}
    for c in customers:
        domain = c["email"].split("@")[-1].lower()
        if domain in customer:
            customer[domain] += 1
        else:
            customer[domain] = 1
    return customer
```

#### Step 6: Converting to DataFrames and saving as CSV file
` def to_dataframe(rows)` is a function that converts these dictinaries we have been returning into csv files.
We will pass `result_x`, `dict` , `counts` when calling out this function. `result_x` is the flat dictinary we returned from  the `extract_attribute()` function , `dict` is the dictinary we returned from the `email_domain_counts()` function while `counts` is what we returned from the `city_counts()` function.

Having converted the dictionaries into dataframes we then save them as csv files in our project folder using `filename.to_csv(path)`.

#### Step 7: Plotting
This is the final step where we are plotting the distribution of our customers in individual cities and domain names. 
syntax:
```python
def plot_distribution(city_counts: dict[str, int], path: Path) -> None:
    labels, values = list(city_counts.keys()), list(city_counts.values())
```
When calling out this function we will pass `counts` as the first parameter and the path of our to be .png file. The `.keys()` is a function that is used to to extract keys from a dictinary, `list(city_counts.keys())` is basically telling us to store those keys extracted in a list. Same applies to the values. 

Suppose we want to plot the distribution of the domain_names:
syntax:
```python
def plot_distribution(domain_counts: dict[str, int], path):
    labels, values = list(domain_counts.keys()), list(domain_counts.values())
```
Likewise when calling out this function , we will pass `dic` as the first parameter followed by our desired path.

### Assumption and Summary
1. The directory is small (about 10 records), so the script loads everything in one request. A larger API would need pagination.
2. Cities are matched as exact strings. Real-world data would need cleaning for spelling and case variants before counting.



