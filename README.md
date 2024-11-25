# crypto-tracker

This projects is about traking of coins pricies.

## Project setup
- Python 3.12


### Setup envierment

```
python -m venv venv
source venv/bin/activate
pip install -r requirments.txt
```
 

### Environment variables

| Name                      | Required           | Description        |
| -------------             | :-------------:    | :-------------:    |
| SAMPLE_SPREADSHEET_ID     | `Yes`              | Google spreadsheet id in witch changes are expected |


## Setup google
### Configure the OAuth consent
1. [Configure OAuth consent](https://developers.google.com/workspace/guides/configure-oauth-consent)
2. [API key credentials](https://developers.google.com/workspace/guides/create-credentials#api-key)
3. Place data from previous step in the [credentials.json](/credentials.json)
