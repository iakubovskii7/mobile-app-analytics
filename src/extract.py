import glob

import pandas as pd
from serpapi import GoogleSearch


def create_search_params(
    search_key: str,
    engine: str = "apple_app_store",
    device: str = "mobile",
    country: str = "us",
    lang: str = "en-us",
):
    return {
        "api_key": "a3a06a53ed09fd1543aca690eca6549abd5454255f438d1763266db50372d743",  # SerpApi search engine
        "engine": engine,
        "term": search_key,  # search query
        "device": device,  # device to get the results  desktop /
        "country": country,  # country for the search
        "lang": lang,  # language for the search
        "disallow_explicit": False,  # disallowing explicit apps
        "num": 200,  # number of items per page
        "page": 0,  # pagination
    }


# # app_store_results = []
all_results = []
all_terms = []
for file in glob.glob(f"../data/*"):
    df = pd.read_parquet(file)
    all_terms.extend(df["search_key"].unique().tolist())
for search_key in list(set(all_terms)):
    params = create_search_params(search_key=search_key)
    search = GoogleSearch(params)
    page_results = search.get_dict()
    results = pd.json_normalize(page_results["organic_results"]).assign(
        parsed_at=page_results["search_metadata"]["created_at"], search_key=search_key, source="parsed_serpapi"
    )
    all_results.append(results)
all_results = pd.concat(all_results)
all_results.to_parquet("../data/serpapi_7.parquet")
