"use strict";
(self["webpackChunk_minrk_jupyter_keepalive"] = self["webpackChunk_minrk_jupyter_keepalive"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__);






// import "./index.css";
/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function keepAliveRequest(endPoint = "", init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(settings.baseUrl, "ext-keepalive", endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.NetworkError(error);
    }
    const responseJSON = await response.text();
    if (responseJSON.length == 0) {
        return;
    }
    const data = JSON.parse(responseJSON);
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.ResponseError(response, data.message);
    }
    return data;
}
const DAY_SECONDS = 24 * 60 * 60;
const hmsPattern = /^(?:(?<days>\d+):(?=\d+:))?(?:(?<hours>\d+):)?(?<seconds>\d+)$/;
const abbrevPattern = /^(?:(?<days>\d+)d)?(?:(?<hours>\d+)h)?(?:(?<minutes>\d+)m)?(?:(?<seconds>\d+)s?)?$/;
const multipliers = {
    minutes: 60,
    hours: 60 * 60,
    days: 24 * 60 * 60,
    seconds: 1,
};
function parseTime(ts) {
    let seconds = 0;
    let match = hmsPattern.exec(ts);
    if (!match) {
        match = abbrevPattern.exec(ts);
    }
    if (!match) {
        throw Error(`time string '${ts}' as a time. Expected e.g. '1:30' or '120m'`);
    }
    let part;
    for (part in multipliers) {
        if (match.groups[part] !== undefined) {
            seconds += multipliers[part] * parseInt(match.groups[part]);
        }
    }
    return seconds;
}
function formatSeconds(seconds) {
    console.log("formatting", seconds);
    if (seconds < 60) {
        return `${seconds}s`;
    }
    else if (seconds < 120) {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}m${s}s`;
    }
    else if (seconds < 3600) {
        const m = Math.floor(seconds / 60);
        return `${m}m`;
    }
    else {
        const h = Math.round(seconds / 3600);
        return `${h}h`;
    }
}
class KeepAliveExtension {
    constructor() {
        this.remainingSignal = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this.remainingSignal.connect(this.scheduleUpdate);
        this.remaining = 0;
    }
    scheduleUpdate(sender, remaining) {
        // keep widgets updated at an appropriate in
        sender.remaining = remaining;
        if (!remaining) {
            return;
        }
        let timeout = 0;
        if (remaining < 60) {
            timeout = 1;
        }
        else if (remaining < 120) {
            // every 2 seconds if we're within 2 minutes
            timeout = 2;
        }
        else if (remaining < 60) {
            // every minute if we're within an hour
            timeout = 60;
        }
        else {
            // at least every 5 minutes
            timeout = 300;
        }
        setTimeout(() => {
            sender.getRemaining();
        }, timeout * 1000);
    }
    setupStatusBar(statusBar) {
        const keepAliveStatusWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget();
        this.remainingSignal.connect((sender, remaining) => {
            if (remaining) {
                const remaining_text = formatSeconds(remaining);
                keepAliveStatusWidget.node.textContent = "";
                const span = document.createElement("span");
                span.textContent = `Keepalive: ${remaining_text}`;
                // TODO: import css?
                // css is copied from TextItem, but using TextItem is incredibly complicated apparently
                span.style.cssText =
                    "line-height: 24px; color: var(--jp-ui-font-color1); font-family: var(--jp-ui-font-family); font-size: var(--jp-ui-font-size1);";
                keepAliveStatusWidget.node.title = `Jupyter Server will not appear idle idle for ${remaining_text}`;
                keepAliveStatusWidget.node.appendChild(span);
            }
            else {
                // Don't show anything when inactive
                keepAliveStatusWidget.node.textContent = "";
            }
        });
        statusBar.registerStatusItem("keepalive", {
            align: "left",
            item: keepAliveStatusWidget,
            isActive: () => true // Always actice
        });
    }
    async start(seconds = DAY_SECONDS) {
        const keepAliveData = await keepAliveRequest("", {
            method: "POST",
            body: JSON.stringify({ seconds: seconds }),
        });
        this.remainingSignal.emit(keepAliveData.remaining);
    }
    async stop() {
        await keepAliveRequest("", { method: "DELETE" });
        this.remainingSignal.emit(0);
    }
    async getRemaining() {
        const keepAliveData = await keepAliveRequest("");
        this.remainingSignal.emit(keepAliveData.remaining);
        return keepAliveData.remaining;
    }
    async startDialog() {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
            title: "Keep Jupyter server alive",
            body: new KeepAliveDialogBody(),
            focusNodeSelector: "input",
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: "Keep alive" }),
            ],
        });
        if (!result.value) {
            return;
        }
        const t = parseTime(result.value);
        await this.start(t);
    }
}
class KeepAliveDialogBody extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Construct a new keep alive dialog.
     */
    constructor() {
        const body = document.createElement("div");
        const description = document.createElement("p");
        description.textContent =
            "Keep Jupyter Server from shutting down due to idle culling for a period of time. \
      Use abbreviated notation such as '2d' for two days, \
      '3h45m' for 3 hours and 45 minutes, \
      or seconds as an integer (900).";
        const label = document.createElement("label");
        label.textContent = "Duration";
        const input = document.createElement("input");
        input.placeholder = "24h";
        input.value = "24h";
        body.appendChild(description);
        body.appendChild(label);
        body.appendChild(input);
        super({ node: body });
    }
    /**
     * Get the input text node.
     */
    get inputNode() {
        return this.node.getElementsByTagName("input")[0];
    }
    /**
     * Get the value of the widget.
     */
    getValue() {
        return this.inputNode.value;
    }
}
/**
 * Initialization data for the extension.
 */
const extension = {
    id: "jupyter-keepalive",
    autoStart: true,
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__.IStatusBar],
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette],
    activate: async (app, palette, statusBar) => {
        console.log("JupyterLab extension keepalive is activated!");
        const keepAlive = new KeepAliveExtension();
        if (statusBar) {
            keepAlive.setupStatusBar(statusBar);
        }
        const { commands } = app;
        const category = "Keepalive";
        commands.addCommand("keepalive:start", {
            label: "Keep server alive while idle (24h)",
            caption: "Registers activity so idle cullers don't shut this server down, for `seconds`.",
            execute: (args) => {
                let seconds;
                if (typeof args.seconds === "number") {
                    seconds = args.seconds;
                }
                else if (typeof args.seconds === "string") {
                    seconds = parseTime(args.seconds);
                }
                else {
                    seconds = DAY_SECONDS;
                }
                keepAlive.start(seconds);
            },
        });
        commands.addCommand("keepalive:start-dialog", {
            label: "Keep server alive while idle (dialog)",
            caption: "Registers activity so idle cullers don't shut this server down.",
            execute: () => {
                keepAlive.startDialog();
            },
        });
        commands.addCommand("keepalive:stop", {
            label: "Stop keeping server alive",
            caption: "Stop the keepalive spinner",
            execute: () => {
                keepAlive.stop();
            },
        });
        commands.addCommand("keepalive:check", {
            label: "Check keepalive status",
            caption: "Check the remaining time on the keepalive timer",
            execute: () => {
                keepAlive.getRemaining();
                // todo: display it somehow
            },
        });
        for (const command of [
            "keepalive:start",
            "keepalive:start-dialog",
            "keepalive:stop",
            "keepalive:check",
        ]) {
            palette.addItem({ command: command, category: category });
        }
        await keepAlive.getRemaining();
        return keepAlive;
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.969879db0425465fe6ea.js.map