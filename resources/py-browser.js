const z = Zod;

const ContentTemplate = z.enum([
    "CONTENT_LIST",
    "CONTENT_GALLERY"
]);

const FolderTemplate = z.enum([
    "FOLDER",
]);

const OpenPathType = z.enum([
    "AUTO",
    "WEBVIEW",
    "APPLICATION",
    "BROWSER",
]);

const GalleryType = z.enum([
    "LAYOUT_LIST",
    "LAYOUT_GALLERY"
]);

const StateKey = z.enum([
    "TEMPLATE",
    "GALLERY_TYPE",
    "PATH",
]);

const WidgetId = z.enum([
    "PY_BROWSER",
    "WIDGET_FOLDER",
    "WIDGET_CONTENT",
    "WIDGET_CONSOLE",
]);


const ActionId = z.enum([
    "APP_ACTION",
    "ON_LOAD",
    "LIST_DIRECTORY",
    "OPEN_PATH",
    "GET_STATE",
    "SET_STATE",
    "GET_LINK",
]);

const BaseMsg = z.object({
    sender_id: WidgetId,
    receiver_id: WidgetId,
    action: ActionId,
});

const FolderReq = BaseMsg.extend({
    path: z.string().nullable(),
    select_path: z.string().nullable(),
    depth: z.number(),
});

const OpenPathReq = BaseMsg.extend({
    open_path_type: OpenPathType.default(OpenPathType.enum.AUTO),
    path: z.string(),
});

const OpenPathRes = BaseMsg.extend({
    open_path_type: OpenPathType.default(OpenPathType.enum.AUTO),
    path: z.string(),
});

const PathItem = z.lazy(() =>
    z.object({
        is_dir: z.boolean(),
        name: z.string(),
        path: z.string(),
        ext: z.string(),
        mime: z.string(),
        mtime: z.number(),
        size: z.number(),
        tot: z.number(),
        items: z.array(PathItem),
    })
);

const FolderRes = BaseMsg.extend({
    path: z.string().nullable(),
    select_path: z.string().nullable(),
    depth: z.number(),
    page_no: z.number(),
    page_size: z.number(),
    item: PathItem,
});

const GetStateReq = BaseMsg.extend({
    key: StateKey
});

const GetStateRes = BaseMsg.extend({
    key: StateKey,
    value: z.union([ContentTemplate, GalleryType, z.string()])
});

const SetStateReq = BaseMsg.extend({
    key: StateKey,
    value: z.union([ContentTemplate, GalleryType, z.string()])
});

const SetStateRes = BaseMsg.extend({
    key: StateKey,
    value: z.union([ContentTemplate, GalleryType, z.string()])
});

const Link = z.object({
    key: z.string(),
    value: z.string(),
});

const GetLinkReq = BaseMsg.extend({
});

const GetLinkRes = BaseMsg.extend({
    items: z.array(Link),
});




class PyBrowser {
    constructor() {
        this.listener = (params) => {
            console.log(`
                <script>
                    Pb.addListener((params) => {
                        const jres = JSON.parse(params);
                        const res = BaseMsg.parse(jres);
                        window[res.action.toLowerCase()](params);
                    });
                    on_load = (params) => {
                        const jres = JSON.parse(params);
                        console.log("on_load");
                    }
                </script>
            `)
        }
    }

    getMessageHandlerName = () => {
        return this.MESSAGE_HANDLER_NAME;
    }

    onLoad = (_onLoad) => {
        this._onLoad = _onLoad;
    }

    sendMessage = (msg) => {
        // https://docs.wxpython.org/wx.html2.WebView.html#wx.html2.WebView.AddScriptMessageHandler
        window[msg.sender_id].postMessage(JSON.stringify(msg));
    }

    addListener = (listener) => {
        this.listener = listener
    }
    

}

const pyBrowser = new PyBrowser();

window.Pb = pyBrowser;
