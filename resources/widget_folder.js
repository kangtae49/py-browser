send_list_directory = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action="api_list_directory",
    callback="Pb.callbacks.appendData",
    path=null,
    is_root=false
} = {}) => { 
    Pb.sendMessage(FolderReq.parse({ sender_id, receiver_id, action, callback, path, is_root,}));}

send_open_file = ({
    sender_id=WidgetId.enum.WIDGET_FOLDER,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action="api_open_file",
    callback=null,
    path=null,
} = {}) => { Pb.sendMessage(OpenFileReq.parse({sender_id, receiver_id,action, callback, path, }));}
