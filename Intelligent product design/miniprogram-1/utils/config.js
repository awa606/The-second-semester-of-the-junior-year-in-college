/**
 * 育儿助手接口地址配置说明：
 *
 * 1) 开发者工具本地调试（默认）：
 *    - 可使用 127.0.0.1 / localhost，例如 http://127.0.0.1:8000
 *    - 在微信开发者工具中，需要勾选“开发环境不校验请求合法域名、TLS版本及HTTPS证书”。
 *
 * 2) 真机预览 / 真机调试：
 *    - 不能使用 127.0.0.1 或 localhost（会指向手机自身）。
 *    - 需改为电脑的局域网 IPv4 地址，并确保后端监听 0.0.0.0。
 *    - 例如：http://192.168.x.x:8000（请替换为你电脑实际 IPv4）。
 */
const API_BASE_URL_LOCAL = 'http://127.0.0.1:8000';
const API_BASE_URL_LAN = 'http://192.168.x.x:8000'; // 真机调试时替换为电脑实际 IPv4

// 默认保持本地开发地址，不切换为公网地址。
const API_BASE_URL = API_BASE_URL_LOCAL;

module.exports = {
  API_BASE_URL,
  API_BASE_URL_LOCAL,
  API_BASE_URL_LAN
};
