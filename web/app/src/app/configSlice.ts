export const APP_CONFIG = {
    baseUrl: '/api',
    streamPath: `/stream`,
    movePath: `/move`,

    get streamUrl() {
        return APP_CONFIG.baseUrl + APP_CONFIG.streamPath;
    },
};
