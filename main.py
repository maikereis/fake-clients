import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("pt_BR")


def clean_name(name: str) -> str:
    """Remove common Brazilian honorific titles from names.

    This function removes titles like "Dr.", "Sra.", "Srta." etc.
    from the beginning of a name string.

    Args:
        name (str): The full name possibly containing a prefix.

    Returns:
        str: The cleaned name without prefixes.
    """
    prefixes = ["Sr.", "Sra.", "Srta.", "Dr.", "Dra.", "Sr", "Sra", "Dr", "Dra"]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix) :].strip()  # noqa: E203
    return name


def generate_person_client() -> dict:
    """Generate a fake individual client record.

    Produces realistic personal data such as a name, CPF, mother’s name,
    and birth date, using Brazilian formatting. The genre is randomly
    chosen from Masculino, Feminino, or Desconhecido.

    Returns:
        dict: A dictionary representing an individual client with fields:
            - name (str)
            - cpf (str)
            - birthDate (str)
            - motherName (str)
            - cnpj (None)
            - genre (str)
            - createdAt (str)
    """
    genre = random.choice(["Masculino", "Feminino", "Desconhecido"])

    if genre == "Masculino":
        name = clean_name(fake.name_male())
    elif genre == "Feminino":
        name = clean_name(fake.name_female())
    else:
        name = clean_name(fake.name())

    return {
        "name": name,
        "cpf": fake.cpf(),
        "birthDate": fake.date_time_between(
            start_date="-80y", end_date="-18y"
        ).isoformat(),
        "motherName": clean_name(fake.name_female()),
        "cnpj": None,
        "genre": genre,
        "createdAt": fake.date_time_between(
            start_date="-2y", end_date="now"
        ).isoformat(),
    }


def generate_company_client() -> dict:
    """Generate a fake company client record.

    Produces a realistic Brazilian company name (with suffixes like
    "Ltda." or "S.A.") and CNPJ. Personal fields are set to None.

    Returns:
        dict: A dictionary representing a company client with fields:
            - name (str)
            - cpf (None)
            - birthDate (None)
            - motherName (None)
            - cnpj (str)
            - genre (None)
            - createdAt (str)
    """
    company_name = fake.company()
    suffixes = ["Ltda.", "S.A.", "ME", "EIRELI"]
    if not any(suffix in company_name for suffix in suffixes):
        company_name += f" {random.choice(suffixes)}"

    return {
        "name": company_name,
        "cpf": None,
        "birthDate": None,
        "motherName": None,
        "cnpj": fake.cnpj(),
        "genre": None,
        "createdAt": fake.date_time_between(
            start_date="-3y", end_date="now"
        ).isoformat(),
    }


def generate_clients(population_size: int, ratio: int = 100) -> list[dict]:
    """Generate a list of fake clients (people and companies).

    Generates a mixed population of individual and company clients
    according to the given ratio. For example, with ratio=100 and
    population_size=1000, it creates 1000 people and 10 companies.

    Args:
        population_size (int): Number of individual (person) clients to generate.
        ratio (int, optional): Number of people per company. Defaults to 100.

    Returns:
        list[dict]: A list of dictionaries, each representing a client record.
    """
    people_count = population_size
    company_count = max(1, people_count // ratio)

    clients = [generate_person_client() for _ in range(people_count)]
    clients += [generate_company_client() for _ in range(company_count)]

    return clients


def save_clients_to_csv(
    clients: list[dict], filename: Path = "data/clients.csv"
) -> None:
    """Save client records to CSV using pandas.

    Args:
        clients (list[dict]): List of client records.
        filename (str): CSV file path.
    """

    Path(filename).parent.mkdir(exist_ok=True)

    df = pd.DataFrame(clients)
    df = df.sample(frac=1)
    df.to_csv(filename, index=False, encoding="utf-8")


if __name__ == "__main__":
    clients = generate_clients(population_size=9900, ratio=100)
    save_clients_to_csv(clients)
