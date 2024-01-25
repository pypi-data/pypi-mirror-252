import click
import pkg_resources
from pathlib import Path
from .process_data import process_data,read_input_file,sort_data_by_hierarchy,validate_data,print_values_in_csv_format


class MainClass:
    def __init__(self, **kwargs):
        self.data = kwargs

    def get_info(self):
        d1 = {}
        for key, value in self.data.items():
            d1[key] = value
        return d1

@click.command()
@click.option('--keys', multiple=True, help='List of key:data_type pairs')
@click.option('--hierarchy', help='Hierarchy string')
def main(keys, hierarchy):
    # Process input data
    input_data = {}
    if keys:
        for item in keys:
            try:
                key, data_type = item.split(":")
                # Check if data_type is one of the allowed types (you can extend this list)
                allowed_types = ["int", "str"]
                if data_type not in allowed_types:
                    raise ValueError(f"Invalid data type: {data_type}. Allowed types are {', '.join(allowed_types)}")
                
                # Here, you may want to add additional checks for specific data types
                input_data[key] = data_type
            except ValueError as e:
                click.echo(f"Error processing key:data_type pair '{item}': {e}")
                exit(1)

    # Create an instance of MainClass with provided inputs
    main_instance = MainClass(**input_data)

    # Read input file
    file_name = "input.txt"
    input_path = pkg_resources.resource_filename(__name__, f"data/{file_name}")
        
    input_file_path = Path(input_path)
    raw_data = read_input_file(input_file_path)

    # Process data
    processed_data = process_data(raw_data, list(main_instance.get_info().keys()))

    # Sort data by hierarchy
    hierarchy_keys = hierarchy.split("-")
    sorted_data = sort_data_by_hierarchy(processed_data, hierarchy_keys)

    # Validate data
    validated_data = validate_data(sorted_data, main_instance.get_info())

    # Print values in CSV format
    final_data = print_values_in_csv_format(validated_data, list(main_instance.get_info().keys()))

    for line in final_data:
        print(line)

if __name__ == '__main__':
    main()