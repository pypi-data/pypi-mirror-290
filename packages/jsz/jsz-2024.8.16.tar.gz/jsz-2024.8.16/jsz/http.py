import httpx
import asyncio
from rich import print


__all__ = [
    "async_fetch",
    "fetch",
    "httpx",
]


async def _async_fetch(
    url: str,
    method: str = "GET",
    *,
    params: dict[str] | None = None,
    content=None,
    data=None,
    json=None,
    headers=None,
    cookies=None,
    files=None,
    auth=None,
    proxy=None,
    proxies=None,
    mounts=None,
    timeout=None,
    follow_redirects: bool = True,
    verify: bool = True,
    cert=None,
    trust_env: bool = True,
    http1=True,
    http2=False,
    default_encoding="utf-8",
):
    """
    ## 发送异步请求（基于 httpx.AsyncClient）

    url: 请求地址
    method: 请求方法, 默认为 GET, 支持 GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE, CONNECT
    params: 查询参数
    content: 请求内容
    data: 请求内容
    json: 请求内容
    headers: 请求头
    cookies: 请求 Cookie
    files: 文件
    auth: 认证
    proxy: 代理
    proxies: 代理
    mounts: 挂载
    timeout: 超时
    follow_redirects: 是否跟随重定向
    verify: 是否验证 SSL 证书
    cert: 证书
    trust_env: 是否信任环境变量
    http1: 是否使用 HTTP/1.1
    http2: 是否使用 HTTP/2
    default_encoding: 默认编码
    """
    async with httpx.AsyncClient(
        verify=verify,
        cert=cert,
        http1=http1,
        http2=http2,
        proxy=proxy,
        proxies=proxies,
        mounts=mounts,
        trust_env=trust_env,
        default_encoding=default_encoding,
    ) as client:
        return await client.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
        )


async def async_fetch(
    url: str,
    method: str = "GET",
    *,
    params: dict[str] | None = None,
    content=None,
    data=None,
    json=None,
    headers=None,
    cookies=None,
    files=None,
    auth=None,
    proxy=None,
    proxies=None,
    mounts=None,
    timeout=None,
    follow_redirects: bool = True,
    verify: bool = True,
    cert=None,
    trust_env: bool = True,
    http1=True,
    http2=False,
    default_encoding="utf-8",
    retry: int = 1,
):
    """
    ## 发送异步请求（基于 httpx.AsyncClient）

    url: 请求地址
    method: 请求方法, 默认为 GET, 支持 GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE, CONNECT
    params: 查询参数
    content: 请求内容
    data: 请求内容
    json: 请求内容
    headers: 请求头
    cookies: 请求 Cookie
    files: 文件
    auth: 认证
    proxy: 代理
    proxies: 代理
    mounts: 挂载
    timeout: 超时
    follow_redirects: 是否跟随重定向
    verify: 是否验证 SSL 证书
    cert: 证书
    trust_env: 是否信任环境变量
    http1: 是否使用 HTTP/1.1
    http2: 是否使用 HTTP/2
    default_encoding: 默认编码
    retry: 重试次数
    """
    for _ in range(retry):
        try:
            response = await _async_fetch(
                url=url,
                method=method,
                params=params,
                content=content,
                data=data,
                json=json,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                proxy=proxy,
                proxies=proxies,
                mounts=mounts,
                timeout=timeout,
                follow_redirects=follow_redirects,
                verify=verify,
                cert=cert,
                trust_env=trust_env,
                http1=http1,
                http2=http2,
                default_encoding=default_encoding,
            )
            return response
        except Exception as e:
            print(f"请求失败: {e!r}")


def fetch(
    url: str,
    method: str = "GET",
    *,
    params: dict[str] | None = None,
    content=None,
    data=None,
    json=None,
    headers=None,
    cookies=None,
    files=None,
    auth=None,
    proxy=None,
    proxies=None,
    mounts=None,
    timeout=None,
    follow_redirects: bool = True,
    verify: bool = True,
    cert=None,
    trust_env: bool = True,
    http1=True,
    http2=False,
    default_encoding="utf-8",
    retry: int = 1,
):
    """
    发送同步请求（基于 httpx.AsyncClient）

    url: 请求地址
    method: 请求方法, 默认为 GET, 支持 GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE, CONNECT
    params: 查询参数
    content: 请求内容
    data: 请求内容
    json: 请求内容
    headers: 请求头
    cookies: 请求 Cookie
    files: 文件
    auth: 认证
    proxy: 代理
    proxies: 代理
    mounts: 挂载
    timeout: 超时
    follow_redirects: 是否跟随重定向
    verify: 是否验证 SSL 证书
    cert: 证书
    trust_env: 是否信任环境变量
    http1: 是否使用 HTTP/1.1
    http2: 是否使用 HTTP/2
    default_encoding: 默认编码
    retry: 重试次数
    """
    response = asyncio.run(
        async_fetch(
            url,
            method,
            params=params,
            content=content,
            data=data,
            json=json,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            proxy=proxy,
            proxies=proxies,
            mounts=mounts,
            timeout=timeout,
            follow_redirects=follow_redirects,
            verify=verify,
            cert=cert,
            trust_env=trust_env,
            http1=http1,
            http2=http2,
            default_encoding=default_encoding,
            retry=retry,
        )
    )
    return response
