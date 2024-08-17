use std::str::FromStr;
use std::sync::{Arc, OnceLock};
use std::time::Duration;

use ahash::RandomState;
use indexmap::IndexMap;
use pyo3::exceptions;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyString};
use rquest::header::{HeaderMap, HeaderName, HeaderValue, COOKIE};
use rquest::tls::Impersonate;
use rquest::multipart;
use rquest::redirect::Policy;
use rquest::Method;
use tokio::runtime::{self, Runtime};

mod response;
use response::Response;

mod utils;
use utils::{get_encoding_from_content, get_encoding_from_headers, json_dumps, url_encode};

// Tokio global one-thread runtime
fn runtime() -> &'static Runtime {
    static RUNTIME: OnceLock<Runtime> = OnceLock::new();
    RUNTIME.get_or_init(|| {
        runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap()
    })
}

#[pyclass]
#[derive(Clone)]
pub struct PyClient {
    inner: rquest::Client,
}

#[pyclass]
/// HTTP client that can impersonate web browsers.
pub struct Client {
    client: Arc<rquest::Client>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    params: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
}

#[pymethods]
impl Client {
    /// Initializes an HTTP client that can impersonate web browsers.
    ///
    /// This function creates a new HTTP client instance that can impersonate various web browsers.
    /// It allows for customization of headers, proxy settings, timeout, impersonation type, SSL certificate verification,
    /// and HTTP version preferences.
    ///
    /// # Arguments
    ///
    /// * `auth` - A tuple containing the username and an optional password for basic authentication. Default is None.
    /// * `auth_bearer` - A string representing the bearer token for bearer token authentication. Default is None.
    /// * `params` - A map of query parameters to append to the URL. Default is None.
    /// * `headers` - An optional map of HTTP headers to send with requests. If `impersonate` is set, this will be ignored.
    /// * `cookies` - An optional map of cookies to send with requests as the `Cookie` header.
    /// * `cookie_store` - Enable a persistent cookie store. Received cookies will be preserved and included
    ///         in additional requests. Default is `true`.
    /// * `referer` - Enable or disable automatic setting of the `Referer` header. Default is `true`.
    /// * `proxy` - An optional proxy URL for HTTP requests.
    /// * `timeout` - An optional timeout for HTTP requests in seconds.
    /// * `impersonate` - An optional entity to impersonate. Supported browsers and versions include Chrome, Safari, OkHttp, and Edge.
    /// * `follow_redirects` - A boolean to enable or disable following redirects. Default is `true`.
    /// * `max_redirects` - The maximum number of redirects to follow. Default is 20. Applies if `follow_redirects` is `true`.
    /// * `verify` - An optional boolean indicating whether to verify SSL certificates. Default is `true`.
    /// * `http1` - An optional boolean indicating whether to use only HTTP/1.1. Default is `false`.
    /// * `http2` - An optional boolean indicating whether to use only HTTP/2. Default is `false`.
    ///
    /// # Example
    ///
    /// ```
    /// from primp import Client
    ///
    /// client = Client(
    ///     auth=("name", "password"),
    ///     params={"p1k": "p1v", "p2k": "p2v"},
    ///     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"},
    ///     cookies={"ck1": "cv1", "ck2": "cv2"},
    ///     cookie_store=False,
    ///     referer=False,
    ///     proxy="http://127.0.0.1:8080",
    ///     timeout=10,
    ///     impersonate="chrome_123",
    ///     follow_redirects=True,
    ///     max_redirects=1,
    ///     verify=False,
    ///     http1=True,
    ///     http2=False,
    /// )
    /// ```
    #[new]
    #[pyo3(signature = (auth=None, auth_bearer=None, params=None, headers=None, cookies=None, cookie_store=None, referer=None,
        proxy=None, timeout=None, impersonate=None, follow_redirects=None, max_redirects=None, verify=None, http1=None, http2=None))]
    fn new(
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        cookie_store: Option<bool>,
        referer: Option<bool>,
        proxy: Option<&str>,
        timeout: Option<f64>,
        impersonate: Option<&str>,
        follow_redirects: Option<bool>,
        max_redirects: Option<usize>,
        verify: Option<bool>,
        http1: Option<bool>,
        http2: Option<bool>,
    ) -> PyResult<Self> {
        if auth.is_some() && auth_bearer.is_some() {
            return Err(PyErr::new::<exceptions::PyValueError, _>(
                "Cannot provide both auth and auth_bearer",
            ));
        }

        // Client builder
        let mut client_builder = rquest::Client::builder()
            .enable_ech_grease()
            .permute_extensions();

        // Impersonate
        if let Some(impersonation_type) = impersonate {
            let impersonation = Impersonate::from_str(impersonation_type).map_err(|_| {
                PyErr::new::<exceptions::PyValueError, _>("Invalid impersonate param")
            })?;
            client_builder = client_builder.impersonate(impersonation);
        }

        // Headers
        if let Some(headers) = headers {
            let mut headers_new = HeaderMap::with_capacity(headers.len());
            for (key, value) in headers {
                headers_new.insert(
                    HeaderName::from_bytes(key.as_bytes()).map_err(|_| {
                        PyErr::new::<exceptions::PyValueError, _>("Invalid header name")
                    })?,
                    HeaderValue::from_str(&value).map_err(|_| {
                        PyErr::new::<exceptions::PyValueError, _>("Invalid header value")
                    })?,
                );
            }
            client_builder = client_builder.default_headers(headers_new);
        }

        // Cookie_store
        if cookie_store.unwrap_or(true) {
            client_builder = client_builder.cookie_store(true);
        }

        // Referer
        if referer.unwrap_or(true) {
            client_builder = client_builder.referer(true);
        }

        // Proxy
        if let Some(proxy_url) = proxy {
            let proxy = rquest::Proxy::all(proxy_url)
                .map_err(|_| PyErr::new::<exceptions::PyValueError, _>("Invalid proxy URL"))?;
            client_builder = client_builder.proxy(proxy);
        }

        // Timeout
        if let Some(seconds) = timeout {
            client_builder = client_builder.timeout(Duration::from_secs_f64(seconds));
        }

        // Redirects
        let max_redirects = max_redirects.unwrap_or(20); // Default to 20 if not provided
        if follow_redirects.unwrap_or(true) {
            client_builder = client_builder.redirect(Policy::limited(max_redirects));
        } else {
            client_builder = client_builder.redirect(Policy::none());
        }

        // Verify
        let verify = verify.unwrap_or(true);
        if !verify {
            client_builder = client_builder.danger_accept_invalid_certs(true);
        }

        // Http version: http1 || http2
        match (http1, http2) {
            (Some(true), Some(true)) => {
                return Err(PyErr::new::<exceptions::PyValueError, _>(
                    "Both http1 and http2 cannot be true",
                ));
            }
            (Some(true), _) => client_builder = client_builder.http1_only(),
            (_, Some(true)) => client_builder = client_builder.http2_only(),
            _ => (),
        }

        let client =
            Arc::new(client_builder.build().map_err(|_| {
                PyErr::new::<exceptions::PyValueError, _>("Failed to build client")
            })?);

        Ok(Client {
            client,
            auth,
            auth_bearer,
            params,
            cookies,
        })
    }

    /// Constructs an HTTP request with the given method, URL, and optionally sets a timeout, headers, and query parameters.
    /// Sends the request and returns a `Response` object containing the server's response.
    ///
    /// # Arguments
    ///
    /// * `method` - The HTTP method to use (e.g., "GET", "POST").
    /// * `url` - The URL to which the request will be made.
    /// * `params` - A map of query parameters to append to the URL. Default is None.
    /// * `headers` - A map of HTTP headers to send with the request. Default is None.
    /// * `cookies` - An optional map of cookies to send with requests as the `Cookie` header.
    /// * `content` - The content to send in the request body as bytes. Default is None.
    /// * `data` - The form data to send in the request body. Default is None.
    /// * `json` -  A JSON serializable object to send in the request body. Default is None.
    /// * `files` - A map of file fields to file contents as bytes to be sent as multipart/form-data. Default is None.
    /// * `auth` - A tuple containing the username and an optional password for basic authentication. Default is None.
    /// * `auth_bearer` - A string representing the bearer token for bearer token authentication. Default is None.
    /// * `timeout` - The timeout for the request in seconds. Default is 30.
    ///
    /// # Returns
    ///
    /// * `Response` - A response object containing the server's response to the request.
    ///
    /// # Errors
    ///
    /// * `PyException` - If there is an error making the request.
    #[pyo3(signature = (method, url, params=None, headers=None, cookies=None, content=None,
        data=None, json=None, files=None, auth=None, auth_bearer=None, timeout=None))]
    fn request(
        &self,
        py: Python,
        method: &str,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyDict>>,
        json: Option<&Bound<'_, PyDict>>,
        files: Option<IndexMap<String, Vec<u8>>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        let client = Arc::clone(&self.client);
        let auth = auth.or(self.auth.clone());
        let auth_bearer = auth_bearer.or(self.auth_bearer.clone());
        let params = params.or(self.params.clone());
        let cookies = cookies.or(self.cookies.clone());
        // Converts 'data' (if any) into a URL-encoded string for sending the data as `application/x-www-form-urlencoded` content type.
        let data_str = data
            .map(|data_pydict| url_encode(py, Some(data_pydict)).ok())
            .unwrap_or_else(|| None);
        // Converts 'json' (if any) into a JSON string for sending the data as `application/json` content type.
        let json_str = json
            .map(|json_pydict| json_dumps(py, Some(json_pydict)).ok())
            .unwrap_or_else(|| None);

        let future = async move {
            // Check if method is POST || PUT || PATCH
            let is_post_put_patch = method == "POST" || method == "PUT" || method == "PATCH";

            // Method
            let method = match method {
                "GET" => Ok(Method::GET),
                "POST" => Ok(Method::POST),
                "HEAD" => Ok(Method::HEAD),
                "OPTIONS" => Ok(Method::OPTIONS),
                "PUT" => Ok(Method::PUT),
                "PATCH" => Ok(Method::PATCH),
                "DELETE" => Ok(Method::DELETE),
                &_ => Err(PyErr::new::<exceptions::PyException, _>(
                    "Unrecognized HTTP method",
                )),
            }?;

            // Create request builder
            let mut request_builder = client.request(method, url);

            // Params
            if let Some(params) = params {
                request_builder = request_builder.query(&params);
            }

            // Headers
            if let Some(headers) = headers {
                let mut headers_new = HeaderMap::with_capacity(headers.len());
                for (key, value) in headers {
                    headers_new.insert(
                        HeaderName::from_bytes(key.as_bytes()).map_err(|_| {
                            PyErr::new::<exceptions::PyValueError, _>("Invalid header name")
                        })?,
                        HeaderValue::from_str(&value).map_err(|_| {
                            PyErr::new::<exceptions::PyValueError, _>("Invalid header value")
                        })?,
                    );
                }
                request_builder = request_builder.headers(headers_new);
            }

            // Cookies
            if let Some(cookies) = cookies {
                let cookies_str = cookies
                    .iter()
                    .map(|(k, v)| format!("{}={}", k, v))
                    .collect::<Vec<String>>()
                    .join("; ");
                request_builder =
                    request_builder.header(COOKIE, HeaderValue::from_str(&cookies_str).unwrap());
            }

            // Only if method POST || PUT || PATCH
            if is_post_put_patch {
                // Content
                if let Some(content) = content {
                    request_builder = request_builder.body(content);
                }
                // Data
                if let Some(url_encoded_data) = data_str {
                    request_builder = request_builder
                        .header("Content-Type", "application/x-www-form-urlencoded")
                        .body(url_encoded_data);
                }
                // Json
                if let Some(json_str) = json_str {
                    request_builder = request_builder
                        .header("Content-Type", "application/json")
                        .body(json_str);
                }
                // Files
                if let Some(files) = files {
                    let mut form = multipart::Form::new();
                    for (file_name, file_content) in files {
                        let part =
                            multipart::Part::bytes(file_content).file_name(file_name.clone());
                        form = form.part(file_name, part);
                    }
                    request_builder = request_builder.multipart(form);
                }
            }

            // Auth
            match (auth, auth_bearer) {
                (Some((username, password)), None) => {
                    request_builder = request_builder.basic_auth(username, password.as_deref());
                }
                (None, Some(token)) => {
                    request_builder = request_builder.bearer_auth(token);
                }
                (Some(_), Some(_)) => {
                    return Err(PyErr::new::<exceptions::PyValueError, _>(
                        "Cannot provide both auth and auth_bearer",
                    ));
                }
                _ => {} // No authentication provided
            }

            // Timeout
            if let Some(seconds) = timeout {
                request_builder = request_builder.timeout(Duration::from_secs_f64(seconds));
            }

            // Send the request and await the response
            let resp = request_builder.send().await.map_err(|e| {
                PyErr::new::<exceptions::PyException, _>(format!("Error in request: {}", e))
            })?;

            // Response items
            let cookies: IndexMap<String, String, RandomState> = resp
                .cookies()
                .map(|cookie| (cookie.name().to_string(), cookie.value().to_string()))
                .collect();
            let headers: IndexMap<String, String, RandomState> = resp
                .headers()
                .iter()
                .map(|(k, v)| (k.as_str().to_string(), v.to_str().unwrap_or("").to_string()))
                .collect();
            let status_code = resp.status().as_u16();
            let url = resp.url().to_string();
            let buf = resp.bytes().await.map_err(|e| {
                PyErr::new::<exceptions::PyException, _>(format!(
                    "Error reading response bytes: {}",
                    e
                ))
            })?;
            let encoding = get_encoding_from_headers(&headers)
                .or_else(|| get_encoding_from_content(&buf))
                .unwrap_or_else(|| "UTF-8".to_string());
            Ok((buf, cookies, encoding, headers, status_code, url))
        };

        // Execute an async future, releasing the Python GIL for concurrency.
        // Use Tokio global runtime to block on the future.
        let result = py.allow_threads(|| runtime().block_on(future));
        let (f_buf, f_cookies, f_encoding, f_headers, f_status_code, f_url) = match result {
            Ok(value) => value,
            Err(e) => return Err(e),
        };

        // Response items
        let cookies_dict = PyDict::new_bound(py);
        for (key, value) in f_cookies {
            cookies_dict.set_item(key, value)?;
        }
        let cookies = cookies_dict.unbind();
        let encoding = PyString::new_bound(py, f_encoding.as_str()).unbind();
        let headers_dict = PyDict::new_bound(py);
        for (key, value) in f_headers {
            headers_dict.set_item(key, value)?;
        }
        let headers = headers_dict.unbind();
        let status_code = f_status_code.into_py(py);
        let url = PyString::new_bound(py, &f_url).unbind();
        let content = PyBytes::new_bound(py, &f_buf).unbind();

        Ok(Response {
            content,
            cookies,
            encoding,
            headers,
            status_code,
            url,
        })
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None, timeout=None))]
    fn get(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "GET",
            url,
            params,
            headers,
            cookies,
            None,
            None,
            None,
            None,
            auth,
            auth_bearer,
            timeout,
        )
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None, timeout=None))]
    fn head(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "HEAD",
            url,
            params,
            headers,
            cookies,
            None,
            None,
            None,
            None,
            auth,
            auth_bearer,
            timeout,
        )
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None, timeout=None))]
    fn options(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "OPTIONS",
            url,
            params,
            headers,
            cookies,
            None,
            None,
            None,
            None,
            auth,
            auth_bearer,
            timeout,
        )
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None, timeout=None))]
    fn delete(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "DELETE",
            url,
            params,
            headers,
            cookies,
            None,
            None,
            None,
            None,
            auth,
            auth_bearer,
            timeout,
        )
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, content=None, data=None,
        json=None, files=None, auth=None, auth_bearer=None, timeout=None))]
    fn post(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyDict>>,
        json: Option<&Bound<'_, PyDict>>,
        files: Option<IndexMap<String, Vec<u8>>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "POST",
            url,
            params,
            headers,
            cookies,
            content,
            data,
            json,
            files,
            auth,
            auth_bearer,
            timeout,
        )
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, content=None, data=None,
        json=None, files=None, auth=None, auth_bearer=None, timeout=None))]
    fn put(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyDict>>,
        json: Option<&Bound<'_, PyDict>>,
        files: Option<IndexMap<String, Vec<u8>>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "PUT",
            url,
            params,
            headers,
            cookies,
            content,
            data,
            json,
            files,
            auth,
            auth_bearer,
            timeout,
        )
    }

    #[pyo3(signature = (url, params=None, headers=None, cookies=None, content=None, data=None,
        json=None, files=None, auth=None, auth_bearer=None, timeout=None))]
    fn patch(
        &self,
        py: Python,
        url: &str,
        params: Option<IndexMap<String, String, RandomState>>,
        headers: Option<IndexMap<String, String, RandomState>>,
        cookies: Option<IndexMap<String, String, RandomState>>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyDict>>,
        json: Option<&Bound<'_, PyDict>>,
        files: Option<IndexMap<String, Vec<u8>>>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Response> {
        self.request(
            py,
            "PATCH",
            url,
            params,
            headers,
            cookies,
            content,
            data,
            json,
            files,
            auth,
            auth_bearer,
            timeout,
        )
    }
}

/// Convenience functions that use a default Client instance under the hood
#[pyfunction]
#[pyo3(signature = (method, url, params=None, headers=None, cookies=None, content=None, data=None,
    json=None, files=None, auth=None, auth_bearer=None, timeout=None, impersonate=None, verify=None))]
fn request(
    py: Python,
    method: &str,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    content: Option<Vec<u8>>,
    data: Option<&Bound<'_, PyDict>>,
    json: Option<&Bound<'_, PyDict>>,
    files: Option<IndexMap<String, Vec<u8>>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.request(
        py,
        method,
        url,
        params,
        headers,
        cookies,
        content,
        data,
        json,
        files,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None,
    timeout=None, impersonate=None, verify=None))]
fn get(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.get(
        py,
        url,
        params,
        headers,
        cookies,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None,
    timeout=None, impersonate=None, verify=None))]
fn head(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.head(
        py,
        url,
        params,
        headers,
        cookies,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None,
    timeout=None, impersonate=None, verify=None))]
fn options(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.options(
        py,
        url,
        params,
        headers,
        cookies,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, auth=None, auth_bearer=None,
    timeout=None, impersonate=None, verify=None))]
fn delete(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.delete(
        py,
        url,
        params,
        headers,
        cookies,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, content=None, data=None,
    json=None, files=None, auth=None, auth_bearer=None, timeout=None, impersonate=None, verify=None))]
fn post(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    content: Option<Vec<u8>>,
    data: Option<&Bound<'_, PyDict>>,
    json: Option<&Bound<'_, PyDict>>,
    files: Option<IndexMap<String, Vec<u8>>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.post(
        py,
        url,
        params,
        headers,
        cookies,
        content,
        data,
        json,
        files,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, content=None, data=None,
    json=None, files=None, auth=None, auth_bearer=None, timeout=None, impersonate=None, verify=None))]
fn put(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    content: Option<Vec<u8>>,
    data: Option<&Bound<'_, PyDict>>,
    json: Option<&Bound<'_, PyDict>>,
    files: Option<IndexMap<String, Vec<u8>>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.put(
        py,
        url,
        params,
        headers,
        cookies,
        content,
        data,
        json,
        files,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pyfunction]
#[pyo3(signature = (url, params=None, headers=None, cookies=None, content=None, data=None,
    json=None, files=None, auth=None, auth_bearer=None, timeout=None, impersonate=None, verify=None))]
fn patch(
    py: Python,
    url: &str,
    params: Option<IndexMap<String, String, RandomState>>,
    headers: Option<IndexMap<String, String, RandomState>>,
    cookies: Option<IndexMap<String, String, RandomState>>,
    content: Option<Vec<u8>>,
    data: Option<&Bound<'_, PyDict>>,
    json: Option<&Bound<'_, PyDict>>,
    files: Option<IndexMap<String, Vec<u8>>>,
    auth: Option<(String, Option<String>)>,
    auth_bearer: Option<String>,
    timeout: Option<f64>,
    impersonate: Option<&str>,
    verify: Option<bool>,
) -> PyResult<Response> {
    let client = Client::new(
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        impersonate,
        None,
        None,
        verify,
        None,
        None,
    )?;
    client.patch(
        py,
        url,
        params,
        headers,
        cookies,
        content,
        data,
        json,
        files,
        auth,
        auth_bearer,
        timeout,
    )
}

#[pymodule]
fn primp(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Client>()?;
    m.add_function(wrap_pyfunction!(request, m)?)?;
    m.add_function(wrap_pyfunction!(get, m)?)?;
    m.add_function(wrap_pyfunction!(head, m)?)?;
    m.add_function(wrap_pyfunction!(options, m)?)?;
    m.add_function(wrap_pyfunction!(delete, m)?)?;
    m.add_function(wrap_pyfunction!(post, m)?)?;
    m.add_function(wrap_pyfunction!(patch, m)?)?;
    m.add_function(wrap_pyfunction!(put, m)?)?;
    Ok(())
}