import json
import oapackage
from openpyxl import Workbook


def generate_web_testing_combinations(factors, levels, runs=None):
    """
    Generates web testing combinations using an orthogonal array from oapackage.

    Args:
        factors (list): A list of strings representing the testing factors (e.g., ["Browser", "Device"]).
        levels (dict): A dictionary mapping each factor to a list of its possible levels (e.g., {"Browser": ["Chrome", "Firefox"]}).
        runs (int, optional): The desired number of test cases (rows in the orthogonal array).
            Defaults to None, which uses a suitable default based on oapackage behavior.

    Returns:
        list: A list of dictionaries, where each dictionary represents a test case combination.
    """

    if len(factors) != len(levels):
        raise ValueError("Number of factors must match the number of level dictionaries.")

    if runs is None:
        runs = find_suitable_runs(factors, levels)

    array_class = oapackage.arraydata_t(len(levels[factors[0]]), runs, len(factors), len(factors))
    # array_class = oapackage.arraydata_t(len(levels[factors[0]]), runs, len(factors), 2)  # Strength changed to 2
    array_link = array_class.create_root()

    generated_array = array_link.getarray()

    combinations = []

    for i in range(runs):
        combination = {}
        for j, factor in enumerate(factors):
            combination[factor] = levels[factor][generated_array[i][j] % len(levels[factor])]
        combinations.append(combination)

    return combinations


def find_suitable_runs(factors, levels):
    """
    Find a suitable number of runs (test cases) for the orthogonal array.

    This example implementation simply returns a placeholder value.
    Replace it with your logic to determine the optimal or desired number of runs
    based on factors, levels, and testing coverage requirements.

    Args:
        factors (list): A list of testing factors.
        levels (dict): A dictionary mapping factors to their levels.

    Returns:
        int: The estimated or desired number of test cases.
    """

    return 6


def write_combinations_to_excel(combinations, filename="web_testing_combinations.xlsx"):
    """
    Writes web testing combinations to an Excel file.

    Args:
        combinations (list): A list of dictionaries representing test case combinations.
        filename (str, optional): The filename of the Excel file. Defaults to "web_testing_combinations.xlsx".
    """

    wb = Workbook()
    ws = wb.active

    header_row = [factor for factor in combinations[0].keys()]
    ws.append(header_row)

    for combination in combinations:
        data_row = [combination[factor] for factor in combinations[0].keys()]
        ws.append(data_row)

    wb.save(filename)

def update_environment_combinations(combinations, env_config_file="environment.json", output_file="updated_env.json"):
    with open(env_config_file, 'r') as f:
        env_config = json.load(f)

    updated_env = []

    for combination in combinations:
        env_key = combination['env'].lower()
        browser_key = combination['browser'].lower()
        if env_key in env_config['env'] and browser_key in env_config['browser']:
            updated_env.append({
                "env": env_config['env'][env_key],
                "browser": env_config['browser'][browser_key],
                "windows_height": env_config['window_height'],
                "window_width": env_config['window_width'],
                "receiver_email": env_config['receiver_email']
            })

    with open(output_file, 'w') as f:
        json.dump(updated_env, f, indent=2)

    print(f"Updated environment combinations written to '{output_file}'")

if __name__ == "__main__":
    # Define factors and levels for web testing
    # factors = ["Device", "Operating System", "Environment"]
    # levels = {
    #     "Device": ["Samsung", "Oppo", "Redmi", "Oneplus"],
    #     "Operating System": ["Android 11", "Android 12", "Android 13", "Android 14"],
    #     "Environment": ["QA", "Staging", "Prod"]
    # }

    factors = ["env", "browser"]
    levels = {
        "env": ["QA", "Staging", "Prod"],
        "browser": ["chrome", "firefox", "edge"]
    }

    # Generate combinations
    test_combinations = generate_web_testing_combinations(factors, levels)

    # Write combinations to Excel
    # write_combinations_to_excel(test_combinations)

    # print(f"Web testing combinations written to 'web_testing_combinations.xlsx'")
    update_environment_combinations(test_combinations)

