from business.SearchManager_Class import SearchManager


if __name__ == '__main__':
    sm = SearchManager("./data/test.db")
    hotels = sm.get_all_hotels()
    for hotel in hotels:
        print(hotel)
        mein_print = print("HAHA")
        print(mein_print)