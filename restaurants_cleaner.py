import json

ICON_CUISINE_MAP = {
    "pizza": ["Italian", "Pizza"],
    "burger": [
        "American (New)",
        "American (Traditional)",
        "Steakhouse",
        "Burgers",
        "Barbecue",
        "Gastropub",
        "Soul Food / Southern",
    ],
    "bread": [
        "French",
        "Belgian",
        "Austrian",
        "Irish",
        "Ukrainian",
        "Modern European",
        "Eastern European",
    ],
    "latin": [
        "Mexican",
        "Dominican",
        "Spanish",
        "Cuban",
        "Latin American",
        "Peruvian",
        "Puerto Rican",
        "Argentinian",
        "Brazilian",
    ],
    "asian": [
        "Japanese / Sushi",
        "Chinese",
        "Thai",
        "Asian Fusion",
        "Korean",
        "Pan-Asian",
        "Vietnamese",
        "Malaysian",
        "Laotian",
    ],
    "kebab": ["Mediterranean", "Greek", "Turkish", "Middle Eastern"],
    "other": [
        "Eclectic",
        "Caribbean",
        "Indian",
        "Jamaican",
        "African",
        "Ethiopian",
        "Hawaiian",
        "Fusion",
        "Southwestern",
        "Dessert",
        "Vegetarian",
        "Vegan",
        "Cajun/Creole",
        "Delicatessen",
        "Eastern European",
        "Coffeehouse",
        "Continental",
    ],
}


def to_category(cuisine):
    for icon, cuisines in ICON_CUISINE_MAP.items():
        if cuisine in cuisines:
            return icon
    return "other"


def get_tags(secondaryCategories):
    tags = {}
    for item in secondaryCategories:
        key = item["fields"]["categoryGroupName"]
        if key in ["Taxonomy", "Location", "Promotion", "Special Designation"]:
            continue
        if key not in tags:
            tags[key] = []
        tags[key].append(item["fields"]["title"])
    return tags


def get_amenities(b2breferences):
    flattened = [
        {
            "name": amenity["NAME"],
            "type": amenity["TYPE"],
            "value": amenity["VALUE"],
        }
        for item in b2breferences
        for amenities in item["fields"]["amenitiesJSON"].values()
        for amenity in amenities
    ]
    amenities = {}
    for item in flattened:
        match item["type"]:
            case "Yes/No":
                amenities[item["name"]] = bool(item["value"])
            case "Number" | "Multi-Select" | "Dropdown":
                amenities[item["name"]] = item["value"]
    return amenities


with open("./restaurants.json") as f:
    data = json.load(f)

data = [item["fields"]["promocodeFor"]["fields"] for item in data]
restaurants = []

for row in data:
    title = row["title"]
    address = row["venueAddress"]
    location = row.get("location")
    description = row.get("summary", "")
    instagram = row.get("instagram")
    url = row["websiteUrl"]
    phone = row["phone"]
    twitter = row.get("twitterHandle")
    pinterest = row.get("pinterest")
    integrations = []
    integrations = {item["fields"]["partnerName"]: item["fields"].get("url") for item in row.get("ecommerce", [])}
    images = [item["fields"]["image"]["fields"]["file"]["url"] for item in row.get("images", [])]
    tags = get_tags(row["secondaryCategories"])
    amenities = get_amenities(row.get("b2breferences", []))
    cuisine = tags["Cuisine"][0]
    price = tags.get("Cost")
    category = to_category(cuisine)

    restaurants.append(
        dict(
            title=title,
            address=address,
            location=location,
            description=description,
            cuisine=cuisine,
            price=price,
            category=category,
            instagram=instagram,
            url=url,
            phone=phone,
            twitter=twitter,
            pinterest=pinterest,
            integrations=integrations,
            images=images,
            tags=tags,
            amenities=amenities,
        )
    )


with open("./restaurants-clean.json", "w") as f:
    json.dump(restaurants, f, indent=2, sort_keys=False)
