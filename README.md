## PESA PULSE - Where are Our Customers?
Pesa Pulse has signed a partner who shares its customer directory through an API. Before marketing plans regional campaigns, they need the basics: how many customers there are, where they are, and what the data looks like. This project pulls the data, explores it, extracts the attributes that matter answering the question first with plain Python and then with pandas, ending with visuals.

### Data Source : 
"https://jsonplaceholder.typicode.com/users"

### Project Layout
```Analysis.py 
Outputs/:
        customers.csv              #a flat dictionary with individual attributes eg 'id','name', 'email' etc 
        cities.csv                 # a dictinary; city name as key, customers as value {<str>:<int>}
        domains.csv                #a dictionary with email domain as key and customers as value{<str>:<int>}
        customer_distribution.png  #no. of customers per city 
        domain_distribution.png    #no. of customers per email domain
README.md```    

