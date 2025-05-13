const z = Zod;

const WidgetId = z.enum([
    "PY_BROWSER",
    "WIDGET_FOLDER",
    "WIDGET_CONTENT",
    "WIDGET_CONSOLE",
]);

const BaseMsg = z.object({
    sender_id: WidgetId,
    receiver_id: WidgetId,
    action: Zod.string(),
    callback: Zod.string().nullable(),
});

const FolderReq = BaseMsg.extend({
    path: z.string().nullable(),
    is_root: z.boolean(),
});

const OpenPathReq = BaseMsg.extend({
    path: z.string(),
});

const PathItem = z.object({
    is_folder: z.boolean(),
    name: z.string(),
    path: z.string(),
    has_children: z.boolean().default(false),
    mtime: z.string(),
    size: z.number().int(),
});

const FolderRes = BaseMsg.extend({
    path: z.string().nullable(),
    is_root: z.boolean(),
    items: z.array(PathItem),
});




class PyBrowser {
    constructor() {
        this.MESSAGE_HANDLER_NAME = null;
        this.message_handler = null;
        this._onLoad = null;
        this.callbacks = {};
    }

    init = (jres) => {
        const res = BaseMsg.parse(jres);
        this.MESSAGE_HANDLER_NAME = res.receiver_id;
        this.message_handler = window[this.MESSAGE_HANDLER_NAME];
        this._onLoad();
    }


    getMessageHandlerName = () => {
        return this.MESSAGE_HANDLER_NAME;
    }

    onLoad = (_onLoad) => {
        this._onLoad = _onLoad;
    }

    sendMessage = (msg) => {
        if (this.MESSAGE_HANDLER_NAME) {
            this.message_handler.postMessage(JSON.stringify(msg));
        } else {
            console.error("https://docs.wxpython.org/wx.html2.WebView.html#wx.html2.WebView.AddScriptMessageHandler");
        }
    }


    listener = (params) => {
        const jres = JSON.parse(params);
        const res = BaseMsg.parse(jres);
        if (res.callback){
            const func = (res.callback).split('.').reduce((acc, key) => acc?.[key], window);
            if (typeof func === "function"){
                func(jres);
            } else {
                alert("Error callback: " + res.callback);
            }
        }
    }

    addCallbacks = (callbacks) => {
        this.callbacks = callbacks;
    }
    

}

const pyBrowser = new PyBrowser();

window.Pb = pyBrowser;
window.onerror = (message, source, lineno, colno, error) => {
    const err = {
        message: message,
        source: source,
        lineno: lineno,
        colno: colno,
        error: error,
    }
    alert("onerror:" + JSON.stringify(err));
    return true;
};

window.addEventListener("unhandledrejection", (event) => {
  alert("Unhandled rejection:" + event.reason);
});
