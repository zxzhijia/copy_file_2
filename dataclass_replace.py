# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:22:38 2025

@author: xuzha
"""

from dataclasses import dataclass, is_dataclass, replace, fields

def update_dataclass(dc_instance, updates):
    """
    Recursively update a dataclass instance using a dictionary of updates.
    
    Parameters:
      dc_instance: The dataclass instance to update.
      updates: A dict where keys correspond to field names in dc_instance.
               If a field is itself a dataclass and the update value is a dict,
               it will be updated recursively.
    
    Returns:
      A new instance of the dataclass with the updates applied.
    """
    # Build a dictionary of new values for the fields we want to update.
    new_field_values = {}
    for field in fields(dc_instance):
        # If this field is in the updates dict, prepare its new value.
        if field.name in updates:
            current_value = getattr(dc_instance, field.name)
            new_value = updates[field.name]
            # If the field is a dataclass and the update is given as a dict,
            # recursively update that nested dataclass.
            if is_dataclass(current_value) and isinstance(new_value, dict):
                new_field_values[field.name] = update_dataclass(current_value, new_value)
            else:
                new_field_values[field.name] = new_value
        # Otherwise, keep the current value (or you can skip it, since replace uses
        # the current instance's value by default).
    
    # Use replace to create a new instance with the updated values.
    return replace(dc_instance, **new_field_values)

# Example usage:

@dataclass(frozen=True)
class Address:
    street: str
    city: str

@dataclass(frozen=True)
class Person:
    name: str
    age: int
    address: Address

# Create an initial instance
p = Person(name="Alice", age=30, address=Address(street="123 Main St", city="Springfield"))

# Prepare an update dictionary.
# Note that the key "address" corresponds to the nested dataclass,
# and its value is itself a dictionary of updates.
updates = {
    "age": 31,
    "address": {
        "city": "Shelbyville"
    }
}

# Get a new instance with updates applied
p_updated = update_dataclass(p, updates)

print(p_updated)
