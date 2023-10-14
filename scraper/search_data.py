import scraper.database as db


def search(queries: list[str]) -> None:
    print("Searching...")

    for query in queries:
        search_functions = [search_product_name, search_category]
        searching_for_names = [
            ("product names", "product name(s)"),
            ("categories", "categories"),
        ]

        for search_function, searching_for_name in zip(search_functions, searching_for_names):
            results = search_function(query)

            if not results:
                print(f"\nFound nothing for search term '{query}' when searching for {searching_for_name[0]}")
                continue

            print(f"\nFound these {searching_for_name[1]} with search term '{query}':")
            for result in results:
                print(f"> {result}")
        print()


def search_product_name(product_name_search: str) -> list[str]:
    products_strings = []
    products = db.get_products_by_names_fuzzy([product_name_search])

    if not products:
        return []

    grouped_products = db.group_products_by_names(products)

    for products in grouped_products:
        matched_domains = []
        for product in products:
            match_string = f" - {product.domain.capitalize()} - {product.product_code}"
            matched_domains.append(match_string)
        matched_domains_string = "\n".join(matched_domains)
        products_strings.append(f"{products[0].name}\n{matched_domains_string}\n")

    return products_strings


def search_category(category_search: str) -> list[str]:
    all_categories = db.get_all_unique_categories()

    return [category for category in all_categories if category_search.lower() in category.lower()]
