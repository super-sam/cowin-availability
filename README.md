# Cowin Vaccine Availability
Check if the vaccine is available by district or pincode and send SMS via AWS SNS

## Prerequisite
- [x] Python3
- [ ] boto3 (Optional) - Only if you want to send SMS

- Configure District ID / Pincode at index.py, main function

## How to run locally
`python3 index.py`
## State IDs
API: https://cdn-api.co-vin.in/api/v2/admin/location/states 

State | Id 
--- | ---
Andaman and Nicobar Islands | 1
Andhra Pradesh | 2
Arunachal Pradesh | 3
Assam | 4
Bihar | 5
Chandigarh | 6
Chhattisgarh | 7
Dadra and Nagar Haveli | 8
Daman and Diu | 37
Delhi | 9
Goa | 10
Gujarat | 11
Haryana | 12
Himachal Pradesh | 13
Jammu and Kashmir | 14
Jharkhand | 15
Karnataka | 16
Kerala | 17
Ladakh | 18
Lakshadweep | 19
Madhya Pradesh | 20
Maharashtra | 21
Manipur | 22
Meghalaya | 23
Mizoram | 24
Nagaland | 25
Odisha | 26
Puducherry | 27
Punjab | 28
Rajasthan | 29
Sikkim | 30
Tamil Nadu | 31
Telangana | 32
Tripura | 33
Uttar Pradesh | 34
Uttarakhand | 35
West Bengal | 36
