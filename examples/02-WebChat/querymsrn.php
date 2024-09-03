<?php
/* PHP script that talks with the MSR Necromancer server via BSD sockets
 * Ondrej Chvala  <ochvala@utexas.edu>
 * https://www.php.net/manual/en/ref.sockets.php */

if (!extension_loaded('sockets')) {
    die('The sockets extension is not loaded.');
}

$socket = socket_create(AF_INET, SOCK_STREAM, 0);
if (!$socket) {
    die('Unable to create AF_UNIX socket: '. socket_strerror(socket_last_error()));
}

$host = "127.0.0.1";
$port = "65001";

$result = socket_connect($socket,  $host, $port);
if ($result === false) {
    die( "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)));
}

$msg = $_POST['messageValue'];
$result = socket_send($socket, $msg, strlen($msg), 0);
$result = socket_recv($socket, $response,  16384, 0);

/* Reformat the response for HTML rendering */
echo str_replace(["\r\n", "\r", "\n"], "<br/>", $response);

?>
