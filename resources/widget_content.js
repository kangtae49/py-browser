send_list_directory = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.LIST_DIRECTORY,
    path=null,
    select_path=null,
    depth=1,
} = {}) => { 
    console.log('send_list_directory');
    Pb.sendMessage(FolderReq.parse({ sender_id, receiver_id, action, path, select_path, depth,}));
}

send_get_state = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.GET_STATE,
    key=null,
} = {}) => { 
    console.log(`send_get_state: ${key}`);
    Pb.sendMessage(GetStateReq.parse({sender_id, receiver_id,action, key,}));
}

send_set_state = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.SET_STATE,
    key=null,
    value=null,
} = {}) => { 
    console.log(`send_set_state: ${key}=${value}`);
    Pb.sendMessage(SetStateReq.parse({sender_id, receiver_id,action, key, value,}));
}

send_open_path = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.OPEN_PATH,
    open_path_type=OpenPathType.enum.AUTO,
    path=null,
    cmd_name=null,
} = {}) => {
    console.log(`send_open_path: ${receiver_id} ${action}`); 
    Pb.sendMessage(OpenPathReq.parse({sender_id, receiver_id,action, open_path_type, path, cmd_name,}));
}


