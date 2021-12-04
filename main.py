from melos import Melos

if __name__ == "__main__":
    # referral link
    url = ""
    # driver path
    driver_path = ""
    if url and driver_path:
        melos = Melos(driver_path)
        melos.start_referral(url)
    else:
        print("Failed to execute due to url or driver path not specified!")
