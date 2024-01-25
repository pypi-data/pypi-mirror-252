# ActionNetworkPy

ActionNetworkPy is an unofficial Python client for the Action Network API. This package allows Python developers to easily integrate with the Action Network's suite of tools for organizing and managing various aspects of digital activism and campaign management.

With ActionNetworkPy, you can programmatically access and manipulate resources such as people, events, petitions, donations, and more, all through the Action Network API. This client handles the intricacies of API communication, allowing you to focus on creating powerful applications for social change.

## Key Features

- **Simple Integration**: Set up with just your OSDI API token and start interacting with the API immediately.
- **Comprehensive Models**: Access a wide range of Action Network resources, including campaigns, events, and donations.
- **Convenience Methods**: Easily list, create and update resources with straightforward Python methods.
- **Pagination Support**: Navigate through large sets of data with built-in pagination support.

## Getting Started

To get started with ActionNetworkPy, you'll need an OSDI API token from ActionNetwork. Once you have your token, you can install the package and begin using it in your project.

## Requirements

- Python 3.6+

## Installation

To install ActionNetworkPy, run the following command:
```sh
pip install py-actionnetworkorg
```

## Usage

Here's a quick example to get you started:
```sh
from action_network import ActionNetwork
# Initialize with your OSDI API token
an = ActionNetwork(osdi_token="your_osdi_api_token")

# Create a new person
person_payload = {
"person": {
"family_name": "Doe",
"given_name": "Jane",
"postal_addresses": [{"postal_code": "20009"}],
"email_addresses": [{"address": "jane.doe@example.com"}],
"phone_numbers": [{"number": "2025550123"}]
},
"add_tags": ["supporter"],
"remove_tags": ["prospect"]
}
# Add the person or many persons to Action Network
response = an.people.create(payloads=[person_payload])
print(response)
# OR
# Add a single person to Action Network
response = an.person.create(payloads=person_payload)
print(response)
```

### Support

If you encounter any issues or have questions regarding `py-actionnetworkorg`, please file an issue on the GitHub repository or contact the maintainers.