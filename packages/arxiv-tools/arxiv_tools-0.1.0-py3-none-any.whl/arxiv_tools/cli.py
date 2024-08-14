import arxiv
import pathlib
from datetime import datetime

DEBUG = 0


def is_debug():
    return DEBUG == 1


def get_pdf_folder():
    # if macos
    research_folder = pathlib.Path("/Users/xiuhao/Documents/Research")

    date_folder = datetime.now().strftime("%Y%m")

    # create folder if not exist
    pdf_folder = research_folder / date_folder / "papers" / "arxiv"
    pdf_folder.mkdir(parents=True, exist_ok=True)
    return pdf_folder


pdf_folder = get_pdf_folder()


def download(name: str):
    # Construct the default API client.
    client = arxiv.Client()

    if is_debug():
        print("searching name is: ", name)

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query=f"all:{name}",
        max_results=2,  # , sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = client.results(search)

    if is_debug():
        for r in results:
            print(r, r.title)

    for r in results:
        # download first pdf
        r.download_pdf(dirpath=str(pdf_folder))
        print("Downloaded:", r.title)


def main():
    import argparse

    # use argparser to get the name
    parser = argparse.ArgumentParser(description="Download arxiv papers")
    parser.add_argument("name", type=str, help="name of the paper")
    args = parser.parse_args()

    # download the paper
    download(args.name)


if __name__ == "__main__":
    main()
