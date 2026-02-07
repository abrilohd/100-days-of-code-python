from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from email_manager import EmailManager
from config.settings import EMAIL_ADDRESS

ORIGIN_CITY_IATA = "LON"  # change if you want different origin

def run_flight_check():
    print("[main] Starting a flight check run...")
    data_manager = DataManager()
    try:
        sheet_data = data_manager.get_destination_data()
    except Exception as e:
        print("[main] Failed to get sheet data:", e)
        return

    flight_search = FlightSearch()    # will get token internally (with retries)
    notification_manager = NotificationManager()
    email_manager = EmailManager()

    # Update missing IATA codes
    if sheet_data and sheet_data[0].get("iataCode", "") == "":
        for row in sheet_data:
            try:
                row["iataCode"] = flight_search.get_destination_code(row["city"])
            except Exception as e:
                print(f"[main] Could not get code for {row['city']}: {e}")
        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=6*30)

    for destination in sheet_data:
        try:
            flight = flight_search.check_flights(
                ORIGIN_CITY_IATA,
                destination["iataCode"],
                from_time=tomorrow,
                to_time=six_month_from_today
            )
        except Exception as e:
            print("[main] Error checking flights for", destination.get("city"), e)
            flight = None

        if flight:
            try:
                if float(flight.price) < float(destination["lowestPrice"]):
                    message = (
                        f"Low price alert! Only £{flight.price} to fly from "
                        f"{flight.origin_city}-{flight.origin_airport} to "
                        f"{flight.destination_city}-{flight.destination_airport}, "
                        f"from {flight.out_date} to {flight.return_date}."
                    )
                    notification_manager.send_sms(message)
                    # send email to configured address
                    if EMAIL_ADDRESS:
                        email_manager.send_email(subject="Flight Deal Alert!", body=message, to_email=EMAIL_ADDRESS)
            except Exception as e:
                print("[main] Error handling alert for", destination.get("city"), e)

    print("[main] Flight check finished.")

if __name__ == "__main__":
    run_flight_check()
