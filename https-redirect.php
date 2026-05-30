<?php
/**
 * Plugin Name: Force HTTPS Redirect
 * Description: Redirects all HTTP traffic to HTTPS
 * Version: 1.0
 */

if (!is_admin() && !isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'on' && 
    (!isset($_SERVER['HTTP_X_FORWARDED_PROTO']) || $_SERVER['HTTP_X_FORWARDED_PROTO'] !== 'https') &&
    (!isset($_SERVER['HTTP_CF_VISITOR']) || strpos($_SERVER['HTTP_CF_VISITOR'], 'https') === false)) {
    
    $redirect_url = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    header('HTTP/1.1 301 Moved Permanently');
    header('Location: ' . $redirect_url);
    exit;
}

// Also set the HTTPS flag for WordPress behind reverse proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
if (isset($_SERVER['HTTP_CF_VISITOR'])) {
    $cf_visitor = json_decode($_SERVER['HTTP_CF_VISITOR'], true);
    if (isset($cf_visitor['scheme']) && $cf_visitor['scheme'] === 'https') {
        $_SERVER['HTTPS'] = 'on';
    }
}
