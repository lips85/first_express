def save_to_file(jobs, keyword):
    file = open(f"{keyword}.csv", mode="w", encoding="utf-8")

    file.write("position,company,location,URL")

    for job in jobs:
        file.write(f"\n{job['position']},{job['company']},{job['region']},{job['link']}")

    file.close()