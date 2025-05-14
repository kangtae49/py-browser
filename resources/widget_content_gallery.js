send_list_directory = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.LIST_DIRECTORY,
    path=null,
    is_root=false
} = {}) => { 
    console.log('send_list_directory');
    Pb.sendMessage(FolderReq.parse({ sender_id, receiver_id, action, path, is_root,}));
}

send_get_state = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.GET_STATE,
    key=null,
} = {}) => { 
    console.log('send_get_state');
    Pb.sendMessage(GetStateReq.parse({sender_id, receiver_id,action, key,}));
}

send_set_state = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.SET_STATE,
    key=null,
    value=null,
} = {}) => { 
    console.log('send_set_state');
    Pb.sendMessage(SetStateReq.parse({sender_id, receiver_id,action, key, value,}));
}
