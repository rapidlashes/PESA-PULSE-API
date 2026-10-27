import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.request.exceptions.RequestException as error:
        print(f"Error fetching customers: {error}")
        return []


customers = get_customers()
print(customers)


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    pad = "     " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{pad}{key}:{type(value).__name__}")  # class <str>
            explore(value, indent + 1)
    elif isinstance(record, list):
        for i, item in enumerate(record):
            if isinstance(item, (dict, list)):
                print(f"{pad}{i}:{type(item).__name__}")
                explore(item, indent + 1)


results = explore(customers)
print(results)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = [
        # creating an empty list , inisde it will have many dictionaries, each dictinary has individual attributes from the jason file(a nested dictinary)
    ]
    # customers is the whole jason file with (eg 500 customers), c stands for one out of the 500 customers.
    for c in customers:
        try:
            rows.append({
                'id': c['id'],
                'name': c['name'],
                "username": c["username"],
                "email": c["email"],
                "email_domain": c["email"].split("@")[-1].lower(),
                "phone": c["phone"],
                "city": c["address"]["city"],
                "zipcode": c["address"]["zipcode"],
                "latitude": float(c["address"]["geo"]["lat"]),
                "longitude": float(c["address"]["geo"]["lng"]),
                "company": c["company"]["name"],
                "website": c["website"],
            })
        except KeyError as e:
            print(f"Customer {c.get('id')}: missing key {e}")
        except (TypeError, AttributeError) as e:
            print(f"Customer {c.get('id')}: missing value ({e})")
    return rows


result_x = extract_attributes(customers)
print(result_x)
print()


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    x = {c['address']['city'] for c in customers}
    unique_city_count = len(x)
    customer_count = len(customers)
    return x, unique_city_count, customer_count


counts = unique_cities(customers)
print(counts)
print()


def city_counts(customers):
    customer = {}
    for c in customers:
        city_name = c['address']['city']

        if city_name in customer:
            customer[city_name] += 1
        else:
            customer[city_name] = 1

    return customer


counts = city_counts(customers)
print(counts)
print()
print()


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    customer = {}
    for c in customers:
        domain = c["email"].split("@")[-1].lower()
        if domain in customer:
            customer[domain] += 1
        else:
            customer[domain] = 1
    return customer


dic = email_domain_counts(customers)
print(dic)


def to_dataframe(rows):
    return pd.DataFrame(rows)


result1 = to_dataframe(result_x)
print(result1)
print()
result1.to_csv(
    r"C:\Users\ahmed\Downloads\ASSIGNMENT_1\Data\Processed\customers.csv", index=False)


def to_dataframe(rows):
    return pd.DataFrame(list(rows.items()), columns=['domain', 'domain_count'])


result2 = to_dataframe(dic)
print(result2)
result2.to_csv(
    r"C:\Users\ahmed\Downloads\ASSIGNMENT_1\Data\Processed\domains.csv", index=False)


def to_dataframe(rows):
    return pd.DataFrame(list(rows.items()), columns=['City', 'count'])


result3 = to_dataframe(counts)
print(result3)
result3.to_csv(
    r"C:\Users\ahmed\Downloads\ASSIGNMENT_1\Data\Processed\cities.csv", index=False)


def plot_distribution(city_counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    labels, values = list(city_counts.keys()), list(city_counts.values())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values, color="#4C78A8")
    ax.set_title('Customer per city')
    ax.set_xlabel('City')
    ax.set_ylabel('Total customers')
    # values of y axis to start from 0-> largest value of the total customers , plus 1 for allowance
    ax.set_yticks(range(0, max(values)+1))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    fig.tight_layout()
    fig.savefig(path)
    plt.show()


plot = plot_distribution(
    counts, r'C:\Users\ahmed\Downloads\ASSIGNMENT_1\Plots\customer_distribution.png')
print(plot)


def plot_distribution(domain_counts: dict[str, int], path):
    labels, values = list(domain_counts.keys()), list(domain_counts.values())
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, values, color="#2484E4")
    ax.set_title('customers per Domain')
    ax.set_ylabel('count of domain')
    ax.set_xlabel('domain')
    ax.set_yticks(range(0, max(values)+1))
    ax.set_xticklabels(labels, rotation=60)
    fig.tight_layout()
    plt.show()
    fig.savefig(path)


domain = plot_distribution(
    dic, r'C:\Users\ahmed\Downloads\ASSIGNMENT_1\Plots\domain_distribution.png')
print(domain)
