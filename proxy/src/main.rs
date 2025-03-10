use pingora::prelude::*;
use pingora::services::http_proxy::HttpProxyService;

#[tokio::main]
async fn main() {
    let mut server = Server::new(None).unwrap();

    let mut proxy = HttpProxyService::new();
    proxy.add_origin("http://frontend:3000").await;
    proxy.add_origin("http://backend:8080").await;

    server.add_service(proxy);
    server.run_forever().await;
}
