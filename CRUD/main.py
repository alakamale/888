from src.data_layer.data_manager import DataManager

def main():
    data_manager = DataManager()
    print("=" * 25)
    print("  CRUD - SIMPLIFIED")
    print("=" * 25)
    print("1. ENTER NEW DATA:")
    print("2. DISPLAY DATA:")
    print("3. UPDATE DATA:")
    print("4. DELETE ENTRY:")
    print("5. EXIT")

    choice = input("\nEnter your choice : ")

    if choice == '1':
        try:
            table_to_edit_ch = int(input("1. Sports \n2. Events \n3. Selection\n\tSelect table to add entry :  "))
        except ValueError:
            print("ERROR : Sorry, Incorrect response.")
            main()

        if table_to_edit_ch == 1:
            print("<=== ADD SPORT ===>")
            while True:
                data_manager.add_a_sport()
                if input('# Do you want to continue adding Sport : ') == 'y':
                    continue
                else:
                    data_manager.commit_data()
                    main()
        elif table_to_edit_ch == 2:
            print("<=== ADD EVENT ===>")
            sport_name = data_manager.get_id(data_manager.sports_tab, "sport_Name")
            while True and sport_name:
                data_manager.add_a_event(sport_name)
                if input('Do you want to continue adding Event : ') == 'y':
                    continue
                else:
                    data_manager.commit_data()
                    main()
        else:
            print("<=== ADD SELECTION ===>")
            event_name = data_manager.get_id(data_manager.events_tab, "event_Name")
            while True and event_name:
                data_manager.add_a_selection(event_name)
                if input('Do you want to continue adding Selection : ') == 'y':
                    continue
                else:
                    data_manager.commit_data()
                    main()

    elif choice == '2':
        data_manager.display_data(data_manager.sports_tab, header_lst=sport_header())
        data_manager.display_data(data_manager.events_tab, header_lst=event_header())
        data_manager.display_data(data_manager.selection_tab, header_lst=selection_header())
        main()

    elif choice == '3':
        try:
            table_to_edit_ch = int(input("1. Sports \n2. Events \n3. Selection\n\tSelect table to add entry :  "))
        except ValueError:
            print("ERROR : Sorry, Incorrect response.")
            main()

        if table_to_edit_ch == 1:
            data_manager.display_data(data_manager.sports_tab, header_lst=sport_header())
            key_to_edit = input("\tEnter Sport Name to edit : ")
            data_manager.update_sport_tab_feild(data_manager.sports_tab, key_to_edit)
            main()
        elif table_to_edit_ch == 2:
            data_manager.display_data(data_manager.events_tab, header_lst=event_header())
            key_to_edit = input("\tEnter Event Name to edit : ")
            data_manager.update_event_tab_feild(data_manager.events_tab, key_to_edit)
            main()
        else:
            data_manager.display_data(data_manager.selection_tab, header_lst=selection_header())
            key_to_edit = input("\tEnter Selection Name to edit : ")
            data_manager.update_selection_tab_feild(data_manager.selection_tab, key_to_edit)
            main()

    elif choice == '4':
        try:
            table_to_edit_ch = int(input("1. Sports \n2. Events \n3. Selection\n\tSelect table to add entry :  "))
        except ValueError:
            print("ERROR : Sorry, Incorrect response.")
            main()

        if table_to_edit_ch == 1:
            data_manager.display_data(data_manager.sports_tab, header_lst=sport_header())
            key_to_edit = input("\tEnter Sport Name to Delete : ")
            data_manager.delete_tab_feild(data_manager.sports_tab, key_to_edit)
            main()
        elif table_to_edit_ch == 2:
            data_manager.display_data(data_manager.events_tab, header_lst=event_header())
            key_to_edit = input("\tEnter Event Name to Delete : ")
            data_manager.delete_tab_feild(data_manager.events_tab, key_to_edit)
            main()
        else:
            data_manager.display_data(data_manager.selection_tab, header_lst=selection_header())
            key_to_edit = input("\tEnter Selection Name to Delete : ")
            data_manager.delete_tab_feild(data_manager.selection_tab, key_to_edit)
            main()
    else :
        exit(0)


def sport_header():
    print("Display Data, ")
    print("=" * 17)
    print("  SPORTS TABLE")
    print("=" * 17)
    sports_hdr_lst = ['Sport Name', 'Slug', 'Active']
    return sports_hdr_lst


def event_header():
    print("=" * 17)
    print("  EVENTS TABLE")
    print("=" * 17)
    events_hdr_lst = ['Event Name', 'Slug', 'Active', 'Type', 'Sport Name', 'Event Status', 'Schedule Start',
                      'Actual Start']
    return events_hdr_lst


def selection_header():
    print("=" * 17)
    print("  SELECTION TABLE")
    print("=" * 17)
    selection_hdr_lst = ['Selection Name', 'Event Name', 'Price', 'Active', 'Outcome']
    return selection_hdr_lst


if __name__ == "__main__":
    main()
