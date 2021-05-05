from helpers import *
import concurrent.futures

def main():
    '''
    Use the setting to filter the result
    AGE_GROUP.BOTH: For all both 18-44 and 45 above
    AGE_GROUP.YOUNG: For 18-44 only
    AGE_GROUP.OLD: For above 45
    '''
    Settings(AGE_GROUP.BOTH)

    '''
    Get District ids by state (ref README.md for state_id)
    https://cdn-api.co-vin.in/api/v2/admin/location/districts/<state_id>
    '''
    districts = []  # District ids to check
    pincodes = []  # Pincodes to check
    argslist = []
    for district in districts:
        argslist.append((district, 'district'))

    for pincode in pincodes:
        argslist.append((pincode, 'pincode'))

    results = ['Vaccine Availability']
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        result = executor.map(lambda args: find_monthly_vaccine(*args), argslist)

    for r in result:
        results.extend(r)

    # If you want to send sms then configure aws credentials in helpers.py, send_sms
    # Uncomment the below function
    # send_sms(results)


if __name__ == '__main__':
    main()
