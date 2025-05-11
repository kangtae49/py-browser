const WidgetId = Zod.enum([
    "WIDGET_FOLDER",
    "WIDGET_CONTENT",
    "WIDGET_CONSOLE",
]);

const BaseMsg = Zod.object({
    sender_id: WidgetId,
    receiver_id: WidgetId,
    action: Zod.string(),
    callback: Zod.string().nullable(),
});

const FolderReq = BaseMsg.extend({
    path: Zod.string().nullable(),
});

const PathItem = Zod.object({
    is_folder: Zod.boolean(),
    name: Zod.string(),
    path: Zod.string(),
});

const FolderListRes = BaseMsg.extend({
    path: Zod.string().nullable(),
    items: Zod.array(PathItem),
});

const ConsoleReq = BaseMsg.extend({
    msg: Zod.string(),
});


class PyBrowser {
    constructor() {
        this.MESSAGE_HANDLER_NAME = null;
        this.message_handler = null;
        this.listener = null;
    }

    addScriptMessageHandler(name) {
        this.MESSAGE_HANDLER_NAME = name;
        this.message_handler = window[name];
        let pb = this;
        window.console = {
            log: function (msg) {
                const req = ConsoleReq.parse({
                    sender_id: pb.MESSAGE_HANDLER_NAME,
                    receiver_id: "WIDGET_CONSOLE",
                    action: "console_log",
                    callback: "Pb.appendConsoleLog",
                    msg: String(msg)
                });
                pb.sendMessage(req);
            },
        };
        this.listener();
    }


    getMessageHandlerName(){
        return this.MESSAGE_HANDLER_NAME;
    }

    onLoad(listener) {
        this.listener = listener;
    }

    sendMessage (msg) {
        if (this.MESSAGE_HANDLER_NAME) {
            this.message_handler.postMessage(JSON.stringify(msg));
        } else {
            console.error("https://docs.wxpython.org/wx.html2.WebView.html#wx.html2.WebView.AddScriptMessageHandler");
        }
    }

    appendConsoleLog(msg) {
        let res = ConsoleReq.safeParse(JSON.parse(msg));
        append_console_log(res.data);
    }
    

}

const pyBrowser = new PyBrowser();

const Pb = {
    addScriptMessageHandler: pyBrowser.addScriptMessageHandler,
    sendMessage: pyBrowser.sendMessage,
    onLoad: pyBrowser.onLoad,
    getMessageHandlerName: pyBrowser.getMessageHandlerName,
    appendConsoleLog: pyBrowser.appendConsoleLog,
};

window.Pb = Pb;

