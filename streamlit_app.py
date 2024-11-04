import streamlit as st
import requests
import pandas as pd

def search_provider(name, address, specialty):
    url = 'https://api.ribbonhealth.com/v1/custom/providers?page_size=10'
    if name:
        url += f'&name={name}'
    if address:
        url += f'&address={address}'
    if specialty:
        url += f'&specialty={specialty}'

    headers = {
        'Authorization': 'Bearer 415842adedfe56cdc9089ae19e4eac192a7d67f6'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def display_results(data):
    results = []
    for provider in data.get('data', []):
        npi = provider.get('npi', 'N/A')
        provider_name = f"{provider.get('first_name', '')} {provider.get('middle_name', '')} {provider.get('last_name', '')}".strip()
        locations = provider.get('locations', [])
        if locations:
            location = locations[0]
            address = location.get('address', 'N/A')
            phone_numbers = location.get('phone_numbers', [])
            phone = phone_numbers[0].get('phone', 'N/A') if phone_numbers else 'N/A'
        else:
            address = 'N/A'
            phone = 'N/A'

        results.append([npi, provider_name, address, phone])

    return results

def main():
    st.set_page_config(layout="wide")
    st.title("Provider Search")
    st.write("Search for providers by name, address, and specialty")

    name = st.text_input("Enter Provider Name:")
    address = st.text_input("Enter Address, City or Zip code:")
    specialty = st.text_input("Enter Specialty:")

    if st.button("Search"):
        try:
            data = search_provider(name, address, specialty)
            results = display_results(data)

            if results:
                df = pd.DataFrame(results, columns=['NPI', 'Provider Name', 'Address', 'Phone Number'])
                st.dataframe(df)
            else:
                st.write("No providers found.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
