from links import all_urls
from scrape import scrape

def main():
  print("Main running...")
  for index, url in enumerate(all_urls):
    print("\nScrape Started")
    file_name = f"data/scraped_data_{index}.json"
    scrape(url, file_name)
    print("Scrape Ended")


if __name__ == "__main__":
  main()