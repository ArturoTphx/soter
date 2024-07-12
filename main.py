from argparse import ArgumentParser
from sites import Sites
import requests

verbose = False


def console(message: str):
    if verbose:
        print(message)


def is_valid_site(site: str) -> bool:
    for key, value in Sites.items():
        if key.lower() == site.lower():
            return value
    return None


def make_request(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        console(f"Error: {e}")
    return None


def save_to_file(content: str, site_name: str):
    with open(f"{site_name}.html", "w") as file:
        file.write(content)


def main(site: str, is_verbose: bool, is_save: bool):
    global verbose
    verbose = is_verbose
    site_entry = is_valid_site(site)
    if not site_entry:
        print("Invalid site")
        return

    if verbose:
        print("Verbose mode is on")
    else:
        print("Verbose mode is off")

    site_name = site_entry["name"]
    site_url = site_entry["url"]

    console(f"Site: {site_name}")
    console(f"URL: {site_url}")

    html = make_request(site_url)
    console(f"HTML: {html}")

    if is_save:
        save_to_file(content=html, site_name=site_name)


parser = ArgumentParser(description="Soter")
parser.add_argument(
    "-s", "--site", type=str, help="site for the request (google|bing|youtube)"
)
group = parser.add_argument_group()
group.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
group.add_argument(
    "-f", "--save", action="store_true", help="save response in file mode"
)
args = parser.parse_args()


if __name__ == "__main__":
    is_verbose = args.verbose
    is_save = args.save
    site = args.site
    main(site=site, is_verbose=is_verbose, is_save=is_save)
