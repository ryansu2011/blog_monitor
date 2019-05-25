import src.scraper as scraper


ret = scraper.craw_all()
print(ret.__next__())
print("\n-----------------------------\n")
print(ret.__next__())
print("\n-----------------------------\n")
print(ret.__next__())
print("\n-----------------------------\n")

