#!/usr/bin/env python3.5
# Wesley Stutzman
# Rsync

# Designed to clone a client file to a server
# Only change files that have been edited since last update

import os
import sys
import shutil

# Return true if a path is file or directory
def check_valid_path(server_name):
  return os.path.isfile(server_name) or os.path.isdir(server_name)

class rsync:

  # Input in arguments from start
  def __init__(self, client_storage=None, server_storage=None):
    self.client_storage = client_storage
    self.server_storage = server_storage
    changes        = []
    
  # Check that files are valid and execute updates
  def update_changes(self):
    assert self.client_storage is not None
    assert self.server_storage is not None
    return self.update_changes_helper("")

  # Use recursion to check for update files
  def update_changes_helper(self, extension):
    # Create working paths for both root files with new extentions
    client_directory = os.path.join(self.client_storage, extension)
    server_directory = os.path.join(self.server_storage, extension)

    # Get the content of the current directory
    directory_content = sorted(os.listdir(client_directory))

    # Go through all items inside the directory
    for files in directory_content:
      client_new_path = os.path.join(client_directory, files)
      server_new_path = os.path.join(server_directory, files)

    # Recursivly climb through the directories
      if os.path.isdir(client_new_path):
        if not os.path.exists(server_new_path):
          os.makedirs(server_new_path)
          print("Creating Directory: " + server_new_path)
        self.update_changes_helper(os.path.join(extension, files))
      
    # Check if the file needs updating
      update_file = False
      if not os.path.exists(server_new_path):
        update_file = True
      elif os.path.getmtime(client_new_path) > os.path.getmtime(server_new_path):
        update_file = True
      
    # Update the file if needed
      if update_file:
        if os.path.isfile(client_new_path):
          shutil.copy(client_new_path, server_new_path)
          print("Updating File: " + server_new_path)

  # Start updating paths for the user
  def update_paths(self, client_storage=None, server_storage=None):
    if client_storage is not None:
      self.set_client_storage(client_storage)
    if server_storage is not None:
      self.set_server_storage(server_storage)

    self.update_changes()
    # assert self.client_storage or self.server_storage
    # changes = self.find_changes(self.client_storage, self.server_storage)
    
  # Set client server location name
  def set_client_storage(self, client_name):

    # Hold a return value for later
    return_value = None

    # Check for valid input
    if check_valid_path(client_name):
      self.client_storage = client_name
      return_value = client_name
    else:
      print("ERROR INVALID CLIENT NAME FOR STORAGE")
    return return_value

  # Set server storage location name
  def set_server_storage(self, server_name):
    
    # Hold a return value for later
    return_value = None

    # Check for valie input
    if check_valid_path(server_name):
      self.server_storage = server_name
      return_value = server_name
    else:
      print("ERROR INVALID CLIENT NAME FOR STORAGE")
    return return_value

if __name__ == "__main__":
  print("Starting")
  test = rsync()
  if len(sys.argv) == 3:
    test.update_paths(sys.argv[1], sys.argv[2])
  else:
    client_directory = input("Enter client directory: ")
    server_directory = input("Enter server directory: ")
    test.update_paths(client_directory, server_directory)
