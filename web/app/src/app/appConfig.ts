export const APP_CONFIG = {
    baseUrl: '/api',
    streamPath: `/stream`,
    movePath: `/move`,
    feedPath: `/feed`,
    setupPath: `/setup`,
    prodUrl: 'https://ostara.maneki.dev',

    get streamUrl() {
        return APP_CONFIG.baseUrl + APP_CONFIG.streamPath;
    },
};
