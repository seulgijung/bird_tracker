import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def scrape_ebird_alerts():
    """Scrape eBird rare bird alerts and return as list of dictionaries."""

    url = "https://ebird.org/alert/summary?sid=SN35466"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    print(f"Fetching: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    observations = soup.select('.Observation')
    print(f"Found {len(observations)} observations")

    data = []

    for obs in observations:
        row = {}

        # Species
        species_el = obs.select_one('.Heading-main')
        row['species'] = species_el.get_text(strip=True) if species_el else None

        # Scientific name
        sci_el = obs.select_one('.Heading-sub--sci')
        row['scientific_name'] = sci_el.get_text(strip=True) if sci_el else None

        # Count
        count_el = obs.select_one('.Observation-numberObserved')
        if count_el:
            count_text = count_el.get_text(strip=True).replace('Number observed:', '').strip()
            row['count'] = count_text
        else:
            row['count'] = None

        # Status
        status_el = obs.select_one('.Observation-tags strong')
        row['status'] = status_el.get_text(strip=True) if status_el else None

        # Date
        date_link = obs.select_one('a[href*="/checklist/"]')
        row['date'] = date_link.get_text(strip=True) if date_link else None

        # Checklist URL
        if date_link:
            href = date_link.get('href', '')
            row['checklist_url'] = 'https://ebird.org' + href if href.startswith('/') else href
        else:
            row['checklist_url'] = None

        # Location
        location_link = obs.select_one('a[href*="google.com/maps"]')
        row['location'] = location_link.get_text(strip=True) if location_link else None

        # Coordinates
        if location_link:
            href = location_link.get('href', '')
            coord_match = re.search(r'query=([0-9.-]+),([0-9.-]+)', href)
            if coord_match:
                row['latitude'] = float(coord_match.group(1))
                row['longitude'] = float(coord_match.group(2))
            else:
                row['latitude'] = None
                row['longitude'] = None
        else:
            row['latitude'] = None
            row['longitude'] = None

        # Observer
        row['observer'] = None
        for cell in obs.select('.GridFlex-cell'):
            hidden = cell.select_one('.is-visuallyHidden')
            if hidden and 'Observer' in hidden.get_text():
                span = cell.select_one('span:not(.is-visuallyHidden)')
                if span:
                    row['observer'] = span.get_text(strip=True)
                break

        if row['species']:
            data.append(row)

    return data


def main():
    print(f"Starting scrape at {datetime.now().isoformat()}")

    # Scrape data
    sightings = scrape_ebird_alerts()

    # Create output
    output = {
        "last_updated": datetime.now().isoformat(),
        "alert_name": "New York Rare Bird Alert",
        "alert_url": "https://ebird.org/alert/summary?sid=SN35466",
        "total_sightings": len(sightings),
        "sightings": sightings
    }

    # Save to JSON
    with open("data.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved {len(sightings)} sightings to data.json")
    print(f"Last updated: {output['last_updated']}")


if __name__ == "__main__":
    main()
