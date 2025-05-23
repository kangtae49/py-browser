send_list_directory = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action=ActionId.enum.LIST_DIRECTORY,
    path=null,
    select_path=null,
    depth=1
} = {}) => { 
    Pb.sendMessage(FolderReq.parse({ sender_id, receiver_id, action, path, select_path, depth,}));}

send_open_path = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action=ActionId.enum.OPEN_PATH,
    open_path_type=OpenPathType.enum.AUTO,
    path=null,
    cmd_name=null,
} = {}) => { Pb.sendMessage(OpenPathReq.parse({sender_id, receiver_id,action, open_path_type, path, cmd_name,}));}

send_get_link = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action=ActionId.enum.GET_LINK,
} = {}) => { Pb.sendMessage(GetLinkReq.parse({sender_id, receiver_id,action, }));}
