'use strict';

var BagouWebSocket = function(url, settings, protocols) {
    var ws;
    if (protocols)
        ws = window['MozWebSocket'] ? new MozWebSocket(url, protocols) : window['WebSocket'] ? new WebSocket(url, protocols) : null;
    else
        ws = window['MozWebSocket'] ? new MozWebSocket(url) : window['WebSocket'] ? new WebSocket(url) : null;

    var defaultSettings = {
        open: function(){},
        close: function(){},
        message: function(){},
        options: {},
        events: {}
    };
    // Added extend method to settings Object
    function extend() {
        for(var i=1; i<arguments.length; i++)
            for(var key in arguments[i])
                if(arguments[i].hasOwnProperty(key))
                    arguments[0][key] = arguments[i][key];
        return arguments[0];
    }
    function getCookies() {
        var cookies = {};
        var all = document.cookie;
        if (all === "")
            return cookies;
        var list = all.split("; ");
        for(var i = 0; i < list.length; i++) {
            var cookie = list[i];
            var p = cookie.indexOf("=");
            var name = cookie.substring(0,p);
            var value = cookie.substring(p+1);
            value = decodeURIComponent(value);
            cookies[name] = value;
        }
        return cookies;
    }

    if (settings.events.callback) {
        console.warn('callback event in reserved, declaration dropped.');
        delete(settings.events.callback);
    }

    settings = extend(defaultSettings, settings);
    settings.events.callback = function(msg) {
        ws.oncallback(msg);
    }

    ws.settings = settings;
    ws.authenticated = true;
    var callbacks = {};

    if (ws) {
        // Events
        ws.onopen = settings.open;
        ws.onclose = settings.close;
        ws.onmessage = settings.message;
        ws.onmessage = function(e) {
            var m = JSON.parse(e.data);
            var h = settings.events[m.event];
            if (h)
                h.call(this, m);
        };
        ws.oncallback = function(e) {
            var callback = ws._getCallback(e.callbackId);
            if (callback) callback(e)
        };
        // Internals
        ws._getCallback = function(callbackId) {
            return callbacks[callbackId];
        }
        ws._setCallback = function(message, callback) {
            var callbackId = uuid.v1();
            callbacks[callbackId] = callback;
            message.callbackId = callbackId;
            return message;
        };
        window.onunload = function() {
            ws.onclose();
            ws = null;
        };
        // Methods
        ws._send = ws.send;
        ws.emit = function(event, data, callback) {
            var m = extend({event: event}, extend({}, settings.open, {event: event}));
            m.data = data;
            if (callback)
                m = ws._setCallback(m, callback);
            return this._send(JSON.stringify(m));
        };
        ws.auth = function(callback) {
            ws.emit('authenticate', {}, function(message) {
                if (message.data.success)
                    ws.authenticated = true;
                    ws.user = message.data.user;
                if (callback) callback(message);
            });
        };
        ws.subscribe = function(channel, callback) {
            ws.emit('subscribe', {'channel': channel}, callback);
        };
        ws.unsubscribe = function(channel, callback) {
            ws.emit('unsubscribe', {'channel': channel}, callback);
        };
        ws.store = function(key, value, callback) {
            var store = {};
            store[key] = value;
            ws.emit('store', store, callback);
        };
    }
    return ws;
};
