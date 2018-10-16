from main_server_client import *

if __name__ == "__main__":
    
  main_server_addr = ['', 8008]
  main_server_client = MainServerClient(main_server_addr)

  while True:
    desktop_id = input("Enter desktop Id: ")
    status, address  = main_server_client.get_desktop_address(desktop_id)
    print(status, address)
    break 

  main_server_client.close()


