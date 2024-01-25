import sys
import os
import shutil

tabular_data_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tabular_data")

if os.path.exists(tabular_data_directory):
    shutil.rmtree(tabular_data_directory)

os.makedirs(tabular_data_directory)

current_directory = os.path.dirname(os.path.realpath(__file__))

google_maps_scraper_directory = os.path.join(current_directory, "google-maps-scraper")
sys.path.append(google_maps_scraper_directory)
output_directory = os.path.join(google_maps_scraper_directory, "output")

if os.path.exists(output_directory):
    shutil.rmtree(output_directory)

os.chdir(google_maps_scraper_directory)
import main

def obtain_places(query, city):
    main.obtain_restaurants(query, city)

    tabular_data_directory = os.path.join(current_directory, "tabular_data")

    if not os.path.exists(tabular_data_directory):
        os.makedirs(tabular_data_directory)

    city_formatted = city.lower().replace(" ", "-")
    specific_output_directory = os.path.join(output_directory, f"{query}-in-{city_formatted}/csv")

    print(specific_output_directory)

    if os.path.exists(specific_output_directory):

        for file_name in os.listdir(specific_output_directory):
            source_path = os.path.join(specific_output_directory, file_name)
            destination_path = os.path.join(tabular_data_directory, file_name)
            shutil.move(source_path, destination_path)