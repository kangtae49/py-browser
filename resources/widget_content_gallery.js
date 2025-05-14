send_list_directory = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_FOLDER,
    action=ActionId.enum.LIST_DIRECTORY,
    callback="Pb.callbacks.appendLayout",
    path=null,
    is_root=false
} = {}) => { 
    Pb.sendMessage(FolderReq.parse({ sender_id, receiver_id, action, callback, path, is_root,}));}

send_get_gallery_type = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.GET_GALLERY_TYPE,
    callback="Pb.callbacks.listenGalleryType",
} = {}) => { Pb.sendMessage(GetGalleryTypeReq.parse({sender_id, receiver_id,action, callback, gallery_type, }));}

send_set_gallery_type = ({
    sender_id=WidgetId.enum.WIDGET_CONTENT,
    receiver_id=WidgetId.enum.WIDGET_CONTENT,
    action=ActionId.enum.SET_GALLERY_TYPE,
    callback=null,
    gallery_type=null,
} = {}) => { Pb.sendMessage(SetGalleryTypeReq.parse({sender_id, receiver_id,action, callback, gallery_type, }));}
