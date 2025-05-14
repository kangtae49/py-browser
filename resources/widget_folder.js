send_list_directory = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action=ActionId.enum.LIST_DIRECTORY,
    path=null,
    is_root=false
} = {}) => { 
    Pb.sendMessage(FolderReq.parse({ sender_id, receiver_id, action, path, is_root,}));}

send_open_path = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action=ActionId.enum.OPEN_PATH,
    path=null,
} = {}) => { Pb.sendMessage(OpenPathReq.parse({sender_id, receiver_id,action, path, }));}

