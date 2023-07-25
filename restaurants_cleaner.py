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


def to_icon_type(cuisine):
    for icon, cuisines in ICON_CUISINE_MAP.items():
        if cuisine in cuisines:
            return icon


with open("./restaurants.json") as f:
    data = json.load(f)

data = [item["fields"]["promocodeFor"]["fields"] for item in data]
restaurants = []
all_cuisines = []

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
    tags = [item["fields"]["title"] for item in row["secondaryCategories"]]
    cuisines = [
        item["fields"]["title"]
        for item in row["secondaryCategories"]
        if item["fields"]["categoryGroupName"] == "Cuisine"
    ]
    b2b = row.get("b2breferences", [])
    amenities = [
        {
            "name": amenity["NAME"],
            "type": amenity["TYPE"],
            "value": amenity["VALUE"],
        }
        for item in b2b
        for amenities in item["fields"]["amenitiesJSON"].values()
        for amenity in amenities
    ]
    all_cuisines.extend(cuisines)
    cuisine = cuisines[0] if cuisines else None
    icon = to_icon_type(cuisine)

    restaurants.append(
        dict(
            title=title,
            address=address,
            location=location,
            description=description,
            cuisine=cuisine,
            icon=icon,
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
