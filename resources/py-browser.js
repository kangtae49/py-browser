let PY_WIDGET_ID = null;
function set_widget_id(widget_id) {
    PY_WIDGET_ID = widget_id;
}

function post_message(data) {
    if (PY_WIDGET_ID) {
        data["widget_id"] = PY_WIDGET_ID;
        window[PY_WIDGET_ID].postMessage(JSON.stringify(data));
    } else {
        console.error("Widget ID is not set. Please call get_widget_id() first.");
    }
}