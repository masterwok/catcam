const baseUrl = "http://192.168.1.86:8000/api";

export const APP_CONFIG = {
    baseUrl: baseUrl,
    streamPath: `/stream`,
    movePath: `/move`,

    get streamUrl() {
        return APP_CONFIG.baseUrl + APP_CONFIG.streamPath;
    },
};